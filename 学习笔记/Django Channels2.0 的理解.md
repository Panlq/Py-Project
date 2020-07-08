# Django Channels2.0 

> 本文主要对Channels的理解，具体实现可参考官网文档.  

[Channels](https://github.com/django/channels)， Channels是针对 Django 项目的一个增强框架，它可以使同步的 Django 项目转变为异步的项目。它可以使得 Django 项目不仅支持 HTTP 请求，还可以支持 Websocket, chat协议，IOT协议 ，甚至是你自定义的协议，同时也整合了 Django 的 auth 以及 session 系統等等，工作中通常用来提供WebSocket支持和后台任务。



## channels 各个模块之间的关系流程图

![整体架构图](https://i.loli.net/2020/06/23/9Il7btewXipRzqn.png)

([图片来源](https://github.com/proofit404/asgi_rabbitmq/blob/master/docs/img/infrastructure.png))

Channels将Django从传统的请求/响应模式，改为工作进程模式，“面向事件”，不仅仅响应请求，而是响应通道中发送的大量事件：监听所有分配了消费者的通道，收到消息就运行对应的消费者。现在，Django不只是在一个连接到WSGI服务器的进程中运行，而是在三个独立的层中运行。

- Interface Server: 负责对协议进行解析，将不同协议分发到不同的Channel
- Channel Layer: 频道层，可以是一个FIFO都列，支持信息过期，对于一个监听器至多投递一次, 通常使用Reids， 不同的频道有不同的监听者，类似于任务队列──信息由 producer 投递至 channel，并设置一个 consumer 监听该 channel.
- Consumer: 消费者，接收和处理消息
- BACKGROUND PROCESSES 可以理解为类似Celery的异步任务，监听所有相关的通道，并在消息就绪时运行消费者代码

[Channels Concepts](https://channels.readthedocs.io/en/1.x/concepts.html#channels-concepts)    实践可参考[Django Channels2.0 websocket最佳实践](https://vimiix.com/post/2018/07/26/channels2-tutorial/)



**从问题出发看channels框架：**

- 如何分辨由HTTP请求和WebSocket发出的请求？
- 如何兼容Django的认证系统？
- 如何接受和推送WebSocket消息？
- 如果通过ORM保存和获取数据？



#### 1. 如何分辨由HTTP请求和WebSocket发出的请求？



![image.png](https://i.loli.net/2020/06/23/wVspTxD2ehy7Rok.png)

Interface Server: 负责协议的解析，根据协议的类型匹配对应的处理实例(Channel)，封装了一个**ProtocoltypeRouter** 类，进行路由分发，默认集成了Django的http - view 请求和认证系统。

```python
class ProtocolTypeRouter:
    """
    Takes a mapping of protocol type names to other Application instances,
    and dispatches to the right one based on protocol name (or raises an error)
    """

    def __init__(self, application_mapping):
        self.application_mapping = application_mapping
        if "http" not in self.application_mapping:
            self.application_mapping["http"] = AsgiHandler

    def __call__(self, scope):
        if scope["type"] in self.application_mapping:
            return self.application_mapping[scope["type"]](scope)
        else:
            raise ValueError(
                "No application configured for scope type %r" % scope["type"]
            )
```

#### 2. 如何兼容Django的认证系统？

```python 
# channels.auth
# Handy shortcut for applying all three layers at once
AuthMiddlewareStack = lambda inner: CookieMiddleware(
    SessionMiddleware(AuthMiddleware(inner))
)
```

[AuthMiddlewareStack](https://channels.readthedocs.io/en/latest/topics/authentication.html)用于WebSocket认证，集成了CookieMiddleware, SessionMiddleware,  AuthMiddleware, 兼容Django认证系统

#### 3. 如何接受和推送WebSocket消息？

[Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html#consumers) 用来开发符合ASGI接口规范的API, 类似Django默认的Views 是用来开发符合WSGI规范的的API

```python

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):

    """"异步处理私信应用中的websocket请求"""
    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 未登录用户拒绝连接请求
            await self.close()
        else:
            await self.channel_layer.group_add('notifications', self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """将接收到的消息返回给前端"""
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """断开连接"""
        await self.channel_layer.group_discard('notifications', self.channel_name)

```

#### 4. 如果通过ORM保存和获取数据？

```python
async def websocket_receive(self, event):
        # ORM 同步的代码
        user = User.objects.get(username=username)

        # ORM语句同步变异步，方式一
        from channels.db import database_sync_to_async
        user = await database_sync_to_async(User.objects.get(username=username))

        # ORM语句同步变异步，方式二
        @database_sync_to_async
        def get_username(username):
            return User.objects.get(username=username)

        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

```



## ASGI

全名：`Asynchronous Server Gateway Interface`。它是区别于 wsgi 的一种异步服务网关接口，不仅仅只是通过 `asyncio` 以异步方式运行，还支持多种协议。完整的文档戳[这里](https://github.com/django/asgiref/blob/master/specs/asgi.rst)

关联的几个项目：

- https://github.com/django/asgiref ASGI内存中的通道层，函数的同步异步之间相互转化需要

- https://github.com/django/daphne 支持HTTP，HTTP2和WebSocket协议服务器，启动 Channels 的项目需要， 类似uWSGI
- https://github.com/django/channels_redis Channels专属的通道层，使用Redis作为其后备存储，并支持单服务器和分片配置以及群组支持。（这个项目是 Channels 的一个附属项目，配置的时候作为可选项使用，该软件包的早期版本被称为 `asgi_redis`，如果你在使用 Channels 1.x项目，它仍可在PyPI下通过这个名称使用。但 `channels_redis` 仅适用于 Channels 2 项目。）

## WSGI

`Python Web Server Gateway Interface  `为python语言定义的Web服务器和Web应用框架之间的一种简单和通用的接口标准，是一种协议规范，部署的环境是基于HTTP, 或者 HTTP2的项目。

![image.png](https://i.loli.net/2020/06/30/NTgLJObcAM41yu8.png)

[根据WSGI实现一个简单的web框架](https://github.com/Panlq/Py-Project/tree/master/mini-web)

## uwsgi

是一种传输协议，用于定义传输信息的类型。用于在uWSGI服务器与其他网络服务器的数据通信如Nginx

## uWSGI

uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi协议、http协议 等协议，完全用C编写，效率高性能稳定， **只处理动态请求，不处理静态文件，静态文件一般交给Nginx来转发**

![image.png](https://i.loli.net/2020/06/30/yKh2WEvgHlncsGm.png)



![](https://img2020.cnblogs.com/blog/778496/202006/778496-20200630172800633-2080035416.png)

![](https://img2020.cnblogs.com/blog/778496/202006/778496-20200630172816965-1306516069.png)





### 了解服务端推送技术



![image.png](https://i.loli.net/2020/06/23/7QOkWVNlsxUT6Sd.png)

![image.png](https://i.loli.net/2020/06/23/7oGflrNBXnM8HbP.png)

| 方式               | 类型          | 技术实现                                                     | 优点                                                         | 缺点                                                         | 适用场景                                                     |
| ------------------ | ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| meta标签           | client→server | 通过配置meta标签让浏览器自动刷新                             | 使用方式简单，可以在JS禁用情况下使用                         | 不是实时更新数据，对服务器造成的压力大，带宽浪费多           | `<META HTTP-RQUIV="Refresh" CONTENT=12>`                     |
| 轮询Polling        | client→server | 利用 Javascript 中的 `setInterval` 或 `setTimeout` 在固定的時間內向 Server 端發起 Request 以 JSON 或 AJAX（xhr)的方式取得最新的資料 | 实现简单                                                     | 1、浪费带宽和服务器资源 2、 一次请求信息大半是无用（完整http头信息） 3、有延迟  4、大部分无效请求 | 适于小型应用                                                 |
| 长轮询Long-Polling | client→server | 服务器hold住连接，一直到有数据或者超时才返回，减少重复请求次数 | 1、实现简单 2、不会频繁发请求 3、节省流量 4、延迟低          | 1、服务器hold住连接，会消耗资源 2、一次请求信息大半是无用    | WebQQ、Hi网页版、Facebook IM                                 |
| 长连接iframe       | client→server | 在页面里嵌入一个隐蔵iframe，将这个 iframe 的 src 属性设为对一个长连接的请求，服务器端就能源源不断地往客户端输入数据。 | 1、数据实时送达 2、不发无用请求，一次链接，多次“推送”        | 1、服务器增加开销 2、无法准确知道连接状态 3、IE、chrome等一直会处于loading状态 | Gmail聊天                                                    |
| WebSocket          | server⇌client | new WebSocket()                                              | 1、支持双向通信，实时性更强 2、可发送二进制文件3、减少通信量4、並且在握手阶段（handshake)采用HTTP 协议，因此不容易被屏蔽 | 浏览器支持程度不一致                                         | 网络游戏、银行交互和支付，实时通讯，股票，数字货币价格信息等 |

#### 了解 Websocket 

> WebSocket是一种在单个TCP连接上进行[全双工](https://zh.wikipedia.org/wiki/全雙工)通讯的协议。WebSocket使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在WebSocket API中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建**持久性**的连接，并进行双向数据传输。本质上也是一个TCP长连接，建立在TCP协议之上。

![img](http://www.ruanyifeng.com/blogimg/asset/2017/bg2017051503.jpg)

**相关信息**

`101code: Switching Protocols`， 当发起ws请求的到时候，服务器响应浏览器的状态码是101， 表示根据Upgrade header转换协议

- 客户端请求

```shell
GET ws://127.0.0.1:8000/ws/.../ HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Host: example.com
Origin: http://example.com
Sec-WebSocket-Key: sN9cRrP/n9NdMgdcy2VJFQ==
Sec-WebSocket-Version: 13
```

- 服务端回应：

```shell
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: fFBooB7FAkLlXgRSz0BT3v4hq5s=
Sec-WebSocket-Location: ws://example.com/
```

#### 字段说明

- Connection必须设置Upgrade，表示客户端希望连接升级。
- Upgrade字段必须设置Websocket，表示希望升级到Websocket协议。
- Sec-WebSocket-Key是随机的字符串，服务器端会用这些数据来构造出一个SHA-1的信息摘要。把“Sec-WebSocket-Key”加上一个特殊字符串“258EAFA5-E914-47DA-95CA-C5AB0DC85B11”(websocket协议制定时用的一个UUID)，然后计算SHA-1摘要，之后进行BASE-64编码，将结果做为“Sec-WebSocket-Accept”头的值，返回给客户端。如此操作，可以尽量避免普通HTTP请求被误认为Websocket协议。
- [Sec-WebSocket-Accept](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Accept) 表示服务端接收客户端请求并建立websocket链接
- Sec-WebSocket-Version 表示支持的Websocket版本。RFC6455要求使用的版本是13，之前草案的版本均应当弃用。
- Origin字段是可选的，通常用来表示在浏览器中发起此Websocket连接所在的页面，类似于Referer。但是，与Referer不同的是，Origin只包含了协议和主机名称。
- 其他一些定义在HTTP协议中的字段，如Cookie等，也可以在Websocket中使用。

[服务端是如何主动推送信息到客户端的？ - 张铁蕾的回答 - 知乎]( https://www.zhihu.com/question/24938934/answer/86181898)

[Web 实时推送技术的总结](https://juejin.im/post/5c20e5766fb9a049b13e387b#heading-10)

[Comet：基于 HTTP 长连接的“服务器推”技术](https://www.ibm.com/developerworks/cn/web/wa-lo-comet/)

[獲得實時更新的方法（Polling, Comet, Long Polling, WebSocket）]([https://blog.niclin.tw/2017/10/28/%E7%8D%B2%E5%BE%97%E5%AF%A6%E6%99%82%E6%9B%B4%E6%96%B0%E7%9A%84%E6%96%B9%E6%B3%95polling-comet-long-polling-websocket/](https://blog.niclin.tw/2017/10/28/獲得實時更新的方法polling-comet-long-polling-websocket/))

[MQTT协议中文版](https://mcxiaoke.gitbooks.io/mqtt-cn/content/) **有时间要看一看**

## 参考资料

[WebSocket 教程-阮一峰](http://www.ruanyifeng.com/blog/2017/05/websocket.html)

[Django Channels](https://channels.readthedocs.io/en/latest/)

[WebSocket chatRoom with Django-Channels（一）](https://medium.com/@Sean_Hsu/websocket-chatroom-with-django-channels-f6c7bed7d2f4)