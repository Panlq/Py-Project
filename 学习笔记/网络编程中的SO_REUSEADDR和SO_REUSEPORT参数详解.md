# 网络编程中的SO_REUSEADDR和SO_REUSEPORT参数详解

***转载自:*** [bloomingtony.club](https://zhuanlan.zhihu.com/p/35367402)

### SO_REUSEADDR

![img](http://xiaorui.cc/wp-content/uploads/2015/12/20151202150525_52816.png)

目前为止我见到的设置SO_REUSEADDR的使用场景：server端在调用bind函数时

setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR,(const void *)&reuse , sizeof(int));

目的：当服务端出现timewait状态的链接时，确保server能够重启成功。

注意：**SO_REUSEADDR只有针对time-wait链接(linux系统time-wait连接持续时间为1min)，确保server重启成功的这一个作用**，至于网上有文章说：如果有socket绑定了0.0.0.0:port；设置该参数后，其他socket可以绑定本机ip:port。本人经过试验后均提示“Address already in use”错误，绑定失败。

举个例子：

server监听9980端口，由于主动关闭链接，产生了一个time-wait状态的链接：

![img](https://pic4.zhimg.com/80/v2-b99ae4f97cc2d26bb2e9010efab91fef_720w.jpg)

如果此时server重启，并且server没有设置SO_REUSEADDR参数，server重启失败，报错：“Address already in use”

如果设置SO_REUSEADDR，重启ok；





### SO_REUSEPORT

![img](http://xiaorui.cc/wp-content/uploads/2015/12/20151202150747_49312.png)

SO_REUSEPORT使用场景：linux kernel 3.9 引入了最新的SO_REUSEPORT选项，使得多进程或者多线程创建多个绑定同一个ip:port的监听socket，提高服务器的接收链接的并发能力,程序的扩展性更好；此时需要设置SO_REUSEPORT（**注意所有进程都要设置才生效**）。

setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT,(const void *)&reuse , sizeof(int));

目的：每一个进程有一个独立的监听socket，并且bind相同的ip:port，独立的listen()和accept()；提高接收连接的能力。（例如nginx多进程同时监听同一个ip:port）

解决的问题：

**（1）避免了应用层多线程或者进程监听同一ip:port的“惊群效应”。**

**（2）内核层面实现负载均衡，保证每个进程或者线程接收均衡的连接数。**

**（3）只有effective-user-id相同的服务器进程才能监听同一ip:port （安全性考虑）**



### 参考：

[使用socket so_reuseport提高服务端性能](http://xiaorui.cc/archives/2413)

[SO_REUSEADDR和SO_REUSEPORT区别](https://www.jianshu.com/p/a23b7e8a4c6a)

[StackOverflow](https://link.jianshu.com/?t=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F14388706%2Fsocket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t).

待查看资料：《UNIX网络编程卷1：套接字API》