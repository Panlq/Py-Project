#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <chrono>
#include <thread>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <cctype>
#include <stdexcept>
#include "json.hpp"

// 字节序转换 (兼容 macOS)
#if defined(__APPLE__)
#include <libkern/OSByteOrder.h>
#define htole32(x) OSSwapHostToLittleInt32(x)
#define le32toh(x) OSSwapLittleToHostInt32(x)
#else
#include <endian.h>
#endif

using json = nlohmann::json;

// 解析时间间隔字符串，返回秒数
int parse_interval(const std::string& interval) {
    if (interval.empty()) {
        throw std::invalid_argument("Interval cannot be empty");
    }

    size_t num_end = 0;
    while (num_end < interval.size() && isdigit(interval[num_end])) {
        num_end++;
    }

    if (num_end == 0) {
        throw std::invalid_argument("Invalid interval format: missing number");
    }

    int value = std::stoi(interval.substr(0, num_end));
    if (value <= 0) {
        throw std::invalid_argument("Interval value must be positive");
    }

    std::string unit = interval.substr(num_end);
    if (unit.empty()) {
        throw std::invalid_argument("Missing interval unit (s/m/h/d)");
    }

    if (unit == "s") {
        return value;
    } else if (unit == "m") {
        return value * 60;
    } else if (unit == "h") {
        return value * 3600;
    } else if (unit == "d") {
        return value * 86400;
    } else {
        throw std::invalid_argument("Invalid interval unit: use s/m/h/d");
    }
}

json generate_stock_data(const std::string& stock_code, time_t timestamp, double price) {
    json data;
    data["type"] = "stock_data";
    data["code"] = stock_code;
    data["timestamp"] = timestamp;
    data["price"] = price;
    data["volume"] = rand() % 10000 + 1000;
    data["open"] = price - (rand() % 100) / 100.0;
    data["high"] = price + (rand() % 100) / 100.0;
    data["low"] = price - (rand() % 100) / 100.0;
    data["close"] = price;
    return data;
}

void send_data(int client_socket, const json& data) {
    std::string msg = data.dump();
    uint32_t msg_len = msg.length();
    msg_len = htole32(msg_len);
    send(client_socket, &msg_len, sizeof(msg_len), 0);
    send(client_socket, msg.c_str(), msg.length(), 0);
}

void handle_client(int client_socket) {
    try {
        // 读取消息长度
        uint32_t msg_len;
        if (recv(client_socket, &msg_len, sizeof(msg_len), 0) <= 0) {
            close(client_socket);
            return;
        }
        msg_len = le32toh(msg_len);

        // 读取消息内容
        std::vector<char> buffer(msg_len + 1);
        if (recv(client_socket, buffer.data(), msg_len, 0) <= 0) {
            close(client_socket);
            return;
        }
        buffer[msg_len] = '\0';

        // 解析请求
        json request = json::parse(buffer.data());
        auto stocks = request["stocks"].get<std::vector<std::string>>();
        std::string interval = request["interval"];
        time_t start_date = request["start_date"];
        time_t end_date = request["end_date"];

        // 解析间隔
        int interval_sec = 1;
        try {
            interval_sec = parse_interval(interval);
            std::cout << "Streaming " << stocks.size() << " stocks with interval " 
                      << interval << " (" << interval_sec << "s)\n";
        } catch (const std::exception& e) {
            std::cerr << "Interval error: " << e.what() << ", using 1s default\n";
        }

        // 流式发送数据
        for (const auto& stock : stocks) {
            time_t current = start_date;
            while (current <= end_date) {
                double price = 100.0 + (rand() % 1000) / 10.0;
                auto data = generate_stock_data(stock, current, price);
                send_data(client_socket, data);
                
                std::cout << "Sent " << stock << " data @" << current << "\n";
                std::this_thread::sleep_for(std::chrono::milliseconds(200)); // 控制发送速度
                
                current += interval_sec;
            }
        }

        // 发送结束标记
        json end_msg = {{"type", "end_of_stream"}};
        send_data(client_socket, end_msg);
        std::cout << "Sent end_of_stream to client\n";

    } catch (const std::exception& e) {
        std::cerr << "Client handling error: " << e.what() << "\n";
    }
    close(client_socket);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8888);

    int opt = 1;
    // 设置 SO_REUSEADDR
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt (SO_REUSEADDR)");
        exit(EXIT_FAILURE);
    }

    // 仅在 Linux 上设置 SO_REUSEPORT
    #if !defined(__APPLE__) && defined(SO_REUSEPORT)
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt (SO_REUSEPORT)");
        exit(EXIT_FAILURE);
    }
    #endif

    if (bind(server_fd, (sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    std::cout << "Stock Server running on port 8888\n"
              << "Supported intervals: [number]s/m/h/d (e.g. 5s, 1m, 2h)\n";

    while (true) {
        sockaddr_in client_addr{};
        socklen_t addr_len = sizeof(client_addr);
        int client_socket = accept(server_fd, (sockaddr*)&client_addr, &addr_len);
        
        if (client_socket < 0) {
            perror("accept");
            continue;
        }

        std::cout << "New connection from " << inet_ntoa(client_addr.sin_addr) << "\n";
        std::thread(handle_client, client_socket).detach();
    }
}