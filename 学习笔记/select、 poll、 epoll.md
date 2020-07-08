### I/O模式及select、 poll、 epoll 

### I/O多路复用技术

复用技术（multiplexing）并不是新技术而是一种设计思想，在通信和硬件设计中存在频分复用、时分复用、波分复用、码分复用等。在日常生活中复用的场景也非常多。从本质上来说，复用就是为了解决有限资源和过多使用者的不平衡问题，且此技术的理论基础是 资源的可释放性。

资源的可释放性： 不可释放场景：ICU病房的呼吸机是有限资源，病人一旦占用且在未脱离危险之前是无法放弃占用的，因此不可能几个情况一样的病人轮流使用。可释放场景：对于一些其他资源比如医护人员就可以实现对多个病人的同时监护。

I/O多路复用就是通过一种机制，一个进程可以监听多个文件描述符，一旦某个描述符就绪，可读或可写，能够通知程序进行响应的操作。

**用户空间和内核空间**

> 将大量的文件描述符托管给内核，内核将最底层的I/O状态封装成读写事件，这样就避免了由程序员去主动轮询状态变化的重复工作，开发者将回掉函数注册到epoll，当检测到相对应文件描述符产生状态变化时，就进行函数回调。select/poll由于效率问题(使用轮询检测)基本已经被epoll和kqueue取代。

### 阻塞 I/O（blocking IO）

在linux中，默认情况下所有的socket都是blocking，一个典型的读操作流程大概是这样：

