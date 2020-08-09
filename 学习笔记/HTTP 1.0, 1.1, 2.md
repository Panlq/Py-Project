## HTTP协议

HTTP（超文本传输协议，HyperText Transfer Protocol)是互联网上应用最为广泛的一种网络协议。所有的WWW文件都必须遵守这个标准。设计HTTP最初的目的是为了提供一种发布和接收HTML页面的方法。HTTP协议和TCP协议是不冲突的，HTTP定义在七层协议中的应用层，TCP解决的是传输层的逻辑。HTTP使用TCP而不是UDP的原因在于（打开）一个网页必须传送很多数据，而TCP协议提供传输控制，按顺序组织数据，和错误纠正。HTTP协议的瓶颈及其优化技巧都是基于TCP协议本身的特性。如TCP建立连接时三次握手有1.5个RTT（round-trip time）的延迟，为了避免每次请求的都经历握手带来的延迟，应用层会选择不同策略的http长链接方案。又如TCP在建立连接的初期有慢启动（slow start）的特性，所以连接的重用总是比新建连接性能要好



## HTTP 0.9 / 1.0



0.9和1.0这两个版本，就是最传统的 request – response的模式了，HTTP 0.9版本的协议简单到极点，请求时，不支持请求头，只支持 `GET` 方法，没了。HTTP 1.0 扩展了0.9版，其中主要增加了几个变化：

- 在请求中加入了HTTP版本号，如：`GET /coolshell/index.html HTTP/1.0`
- HTTP 开始有 header了，不管是request还是response 都有header了。
- 增加了HTTP Status Code 标识相关的状态码。
- 还有 `Content-Type` 可以传输其它的文件了。



我们可以看到，HTTP 1.0 开始让这个协议变得很文明了，一种工程文明。因为：

- 一个协议有没有版本管理，是一个工程化的象征。
- header是协议可以说是把元数据和业务数据解耦，也可以说是控制逻辑和业务逻辑的分离。
- Status Code 的出现可以让请求双方以及第三方的监控或管理程序有了统一的认识。最关键是还是控制错误和业务错误的分离。

但是，HTTP1.0性能上有一个很大的问题，那就是每请求一个资源都要新建一个TCP链接，而且是串行请求，所以，就算网络变快了，打开网页的速度也还是很慢。所以，HTTP 1.0 应该是一个必需要淘汰的协议了。

## HTTP/1.1

HTTP/1.1 主要解决了HTTP 1.0的网络性能的问题，以及增加了一些新的东西：

- 可以设置keepalive让HTTP重用TCP链接，重用TCP链接可以省了每次请求都要在广域网上进行的TCP的三次握手的巨大开销，所谓的‘HTTP长连接’ 或是 ‘请求响应式的HTTP持久链接’ 。HTTP Persistent connection

- 然后支持pipeline网络传输，只要第一个请求发出去了，不必等其回来，就可以发第二个请求，可以减少整体的响应时间，（注：非幂等的POST 方法或是有依赖的请求是不能被pipeline化的）

- 支持 Chunked Responses 也就是说，在Response的时候，不必说明 `Content-Length`这样，客户端就不能断开链接，知道收到服务端的EOF标识。这种技术又叫**“服务端Push模型”**， 或是 “**服务端Push式的HTTP持久链接**”

- 增加了cache control 机制

- 协议头注增加了Language, Encoding, Type等头部，让客户端可以跟服务器进行更多的协商

- 正式的加入了一个很重要的头--  HOST， 这样的话，服务器就知道你要请求那个网站，因为可以有多个域名解析到同一个IP上，要区分用户是请求的哪个域名，就需要在HTTP的协议中加入域名的信息，而不是被DNS转换过的IP信息。

- 正式加入 `OPTIONS`方法，其主要用于 [CORS – Cross Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) 应用

- 断点续传 <code>RANGE: bytes</code> http1.0每次传送文件都是从文件头开始的，即0字节处开始

  <code>RANGE:bytes=XXXX</code> 表示要求服务器从文件xxx字节处开始传送。响应返回状态码是 206（Partial Content）

