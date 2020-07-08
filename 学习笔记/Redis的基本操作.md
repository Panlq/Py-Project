Redis的基本操作

[Redis SCAN的使用](http://jinguoxing.github.io/redis/2018/09/04/redis-scan/)

[ Redis 命令参考](http://redisdoc.com/index.html)

[面试中关于Redis的问题看这篇就够了](https://juejin.im/post/5ad6e4066fb9a028d82c4b66)

[万亿级日访问量下，Redis在微博的9年优化历程](https://cloud.tencent.com/developer/news/462944)

[**Redis集群Proxy支持select命令方案介绍**](https://yq.aliyun.com/articles/69349?spm=5176.154649.801568.2.kNutr4)

[超硬核！16000 字 Redis 面试知识点总结，这还不赶紧收藏？](https://juejin.im/post/5e9da97ff265da47da2ae848#heading-14)

![img](http://ata2-img.cn-hangzhou.img-pub.aliyun-inc.com/820ab08721f08edea307cf0171fbb88b.png)



[mysql binlog**应用场景**与原理深度剖析](http://www.jiangxinlingdu.com/mysql/2019/06/07/binlog.html)

[Redis实战：如何构建类微博的亿级社交平台](https://www.jianshu.com/p/51f9c39cd1e4)

![Redis深入之道：原理解析、场景使用以及视频解读](https://pic3.zhimg.com/v2-03287e93d21076afb78f672bf0ab92e4_1440w.jpg)

[Redis深入之道：原理解析、场景使用以及视频解读](https://zhuanlan.zhihu.com/p/28073983) 很全面的信息

[阿里云redis大key搜索工具](https://developer.aliyun.com/article/117042)  scan/iscan

## Reids相关面试题

1. **Redis的两种持久化操作以及如何保障数据安全（快照和AOF）**
2. **如何防止数据出错（Redis事务）**
3. **如何使用流水线来提升性能**
4. **Redis主从复制**
5. **Redis集群的搭建**
6. **Redis的几种淘汰策略**
7. **Redis集群宕机，数据迁移问题**
8. **Redis缓存使用有很多，怎么解决缓存雪崩和缓存穿透？**

### 什么是Redis？

> Redis 是一个使用 C 语言写成的，开源的 key-value 数据库。。和Memcached类似，它支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。这些数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。在此基础上，redis支持各种不同方式的排序。与memcached一样，为了保证效率，数据都是缓存在内存中。区别的是redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。目前，Vmware在资助着redis项目的开发和维护。

### Redis与Memcached的区别与比较

1 、Redis不仅仅支持简单的k/v类型的数据，同时还提供list，set，zset，hash等数据结构的存储。memcache支持简单的数据类型，String。

2 、Redis支持数据的备份，即master-slave模式的数据备份。

3 、Redis支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用,而Memecache把数据全部存在内存之中

4、 redis的速度比memcached快很多

5、Memcached是多线程，非阻塞IO复用的网络模型；Redis使用单线程的IO复用模型。

6、value的大小：redis可以达到1GB，而memcache只有1MB。



![Redis与Memcached的区别与比较](https://user-gold-cdn.xitu.io/2018/4/18/162d7773080d4570?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### Redis与Memcached的选择

**终极策略：** 使用Redis的String类型做的事，都可以用Memcached替换，以此换取更好的性能提升； 除此以外，优先考虑Redis；

### 使用redis有哪些好处？

(1) **速度快**，因为数据存在内存中，类似于HashMap，HashMap的优势就是查找和操作的时间复杂度都是O(1)

(2)**支持丰富数据类型**，支持string，list，set，sorted set，hash

(3) **支持事务** ：redis对事务是部分支持的，如果是在入队时报错，那么都不会执行；在非入队时报错，那么成功的就会成功执行。详细了解请参考：《Redis事务介绍（四）》：[blog.csdn.net/cuipeng0916…](https://blog.csdn.net/cuipeng0916/article/details/53698774)

redis监控：锁的介绍

(4) **丰富的特性**：可用于缓存，消息，按key设置过期时间，过期后将会自动删除

### Redis常见数据结构使用场景

#### 1. String

> **常用命令:**  set,get,decr,incr,mget 等。

String数据结构是简单的key-value类型，value其实不仅可以是String，也可以是数字。 常规key-value缓存应用； 常规计数：微博数，粉丝数等。

#### 2.Hash

> **常用命令：** hget,hset,hgetall 等。

Hash是一个string类型的field和value的映射表，hash特别适合用于存储对象。 比如我们可以Hash数据结构来存储用户信息，商品信息等等。

**举个例子：** 最近做的一个电商网站项目的首页就使用了redis的hash数据结构进行缓存，因为一个网站的首页访问量是最大的，所以通常网站的首页可以通过redis缓存来提高性能和并发量。我用**jedis客户端**来连接和操作我搭建的redis集群或者单机redis，利用jedis可以很容易的对redis进行相关操作，总的来说从搭一个简单的集群到实现redis作为缓存的整个步骤不难。感兴趣的可以看我昨天写的这篇文章：

**《一文轻松搞懂redis集群原理及搭建与使用》：** [juejin.im/post/5ad54d…](https://juejin.im/post/5ad54d76f265da23970759d3)

#### 3.List

> **常用命令:** lpush,rpush,lpop,rpop,lrange等

list就是链表，Redis list的应用场景非常多，也是Redis最重要的数据结构之一，比如微博的关注列表，粉丝列表，最新消息排行等功能都可以用Redis的list结构来实现。

Redis list的实现为一个双向链表，即可以支持反向查找和遍历，更方便操作，不过带来了部分额外的内存开销。

#### 4.Set

> **常用命令：** sadd,spop,smembers,sunion 等

set对外提供的功能与list类似是一个列表的功能，特殊之处在于set是可以自动排重的。 当你需要存储一个列表数据，又不希望出现重复数据时，set是一个很好的选择，并且set提供了判断某个成员是否在一个set集合内的重要接口，这个也是list所不能提供的。

在微博应用中，可以将一个用户所有的关注人存在一个集合中，将其所有粉丝存在一个集合。Redis可以非常方便的实现如共同关注、共同喜好、二度好友等功能。

#### 5.Sorted Set

> **常用命令：** zadd,zrange,zrem,zcard等

和set相比，sorted set增加了一个权重参数score，使得集合中的元素能够按score进行有序排列。

**举例：** 在直播系统中，实时排行信息包含直播间在线用户列表，各种礼物排行榜，弹幕消息（可以理解为按消息维度的消息排行榜）等信息，适合使用Redis中的SortedSet结构进行存储。

### MySQL里有2000w数据，Redis中只存20w的数据，如何保证Redis中的数据都是热点数据（redis有哪些数据淘汰策略？？？）

   相关知识：redis 内存数据集大小上升到一定大小的时候，就会施行数据淘汰策略（回收策略）。redis 提供 6种数据淘汰策略：

1. **volatile-lru**：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
2. **volatile-ttl**：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
3. **volatile-random**：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
4. **allkeys-lru**：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
5. **allkeys-random**：从数据集（server.db[i].dict）中任意选择数据淘汰
6. **no-enviction**（驱逐）：禁止驱逐数据

### Redis内存回收使用的是什么算法?

**Redis内存回收:LRU算法（写的很不错，推荐）**：[www.cnblogs.com/WJ5888/p/43…](https://www.cnblogs.com/WJ5888/p/4371647.html)

### Redis 大量数据插入

官方文档给的解释：[www.redis.cn/topics/mass…](http://www.redis.cn/topics/mass-insert.html)

### Redis常见性能问题和解决方案:

1. Master最好不要做任何持久化工作，如RDB内存快照和AOF日志文件
2. 如果数据比较重要，某个Slave开启AOF备份数据，策略设置为每秒同步一次
3. 为了主从复制的速度和连接的稳定性，Master和Slave最好在同一个局域网内
4. 尽量避免在压力很大的主库上增加从库

### Redis与消息队列

> 作者：翁伟 链接：https://www.zhihu.com/question/20795043/answer/345073457

不要使用redis去做消息队列，这不是redis的设计目标。但实在太多人使用redis去做去消息队列，redis的作者看不下去，另外基于redis的核心代码，另外实现了一个消息队列disque： antirez/disque:[github.com/antirez/dis…](https://github.com/antirez/disque)部署、协议等方面都跟redis非常类似，并且支持集群，延迟消息等等。

我在做网站过程接触比较多的还是使用redis做缓存，比如秒杀系统，首页缓存等等。


作者：Guide哥
链接：https://juejin.im/post/5ad6e4066fb9a028d82c4b66
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



### 是否使用过Redis集群，集群的原理是什么？

Redis Sentinal着眼于高可用，在master宕机时会自动将slave提升为master，继续提供服务。

Redis Cluster着眼于扩展性，在单个redis内存不足时，使用Cluster进行分片存储。

### 如何使用过Redis做异步队列？

一般使用list结构作为队列，rpush生产消息，lpop消费消息。当lpop没有消息的时候，要适当sleep一会再重试。

如果不用sleep，list还有个指令叫blpop，在没有消息的时候，它会阻塞住直到消息到来。

如果想要生产一次消费多次，可以使用pub/sub主题订阅者模式，可以实现1:N的消息队列，但在消费者下线后，生产的消息会丢失，想要持久化的话，需要使用消息队列如rabbitmq等。

### redis如何实现延时队列？

使用sortedset，拿时间戳作为score，消息内容作为key调用zadd来生产消息，消费者用zrangebyscore指令获取N秒之前的数据轮询进行处理。

### 如果有大量的key需要设置同一时间过期，需要注意什么？

如果大量的key过期时间设置的过于集中，到过期的那个时间点，redis可能会出现短暂的卡顿现象。一般需要在过期时间上加一个随机值，使得过期时间分散一些。

### Redis单点吞吐量

单点TPS达到8万/秒，QPS达到10万/秒，补充下TPS和QPS的概念

1. QPS: 应用系统每秒钟最大能接受的用户访问量。每秒钟处理完请求的次数，注意这里是处理完，具体是指发出请求到服务器处理完成功返回结果。可以理解在server中有个counter，每处理一个请求加1，1秒后counter=QPS。
2. TPS： 每秒钟最大能处理的请求数。每秒钟处理完的事务次数，一个应用系统1s能完成多少事务处理，一个事务在分布式处理中，可能会对应多个请求，对于衡量单个接口服务的处理能力，用QPS比较合理。

### Redis哈希槽

Redis集群没有使用一致性hash,而是引入了哈希槽的概念，当需要在 Redis 集群中放置一个 key-value 时，根据 CRC16(key) mod 16384的值，决定将一个key放到哪个桶中。

### Redis集群最大节点个数是多少？

Redis集群预分好16384个桶(哈希槽)

### Redis事务是什么？

Redis事务可以一次执行多个命令，有以下特点：

- 批量操作在发送 EXEC 命令前被放入队列缓存。
- 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。
- 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。

事务可以理解为一个打包的批量执行脚本，但批量指令并非原子化的操作，中间某条指令的失败不会导致前面已做指令的回滚，也不会造成后续的指令不做。
[彻底搞懂Redis的线程模型](https://juejin.im/post/5dabdb1ee51d45216d7b166a)