![](https://segmentfault.com/img/bVm1c3/view)


当用户进程调用了recvfrom这个系统调用，kernel就开始了IO的第一个阶段：准备数据（对于网络IO来说，很多时候数据在一开始还没有到达。比如，还没有收到一个完整的UDP包。这个时候kernel就要等待足够的数据到来）。这个过程需要等待，也就是说数据被拷贝到操作系统内核的缓冲区中是需要一个过程的。而在用户进程这边，整个进程会被阻塞（当然，是进程自己选择的阻塞）。当kernel一直等到数据准备好了，它就会将数据从kernel中拷贝到用户内存，然后kernel返回结果，用户进程才解除block的状态，重新运行起来。

所以，blocking IO的特点就是在IO执行的两个阶段都被block了。

### 非阻塞I/O（nonblocking IO）

linux下，可以通过设置socket使其变为non-blocking。当对一个non-blocking socket执行读操作时，流程是这个样子：

![preview](https://segmentfault.com/img/bVm1c4/view)

当用户进程发出read操作时，如果kernel中的数据还没有准备好，那么它并不会block用户进程，而是立刻返回一个error。从用户进程角度讲 ，它发起一个read操作后，并不需要等待，而是马上就得到了一个结果。用户进程判断结果是一个error时，它就知道数据还没有准备好，于是它可以再次发送read操作。一旦kernel中的数据准备好了，并且又再次收到了用户进程的system call，那么它马上就将数据拷贝到了用户内存，然后返回。

>  所以，nonblocking IO的特点是用户进程需要不断的主动询问kernel数据好了没有。

### /I/O 多路复用（ IO multiplexing）

IO multiplexing就是我们说的select，poll，epoll，有些地方也称这种IO方式为event driven IO。select/epoll的好处就在于单个process就可以同时处理多个网络连接的IO。它的基本原理就是select，poll，epoll这个function会不断的轮询所负责的所有socket，当某个socket有数据到达了，就通知用户进程。

![preview](https://segmentfault.com/img/bVm1c5/view)

当用户进程调用了select，那么整个进程会被block，而同时，kernel会“监视”所有select负责的socket，当任何一个socket中的数据准备好了，select就会返回。这个时候用户进程再调用read操作，将数据从kernel拷贝到用户进程。

> 所以，I/O 多路复用的特点是通过一种机制一个进程能同时等待多个文件描述符，而这些文件描述符（套接字描述符）其中的任意一个进入读就绪状态，select()函数就可以返回。

### 异步I/O(asynchronous I/O)

Linux下的asynchronous IO其实用得很少。先看一下它的流程：

![preview](https://segmentfault.com/img/bVm1c8/view)

用户进程发起read操作之后，立刻就可以开始去做其它的事。而另一方面，从kernel的角度，当它受到一个asynchronous read之后，首先它会立刻返回，所以不会对用户进程产生任何block。然后，kernel会等待数据准备完成，然后将数据拷贝到用户内存，当这一切都完成之后，kernel会给用户进程发送一个signal，告诉它read操作完成了。

#### blocking和non-blocking的区别
调用blocking IO会一直block住对应的进程直到操作完成，而non-blocking IO在kernel还准备数据的情况下会立刻返回



#### synchronous IO和asynchronous IO的区别

在说明synchronous IO和asynchronous IO的区别之前，需要先给出两者的定义。POSIX的定义是这样子的：
- A synchronous I/O operation causes the requesting process to be blocked until that I/O operation completes;
- An asynchronous I/O operation does not cause the requesting process to be blocked;

有人会说，non-blocking IO并没有被block啊。这里有个非常“狡猾”的地方，定义中所指的”IO operation”是指真实的IO操作，就是例子中的recvfrom这个system call。**non-blocking IO在执行recvfrom这个system call的时候，如果kernel的数据没有准备好，这时候不会block进程。但是，当kernel中数据准备好的时候，recvfrom会将数据从kernel拷贝到用户内存中，这个时候进程是被block了，在这段时间内，进程是被block的。**

而asynchronous IO则不一样，当进程发起IO 操作之后，就直接返回再也不理睬了，直到kernel发送一个信号，告诉进程说IO完成。在这整个过程中，进程完全没有被block。





![preview](https://segmentfault.com/img/bVm1c9/view)

通过上面的图片，可以发现non-blocking IO和asynchronous IO的区别还是很明显的。在non-blocking IO中，虽然进程大部分时间都不会被block，但是它仍然要求进程去主动的check，并且当数据准备完成以后，也需要进程主动的再次调用recvfrom来将数据拷贝到用户内存。而asynchronous IO则完全不同。它就像是用户进程将整个IO操作交给了他人（kernel）完成，然后他人做完后发信号通知。在此期间，用户进程不需要去检查IO操作的状态，也不需要主动的去拷贝数据。

##  I/O 多路复用之select、poll、epoll详解

### Select

```c++
#include <sys/select.h>

/*According to earlier standards*/
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);

// select 四个宏
void FD_CLR(int fd, fd_set *set);
int FD_ISSET(int fd, fd_set, *set);
void FD_SET(int fd, fd_set *set);
void FD_ZERO(fd_set *set);

# ifndef FD_SETSIZE
#define FD_SETSIZE 1024
#endif

```



假定fd_set长度为1字节，则一字节长度的fd_set最大可以对应8个fd。

Select的调用过程如下：

1. 执行FD_ZERO(&set)，则set用位表示是0000,0000
2. 若fd=5, 执行FD_SET(fd, &set); set后 bitmap 变为 0001,0000 (第5位置1)
3. 若加入fd=2, fd=1, 则set 变为 0001,0011
4. 执行select(6, &set, 0, 0, 0)
5. 若fd=1, fd=2上都发生可读时间，则select返回，此时set变为0000,0011，没有事件发生的fd=5被清空

**select 特点**

1. 可监控的文件描述符个数取决于 sizeof(fd_set) 的值。假设服务器上 sizeof(fd_set)＝512，每 bit 表示一个文件描述符，则服务器上支持的最大文件描述符是 512*8=4096。fd_set 的大小调整可参考 [【原创】技术系列之 网络模型（二）](http://www.cppblog.com/CppExplore/archive/2008/03/21/45061.html) 中的模型 2，可以有效突破 select 可监控的文件描述符上限。一般来说这个数目和系统内存关系很大，具体数目可以`cat /proc/sys/fs/file-max`察看。32位机默认是1024个。64位机默认是2048.

**select缺点：**

1. 最大并发数限制：select 的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制，在Linux上一般为1024， 可以通过修改宏定义设置重新编译内核的方式提升这一限制，但是这样也会造成效率的降低。有以下2，3点瓶颈
2. 每次调用select ， 都需要把fd集合从用户态拷贝到内核态，这个开销在fd很多时会很大
3. 性能衰减严重：每次kernel都需要线性扫描整个fd_set，所以随着监控fd数量增加，I/0性能线性下降

网卡如何接收数据，当网卡把数据写入内存后，网卡向CPU发出一个中断信号，操作系统便能得知有新数据到来，再通过网卡中断程序去处理数据。

### Poll

> ```c++
> int poll (struct pollfd *fds, unsigned int nfds, int timeout);
> ```

Poll的实现和select相似，只是存储fd的结构不同，polll使用**pollfd**结构而不是**bitmap**, pollfd是一个数组，数组就解决得了最大文件描述符数量限制的问题。pollfd结构包含了要监视的event和发生的event，不再使用selectc参数-值传递的方式。但是同样需要从用户态拷贝fd到内核态，且是线性循环遍历所有fd集合来判断可读连接的，所以本质上没有区别。poll返回后，仍然需要轮询pollfd来获取就绪的描述符。

```c++
struct pollfd {
    int fd;         /*file descriptor*/
    short events;   /*requested events to watch*/
    short revents;  /*returned events witnessed*/
}
```

> 从上面看，select和poll都需要在返回后，通过遍历文件描述符来获取已经就绪的socket。事实上，同时连接的大量客户端在一时刻可能只有很少的处于就绪状态，因此随着监视的描述符数量的增长，其效率也会线性下降。

### epoll

相对于select和poll来说，epoll更加灵活，没有描述符限制。epoll使用一个文件描述符管理多个描述符，将用户关系的文件描述符的事件存放到内核的一个事件表中，这样在用户空间和内核空间的copy只需一次。

**epoll 的API设计以下3的函数**

```c++
#include <sys/epoll.h>
int epoll_create(int size);
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
/*	op参数
	EPOLL_CTL_ADD
	EPOLL_CTL_MOD
	EPOLL_CTL_DEL
*/
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);

/*
timeout:
	-1: 阻塞
	0：立即返回
	>0：指定毫秒
*/
```

- `epoll_create` 创建一个epoll实例并返回epollfd，size用来告诉内核这个监听的数目一共多大，并不是限制了epoll所能监听的描述符最大数，**只是对内核初始分配 红黑树节点个数据的一个建议**。

> 当创建好epoll句柄后，它就会占用一个fd值，在linux下如果查看/proc/进程id/fd/，是能够看到这个fd的，所以在使用完epoll后，必须调用close()关闭，否则可能导致fd被耗尽
>

- **epoll_ctl(int epfd, int op, int fd, struct epoll_event \*event)；**

  - -epfd： epoll_create()的返回值

  - -op：表示操作，用三个宏来表示： EPOLL_CTL_ADD（添加），EPOLL_CTL_MOD（修改）， EPOLL_CTL_DEL（删除）

  - -fd：需要监听的fd文件描述符

  - epoll_event：告诉内核需要监听什么，struct_epoll_event结构如下

  - ```c++
    struct epoll_event {
        unit32_t events;
        epoll_data_t  data;
    }
    
    //events 可以是一下几个宏的集合
    EPOLLIN: 表示对应的文件描述符可以读
    EPOLLOUT: 表示对应文件描述符可以写
    EPOLLPRI: 表示对应文件描述符有紧急的数据可读
    EPOLLERR: 表示文件描述符发生错误
    EPOLLHUP: 表示对应的文件描述符被挂断
    EPOLLET: 将EPOLL设为边缘出发模式
    EPOLLONNESHOT: 只监听一个事件，当监听完这次事件之后，如果还需要继续监听这个socket的话，需要再次把这个socket加入到EPOLL队列里
    ```

  - ```c++
    typedef union epoll_data {
        void   *ptr;
        int    fd;
        unit32_t  u32;
        unit64_t  u64;
    } epoll_data_t;
    ```

- epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout)

  参数events用来从内核得到事件集合，maxevents告诉内核这个events多大，不能大于epoll_create()的size.

  **则是阻塞监听epoll实例上所有的 file descriptor的I/O事件，接收用户空间上的一块内存地址（events数组） ，kernel会在有I/O事件发生的时候会把文件描述符列表 rdlist 复制到 这块内存上，然后epoll_wail解阻塞并返回。**

#### epoll 工作模式

- LT模式(默认模式)：当epoll_wait检测到描述符事件发生并将此事件通知应用程序，应用程序可以不立即处理该事件，下次调用epoll_wait时，会再次相应应用程序并通知此事件
- ET模式：当epoll_wait检测描述符事件发生并将此事件通知应用程序，应用程序必须立即处理该事件，如果不处理，下次调用epoll_wait时，不会再次响应程序并通知此事件。一般会设置一个定期的事件清除未处理缓存。**ET模式在很大程度上减少了epoll事件被重复触发的次数，因此效率要比LT模式高**。**epoll工作在ET模式的时候，必须使用非阻塞套接口**，以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。

#### epoll 监听事件的数据结构及其原理

在实现上 epoll 采用红黑树来存储所有监听的 fd，而红黑树本身插入和删除性能比较稳定，时间复杂度 O(logN)。通过 `epoll_ctl` 函数添加进来的 fd 都会被放在红黑树的某个节点内，所以，重复添加是没有用的。当把 fd 添加进来的时候时候会完成关键的一步：**该 fd 会与相应的设备（网卡）驱动程序建立回调关系，也就是在内核中断处理程序为它注册一个回调函数，在 fd 相应的事件触发（中断）之后（设备就绪了），内核就会调用这个回调函数，该回调函数在内核中被称为：** `ep_poll_callback` ，**这个回调函数其实就是把这个 fd 添加到 rdllist 这个双向链表（就绪链表）中**。`epoll_wait `实际上就是去检查 **rdlist** 双向链表中是否有就绪的 fd，当 rdlist 为空（无就绪 fd）时挂起当前进程，直到 rdlist 非空时进程才被唤醒并返回。

![image.png](https://i.loli.net/2020/06/04/ul1RNcziAaHLZ79.png)

>  图片来源：《深入理解Nginx：模块开发与架构解析(第二版)》，陶辉

##### epoll实现细节

- 就绪队列的数据结构，就绪列表引用就绪的socket， 所以能够快速插入数据。程序可能随时调用epoll_ctl添加监视socket， 也可能随时删除。当删除时，若该socket已经存放在就绪列表中，它也应该被移除。所以就绪列表应该是一种能快速插入和删除的数据结构。**双向链表是epoll中实现就绪队列的数据结构**，
- 既然 epoll 将“维护监视队列”和“进程阻塞”分离，也意味着需要有个数据结构来保存监视的 socket，至少要方便地添加和移除，还要便于搜索，以避免重复添加。红黑树是一种自平衡二叉查找树，搜索、插入和删除时间复杂度都是O(log(N))，效率较好，epoll 使用了红黑树作为索引结构（对应上图的 rbr）

### 小结

| I/O多路复用 | select                                                       | poll                                                         | epoll                                                        |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 时间复杂度  | O(n)                                                         | O(n)                                                         | O(k) k表示被激活的事件fd个数                                 |
| 实现机制    | 无差别轮询监听的fd（三组流数据：可读，可写，异常）           | 无差别轮询，查看每个fd绑定的事件状态                         | 事件回掉，将fd与网卡设备绑定一个回到函数，当fd就绪，调用回调函数，将就绪fd放入 rdlist链表中，kernel把有I/O事件发生的文件描述符列表 **rdlist** 复制到 epoll_wait用户指定的内存events内， epoll_wait 解阻塞并返回给应用 |
| 数据结构    | 三个bitmap                                                   | 数组存放struct -pollfd                                       | 红黑树(socket) + 双向链表(就绪队列)                          |
| 最大连接数  | 1024(x86) / 2048(x64)                                        | 无上限，同epoll解释                                          | 无上限，在1GB内存的机器上大约是10万左右，具体数目可以cat /proc/sys/fs/file-max察看 |
| 优缺点      | 1. 可移植性好，有些Unix系统不支持poll(), 对超时值提供了微妙级别的精确度<br />2. 单进程可监听fd的数量有限制<br />3. 用户态需要每次`select`之前复位所有fd，然后`select`之后还得遍历所有`fd`找到可读写或异常的`fd`，IO效率随FD的增加而线性下降<br />4. 每次select调用都需要把fd集合从用户态拷贝到内核态 | 1. 没有最大连接限制 <br />2. 与select一样，poll返回后，需要轮询整个pollfd集合来获取就绪的描述符,IO效率随FD的增加而线性下降<br />3. 大量的fd的数组被整体复制于用户态和内核地址空间之间，浪费资源 | 1.没有最大连接树限制<br />2.内核拷贝只返回活跃的连接，**而跟连接总数无关，因此在实际的网络环境中，Epoll的效率就会远远高于select和poll。** |
| 工作模式    | LT                                                           | LT                                                           | LT/ET                                                        |

select，poll实现需要自己不断轮询所有fd集合，直到设备就绪，期间可能要睡眠和唤醒多次交替。

而epoll其实也需要调用 epoll_ wait不断轮询就绪链表，期间也可能多次睡眠和唤醒交替，但是它是设备就绪时，调用回调函数，把就绪fd放入就绪链表中，并唤醒在 epoll_wait中进入睡眠的进程。　

**虽然都要睡眠和交替，但是select和poll在“醒着”的时候要遍历整个fd集合，而epoll在“醒着”的 时候只要判断一下就绪链表是否为空就行了，这节省了大量的CPU时间，这就是回调机制带来的性能提升**。



#### 高性能网络模式之 Reactor模式

反应器设计模式（Reator pattern）是一种基于事件驱动的设计模式，常用于高并发场景下，常见的像Node.js、Netty、Vert.x中都有着Reactor模式的身影

Reactor 模式本质上指的是使用 `I/O 多路复用(I/O multiplexing) + 非阻塞 I/O(non-blocking I/O)` 的模式

高并发模式最好的就是 `非阻塞I/O+epoll ET` 模式



### 惊群效应

使用多个进程监听同一端口就绕不开惊群这个话题, fork子进程, 子进程共享`listen socket fd`, 多个子进程同时accept阻塞, 在请求到达时内核会唤醒所有accept的进程, 然而只有一个进程能accept成功, 其它进程accept失败再次阻塞, 影响系统性能, 这就是惊群. Linux 2.6内核更新以后多个进程accept只有一个进程会被唤醒, 但是如果使用epoll还是会产生惊群现象.

Nginx为了解决epoll惊群问题, 使用进程间互斥锁, 只有拿到锁的进程才能把`listen fd`加入到epoll中, 在accept完成后再释放锁.

但是在高并发情况下, 获取锁的开销也会影响性能, 一般会建议把锁配置关掉. 直到Nginx 1.9.1更新支持了socket的`SO_REUSEPORT`选项, 惊群问题才算解决, `listen socket fd`不再是在master进程中创建, 而是每个worker进程创建一个通过`SO_REUSEPORT` 选项来复用端口, 内核会自行选择一个fd来唤醒, 并且有负载均衡算法.[Gunicorn与uWSGI之我见]([https://zhu327.github.io/2018/08/29/gunicorn%E4%B8%8Euwsgi%E4%B9%8B%E6%88%91%E8%A7%81/](https://zhu327.github.io/2018/08/29/gunicorn与uwsgi之我见/))



### **文件描述符FD（file descriptor）**

> Linux中一切皆文件

![](https://img2020.cnblogs.com/blog/778496/202007/778496-20200706172207428-2098342208.png)

0   ----> 标准输入

1   ----> 标准输出

2   ----> 标准错误

0，1，2 固定描述符，所以文件描述符是从3开始



### 参考资料

[转载自---Linux IO模式及 select、poll、epoll详解](https://segmentfault.com/a/1190000003063859) 

[epoll 或者 kqueue 的原理是什么？](https://www.zhihu.com/question/20122137)

[如果这篇文章说不清epoll的本质，那就过来掐死我吧-罗培羽](https://zhuanlan.zhihu.com/p/63179839)

