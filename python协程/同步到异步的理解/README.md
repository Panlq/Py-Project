## 由同步到异步的思想转变
0. 一个同步io操作(syncio.py)
1. 一个同步的代码怎么变异步? (async_io.py)
2. 变成异步的代码怎么去写，才能看起来像同步? (yield_io.py)
3. 在不改变同步代码的形式，怎么实现协程异步? (yield_io2.py)

当实现到第三步的时候, 就可以大致理解tornado协成的实现机制

### 需要注意: 
1. yield并不是协程, 他实现的只是一个生成器, 用yield可以实现协程, 我们需要自己实现调度切换。
2. 第三个版本严格意义上来说不算协程, 因为是两个程序的挂起和唤醒是在两个线程上来实现的, 而Tornado(底层使用asyncio) 是用 epoll来实现异步的，程序的挂起和唤醒是在要给线程上的, 由Tronado自己来调度, 属于真正意义上的协程。
3. Tornado(ayncio)使用的是eventloop事件驱动方式来实现调度的

[Python yield的调度机制](https://www.cnblogs.com/panlq/p/13069726.html#907438336)

