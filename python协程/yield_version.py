__doc__ = '如何使用yield完成协程（简化版的asyncio）'

import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = False
host = '127.0.0.1' ## 自建一个简单服务,模拟一个设置每个请求需要等待1s才返回结果
port = 5000
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

# 在单线程内做协作式时多任务调度
# 要异步，必回调
# 为了避免地狱式回调,将回调一拆为三,回调链变成了Future-Task-Coroutine
# 

class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:
    def __init__(self, coro):
        self.coro = coro   # Crawler(url).fetch()
        f = Future()
        self.step(f)

    def step(self, future):
        try:
            next_f = self.coro.send(future.result)
        except StopIteration:
            return 
        next_f.add_done_callback(self.step)


# Coroutine yield 实现的协程
class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect((host, port))
        except BlockingIOError:
            pass
        f = Future()


        def on_connected():
            f.set_result(None)
        
        selector.register(sock.fileno(), EVENT_WRITE, on_connected) # 连接io写事件
        yield f # 注册完就yield出去，等待时间触发
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)  # self.url 区分每个协程
        sock.send(get.encode('ascii'))

        global stopped
        while True:
            f = Future()
            def on_readable():f.set_result(sock.recv(4096)) # 可读的情况下,读取4096个bytes暂存给Future,执行回调,使生成器继续执行下去

            selector.register(sock.fileno(), EVENT_READ, on_readable) # # io读事件
            chunk = yield f # # 返回f,并接受step中send进来的future.result值,也就是暂存的请求返回字符
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break

        print("result:", self.response)

    
def loop():
    while not stopped:
        events = selector.select()
        for event_key, _ in events: # # 监听事件,触发回调,推动协程运行下去
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())

    loop()
    end = time.time()
    print(end - start)