HTTP/1.1应该分成两个时代，一个是2014年前，一个是2014年后，因为2014年HTTP/1.1有了一组RFC（[7230](https://tools.ietf.org/html/rfc7230) /[7231](https://tools.ietf.org/html/rfc7231)/[7232](https://tools.ietf.org/html/rfc7232)/[7233](https://tools.ietf.org/html/rfc7233)/[7234](https://tools.ietf.org/html/rfc7234)/[7235](https://tools.ietf.org/html/rfc7235)），这组RFC又叫“HTTP/2 预览版”。其中影响HTTP发展的是两个大的需求：

- 一个需要是加大了HTTP的安全性，这样就可以让HTTP应用得广泛，比如，使用TLS协议。
- 另一个是让HTTP可以支持更多的应用，在HTTP/1.1 下，HTTP已经支持四种网络协议：
  - 传统的短链接。
  - 可重用TCP的的长链接模型。
  - 服务端push的模型。
  - WebSocket模型。

## HTTP/2.0

![HTTP/2](http://hengyunabc.github.io/img/http2.svg)

虽然 HTTP/1.1 已经开始变成应用层通讯协议的一等公民了，但是还是有性能问题，虽然HTTP/1.1 可以重用TCP链接，但是请求还是一个一个串行发的，需要保证其顺序。然而，大量的网页请求中都是些资源类的东西，这些东西占了整个HTTP请求中最多的传输数据量。所以，理论上来说，如果能够并行这些请求，那就会增加更大的网络吞吐和性能。

另外，HTTP/1.1传输数据时，是以文本的方式，借助耗CPU的zip压缩的方式减少网络带宽，但是耗了前端和后端的CPU。这也是为什么很多RPC协议诟病HTTP的一个原因，就是数据传输的成本比较大。

其实，在2010年时，Google 就在搞一个实验型的协议，这个协议叫[SPDY](https://en.wikipedia.org/wiki/SPDY)，这个协议成为了HTTP/2的基础（也可以说成HTTP/2就是SPDY的复刻）。HTTP/2基本上解决了之前的这些性能问题，其和HTTP/1.1最主要的不同是：

- HTTP/2是一个二进制协议，增加了数据传输的效率
- HTTP/2是可以在一个TCP链接中并发请求多个HTTP请求，移除了HTTP/1.1中的串行请求。
- HTTP/2会压缩头，如果你同时发出多个请求，他们的头是一样的或是相似的，那么，协议会帮你消除重复的部分。这就是 HPAK 算法（参看[RFC 7541](https://tools.ietf.org/html/rfc7541) 附录A）
- HTTP/2允许服务端在客户端放cache, 又叫服务端push，也就是说，你没有请求的东西，服务端可以先发送给你放在你的本地缓存中，比如，你请求X，我服务端知道X依赖于Y，虽然你没有的请求Y，但我把把Y跟着X的请求一起返回客户端。

对于这些性能上的改善，在Medium上有篇文章你可看一下相关的细节说明和测试“[HTTP/2: the difference between HTTP/1.1, benefits and how to use it](https://medium.com/@factoryhr/http-2-the-difference-between-http-1-1-benefits-and-how-to-use-it-38094fa0e95b)”

## HTTP请求方法一览

| 方法    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| GET     | GET请求会显示请求指定的资源。一般来说GET方法应该只用于数据的读取，而不应当用于会产生副作用的非幂等的操作中。它期望的应该是而且应该是安全的和幂等的。这里的安全指的是，请求不会影响到资源的状态。 |
| HEAD    | HEAD方法与GET方法一样，都是向服务器发出指定资源的请求。但是，服务器在响应HEAD请求时不会回传资源的内容部分，即：响应主体。这样，我们可以不传输全部内容的情况下，就可以获取服务器的响应头信息。HEAD方法常被用于客户端查看服务器的性能。 |
| POST    | POST请求会 向指定资源提交数据，请求服务器进行处理，如：表单数据提交、文件上传等，请求数据会被包含在请求体中。POST方法是非幂等的方法，因为这个请求可能会创建新的资源或/和修改现有资源。 |
| PUT     | PUT请求会身向指定资源位置上传其最新内容，PUT方法是幂等的方法。通过该方法客户端可以将指定资源的最新数据传送给服务器取代指定的资源的内容。 |
| DELETE  | DELETE请求用于请求服务器删除所请求URI（统一资源标识符，Uniform Resource Identifier）所标识的资源。DELETE请求后指定资源会被删除，DELETE方法也是幂等的。 |
| CONNECT | CONNECT方法是HTTP/1.1协议预留的，能够将连接改为管道方式的代理服务器。通常用于SSL加密服务器的链接与非加密的HTTP代理服务器的通信。 |
| OPTIONS | OPTIONS请求与HEAD类似，一般也是用于客户端查看服务器的性能。 这个方法会请求服务器返回该资源所支持的所有HTTP请求方法，该方法会用'*'来代替资源名称，向服务器发送OPTIONS请求，可以测试服务器功能是否正常。JavaScript的XMLHttpRequest对象进行CORS跨域资源共享时，就是使用OPTIONS方法发送嗅探请求，以判断是否有对指定资源的访问权限。 |
| TRACE   | TRACE请求服务器回显其收到的请求信息，该方法主要用于HTTP请求的测试或诊断。 |
| PATCH   | PATCH方法出现的较晚，它在2010年的RFC 5789标准中被定义。PATCH请求与PUT请求类似，同样用于资源的更新。二者有以下两点不同：1.PATCH一般用于资源的部分更新，而PUT一般用于资源的整体更新。2.当资源不存在时，PATCH会创建一个新的资源，而PUT只会对已在资源进行更新。 |

名词解释： 幂等：对同一个系统，使用同样的条件，一次请求和重复的多次请求对系统资源的影响是一致的。

- GET 可提交的数据量受到URL长度的限制，HTTP 协议规范没有对 URL 长度进行限制。这个限制是特定的浏览器及服务器对它的限制。
- 理论上讲，POST 是没有大小限制的，HTTP 协议规范也没有进行大小限制，出于安全考虑，服务器软件在实现时会做一定限制。



# [HTTP 响应代码](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)

# HTTP消息头（HTTP headers）![img](https://mmbiz.qpic.cn/mmbiz_png/J0g14CUwaZdCwxNydn5YuT0s7aLuqWCvCl3iaCJeUV6Oa8zESpNKPDicgibjwANs465zibfWwwUQlMZsjciaNicO1Vwg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### OAuth2.0

几个关键的名字

（1） **Third-party application**：第三方应用程序，本文中又称"客户端"（client），即上一节例子中的"云冲印"。

（2）**HTTP service**：HTTP服务提供商，本文中简称"服务提供商"，即上一节例子中的Google。

（3）**Resource Owner**：资源所有者，本文中又称"用户"（user）。

（4）**User Agent**：用户代理，本文中就是指浏览器。

（5）**Authorization server**：认证服务器，即服务提供商专门用来处理认证的服务器。

（6）**Resource server**：资源服务器，即服务提供商存放用户生成的资源的服务器。它与认证服务器，可以是同一台服务器，也可以是不同的服务器。

#### OAuth的思路

OAuth在"客户端"与"服务提供商"之间，设置了一个授权层（authorization layer）。"客户端"不能直接登录"服务提供商"，只能登录授权层，以此将用户与客户端区分开来。"客户端"登录授权层所用的令牌（token），与用户的密码不同。用户可以在登录的时候，指定授权层令牌的权限范围和有效期。

"客户端"登录授权层以后，"服务提供商"根据令牌的权限范围和有效期，向"客户端"开放用户储存的资料。

#### 运行流程

![OAuth运行流程](https://www.ruanyifeng.com/blogimg/asset/2014/bg2014051203.png)

（A）用户打开客户端以后，客户端要求用户给予授权。

（B）用户同意给予客户端授权。

（C）客户端使用上一步获得的授权，向认证服务器申请令牌。

（D）认证服务器对客户端进行认证以后，确认无误，同意发放令牌。

（E）客户端使用令牌，向资源服务器申请获取资源。

（F）资源服务器确认令牌无误，同意向客户端开放资源。

#### 客户端的授权模式

客户端必须得到用户的授权（authorization grant），才能获得令牌（access token）。OAuth 2.0定义了四种授权方式。

- 授权码模式（authorization code）
- 简化模式（implicit）
- 密码模式（resource owner password credentials）
- 客户端模式（client credentials）

#### 授权码模式

授权码模式（authorization code）是功能最完整、流程最严密的授权模式。它的特点就是通过客户端的后台服务器，与"服务提供商"的认证服务器进行互动。

![授权码模式](https://www.ruanyifeng.com/blogimg/asset/2014/bg2014051204.png)

（A）用户访问客户端，后者将前者导向认证服务器。

（B）用户选择是否给予客户端授权。

（C）假设用户给予授权，认证服务器将用户导向客户端事先指定的"重定向URI"（redirection URI），同时附上一个授权码。

（D）客户端收到授权码，附上早先的"重定向URI"，向认证服务器申请令牌。这一步是在客户端的后台的服务器上完成的，对用户不可见。

（E）认证服务器核对了授权码和重定向URI，确认无误后，向客户端发送访问令牌（access token）和更新令牌（refresh token）。

转自[阮一峰老师-理解OAuth 2.0](https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)

[阮一峰老师-OAuth 2.0 的一个简单解释](http://www.ruanyifeng.com/blog/2019/04/oauth_design.html)

### 参考：

1. [HTTP/2 相比 1.0 有哪些重大改进？](https://www.zhihu.com/question/34074946)
2. [HTTP/2 对现在的网页访问，有什么大的优化呢？体现在什么地方？ - Leo Zhang的回答 - 知乎]( https://www.zhihu.com/question/24774343/answer/96586977)
3. [既然有http 请求，为什么还要用rpc调用？](https://link.jianshu.com/?t=https%3A%2F%2Fwww.zhihu.com%2Fquestion%2F41609070)
4. [HTTP,HTTP2.0,SPDY,HTTPS你应该知道的一些事](https://link.jianshu.com/?t=http%3A%2F%2Fwww.alloyteam.com%2F2016%2F07%2Fhttphttp2-0spdyhttps-reading-this-is-enough%2F)
5. [HTTP的前世今生-左耳朵耗子](https://coolshell.cn/articles/19840.html)
6. [HTTP1.0、HTTP1.1 和 HTTP2.0 的区别](https://juejin.im/entry/5981c5df518825359a2b9476)
7. [如何优雅的谈论HTTP／1.0／1.1／2.0](https://www.jianshu.com/p/52d86558ca57)
8. [http 和 https 有何区别？如何灵活使用？ - 程序员cxuan的回答 - 知乎 ](https://www.zhihu.com/question/19577317/answer/1157658840)