### Redis 事件机制

> **1. 为什么Reids是单线程的？**
>
> **2. 高并发快的原因是什么？**



Redis采用事件驱动机制来处理大量的网络IO, 自己实现了一个非常简洁的事件驱动库`ae_event`。

事件库处理下面两类事件：

- 文件事件（file event）：用于处理Redis 服务器和客户端之间的网络IO， 文件事件就是服务器对 socket 操作的抽象， Redis 服务器，通过监听这些 socket 产生的文件事件并处理这些事件，实现对客户端调用的响应。

  - 读事件： 实现命令请求的接受
  - 写事件：实现了命令结果的返回

- 时间事件（time event）：Redis服务器中的一些操作，（ServerCron函数）需要在给定的时间执行。

  服务器需要定期对自身的资源和状态进行必要的检查和整理，（过期淘汰策略等）在Redis中，常规操作由reids.c/serverCron实现，主要执行以下操:

  - 更新服务器的各类统计信息，比如时间、内存占用、数据库占用
  - 清理数据库中过期键值对
  - 对不合理的数据库进行大小调整
  - 关闭和清理连接失效的客户端
  - 尝试进行AOF或者RDB持久化操作
  - 如果服务器是主节点的话，对附属节点进行定期同步
  - 如果处于集群模式的话，对集群进行定期同步和连接测试

## 1. 文件事件

Redis基于 `Reactor` 模式 开发了自己的事件处理器，Reactor模式 即下图

![![aeApiPoll示意图](https://user-gold-cdn.xitu.io/2019/8/8/16c71c3f6af515b6?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)](https://user-gold-cdn.xitu.io/2019/8/8/16c71c3f68d98f5a?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![image.png](https://i.loli.net/2020/06/12/dC4f3HJXl8mFcRT.png)

通过"I/O多路复用模块"（底层也是`epoll`实现）监听多个`fd`, 当 这些 `fd` 产生， `accept`, `read`,  `write`, `close`文件操作的事件时，会讲事件放入事件池即 文件事件分发器，文件事件分发器，在收到事件后，根据事件的类型将事件分到到对应的`handlefunc`



![aeApiPoll示意图](https://user-gold-cdn.xitu.io/2019/8/8/16c71c3f6af515b6?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)



![image.png](https://i.loli.net/2020/05/30/pOaGMQHz7AiZrKI.png)

![image.png](https://i.loli.net/2020/05/30/aWV4mhDj67r5XMG.png)

## 2. 定时事件

在 Redis 中，常规操作由 redis.c/serverCron 实现，它主要执行以下操作  

- 更新服务器的各类统计信息，比如时间、内存占用、数据库占用情况等。  
- 清理数据库中的过期键值对。
- 对不合理的数据库进行大小调整。
- 关闭和清理连接失效的客户端。
- 尝试进行 AOF 或 RDB 持久化操作。
- 如果服务器是主节点的话，对附属节点进行定期同步。
- 如果处于集群模式的话，对集群进行定期同步和连接测试  

Redis 将 serverCron 作为时间事件来运行，从而确保它每隔一段时间就会自动运行一次，又
因为 serverCron 需要在 Redis 服务器运行期间一直定期运行，所以它是一个循环时间事件：
serverCron 会一直定期执行，直到服务器关闭为止。  

在 Redis 2.6 版本中，程序规定 serverCron 每隔 10 毫秒就会被运行一次。从 Redis 2.8 开始，
10 毫秒是 serverCron 运行的默认间隔，而具体的间隔可以由用户自己调整。  

**为什么Reids是单线程的？**

**官方答案：**因为Redis是基于内存操作的，CPU不是Redis的瓶颈， Redis的瓶颈最有可能是机器内存的大小或者网络带宽。既然单线程容易实现，而且CPU不会成为瓶颈，那就顺理成章地采用单线程的方案。

**性能指标：**普通笔记本轻松处理每秒几十万的请求

为什么？：

- 不需要各种锁的性能消耗
- 不需要多线程的上下文切换竞争条件，保证了每个操作的原子性。
- 单线程多进程的集群方案
  - 单线程的威力实际上非常强大，每核心效率也非常高，多线程自然是可以比单线程有更高的性能上限，但是在今天的计算环境中，即使是单机多线程的上限也往往不能满足需要了，需要进一步摸索的是多服务器集群化的方案，这些方案中多线程的技术照样是用不上的

为什么快：

数据结构也帮了不少忙，Redis全程使用hash结构，读取速度快，还有一些特殊的数据结构，对数据存储进行了优化，如压缩表，对短数据进行压缩存储，再如，跳表，使用有序的数据结构加快读取的速度。

## 参考博文与书籍

1. [Redis 事件机制详解](https://juejin.im/post/5d4c3a5df265da03934bcbe8)
2. [Redis 中的事件驱动模型-阿里工程师犀利豆](https://www.xilidou.com/2018/03/22/redis-event/)
3. [为什么说Redis是单线程的以及Redis为什么这么快](https://blog.csdn.net/xlgen157387/article/details/79470556)
4. [正式支持多线程！Redis 6.0与老版性能对比评测](https://blog.csdn.net/weixin_45583158/article/details/100143587)
5. 《redis设计与实现》