import socket
import struct
from datetime import datetime
import json


class StockClient:
    def __init__(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock:
            self.sock.close()

    def sub(self, stock_codes, interval, start_date, end_date):
        """
        订阅股票分钟数据
        :param stock_codes: 股票代码列表, 如 ["111234", "342444", "HZ0909"]
        :param interval: 时间间隔, 如 "1m"
        :param start_date: 开始日期 datetime对象
        :param end_date: 结束日期 datetime对象
        """
        if not self.sock:
            self.connect()

        # 构造请求数据
        request = {
            "action": "sub",
            "stocks": stock_codes,
            "interval": interval,
            "start_date": start_date.timestamp(),
            "end_date": end_date.timestamp(),
        }
        request_json = json.dumps(request).encode("utf-8")

        # 使用struct打包: 4字节长度(小端) + json数据
        packed_data = struct.pack("<I", len(request_json)) + request_json
        self.sock.sendall(packed_data)

        # 接收数据流
        self._receive_stream()

    def _receive_stream(self):
        """接收并处理数据流"""
        try:
            while True:
                # 先读取4字节的消息长度(小端)
                raw_len = self._recv_n(4)
                if not raw_len:
                    break
                msg_len = struct.unpack("<I", raw_len)[0]

                # 读取实际消息
                raw_msg = self._recv_n(msg_len)
                if not raw_msg:
                    break

                # 解析消息
                try:
                    data = json.loads(raw_msg.decode("utf-8"))
                    if self._handle_data(data):
                        print("Received end of stream signal")
                        break
                except json.JSONDecodeError:
                    print("Invalid JSON data received")

        except ConnectionResetError:
            print("Connection closed by server")
        finally:
            self.close()

    def _recv_n(self, n):
        """精确接收n字节数据"""
        data = bytearray()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)

    def _handle_data(self, data):
        """处理接收到的数据"""
        if data.get("type") == "stock_data":
            print(f"Received stock data: {data}")
            return False
        elif data.get("type") == "end_of_stream":
            print("End of data stream reached")
            return True
        else:
            print(f"Unknown message type: {data}")
            return False


# 使用示例
if __name__ == "__main__":
    client = StockClient()
    try:
        stock_codes = ["111234", "342444", "HZ0909"]
        interval = "1h"
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 2)

        print(f"Subscribing to {stock_codes} from {start_date} to {end_date}")
        client.sub(stock_codes, interval, start_date, end_date)
    except KeyboardInterrupt:
        client.close()
