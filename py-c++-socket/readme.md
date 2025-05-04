# 功能说明

python 与 c++ socket 通信案例

Python 客户端使用 struct 进行封包解包，小端通信，支持订阅多只股票的分钟数据，C++服务端流式推送数据，并在结束时发送结束标记。

这种通信方式在实际生产中的应用场景：金融实时数据分发，证券行情数据订阅推送

可继续优化的点

1. 增加心跳保持连接
2. 消息 ACK+重试队列
3. 重写数据压缩协议
4. 增加吞吐量 (高并发无锁队列 - [LMAX Disruptor 架构](https://github.com/LMAX-Exchange/disruptor))

# 环境说明

支持 linux , mac

# 编译和运行

### c++服务端

编译

> g++ -std=c++11 stock_server.cpp -o stock_server

执行

> ./stock_server

### py 客户端

> python3 stock_client.py

# 通信协议说明

**1. 数据包格式** :

- 每个消息前 4 字节是小端格式的消息长度(uint32)
- 后面跟着 JSON 格式的消息内容

**2. 订阅请求格式** :

```json
{
  "action": "sub",
  "stocks": ["111234", "342444", "HZ0909"],
  "interval": "1m",
  "start_date": 1672531200,
  "end_date": 1672617600
}
```

**3. 数据推送格式** :

```json
{
  "type": "stock_data",
  "code": "111234",
  "timestamp": 1672531260,
  "price": 123.45,
  "volume": 5000,
  "open": 123.4,
  "high": 123.5,
  "low": 123.35,
  "close": 123.45
}
```

**4. 流结束标记** :

```json
{
  "type": "end_of_stream"
}
```
