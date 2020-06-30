浏览器请求动态页面过程
![image.png](https://i.loli.net/2020/06/30/NTgLJObcAM41yu8.png)

## WSGI
允许开发者将选择web框架和web服务器分开。可以混合匹配web服务器和web框架，选择一个适合的配对
比如,可以在Gunicorn 或者 Nginx/uWSGI 或者 Waitress上运行 Django, Flask, 或 Pyramid。真正的混合匹配，得益于WSGI同时支持服务器和架构

![image.png](https://i.loli.net/2020/06/30/VMhpicYJEwFaHk2.png)

## 定义WSGI接口
WSGI接口定义非常简单，它只要求Web开发者实现一个函数，就可以响应HTTP请求。我们来看一个最简单的Web版本的“Hello World!”：
```python
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return 'Hello World!'
```

```python
from wsgiref.simple_server import make_server
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']
if __name__ == '__main__':
    httpd = make_server('', 9999, application)
    print("Serving HTTP on port 9999...")
    httpd.serve_forever()
```

上面的application()函数就是符合WSGI标准的一个HTTP处理函数，它接收两个参数：

- environ：一个包含所有HTTP请求信息的dict对象；
- start_response：一个发送HTTP响应的函数。
整个application()函数本身没有涉及到任何解析HTTP的部分，也就是说，把底层web服务器解析部分和应用程序逻辑部分进行了分离，这样开发者就可以专心做一个领域了

application()函数必须由WSGI服务器来调用。有很多符合WSGI规范的服务器


## 参考
[wsgiref](https://docs.python.org/3.7/library/wsgiref.html)
[WSGI协议的原理及实现](https://geocld.github.io/2017/08/14/wsgi/)