Golang/Python语言特性

Golang 静态强类型，运行效率，内存用量，类型安全都比python强 ，Python 动态强类型

go的面向对象编程核心是 组合和方法， 组合类似C语言是struct结构体的组合方式，方法类似于java的接口

Go和Erlang的并发模型都来源与CSP（(communicating sequential processes）, 但是Erlang是基于Actor和消息传递(mailbox)的并发实现的，而这是耦合的关系。Go是基于goroutine和管道(channel)的并发实现的。不管Erlang的actor还是Go的goroutine，都满足协程的特点：由编程语言实现和调度，切换在用户态完成，创建销毁开销很小。而python, 线程的切换和调度是基于操作系统实现的，而且因为GIL的存在，无法真正的做到并行。

![preview](https://segmentfault.com/img/remote/1460000021250092/view)

![img](https://i6448038.github.io/img/csp/total.png)



##### Actor模型和CSP模型的区别

- CSP并不关心发送消息的实体/task, 而是关注发送消息时消息所使用的载体，即channel.
- 在actor的设计中，actor与信箱是耦合的，而CSP中channel是作为first-calsss独立存在的
- Actor中有明确的send/receive的关系，而channel中并不区分这样的关系，执行块可以任意选择发送或者取出消息



**计算机科学领域的任何问题都可以通过增加一个间接的中间层来解决** -- G-P-M模型正是此理论践行者,此理论也用到了python的asyncio对地狱回调的处理上(使用Task+Future避免回调嵌套),是不是巧合?
其实**异步≈可中断的函数+事件循环+回调**,go和python都把嵌套结构转换成列表结构有点像算法中的递归转迭代.





python中，协程的调度是非抢占式的，也就是说一个协程必须主动让出执行机会，其他协程才有机会运行。让出执行的关键字就是 await。也就是说一个协程如果阻塞了，持续不让出 CPU，那么整个线程就卡住了，没有任何并发。