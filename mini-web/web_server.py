#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

import re
import sys
import time
import select
import socket
import io
import multiprocessing


class WSGIServer(object):

    def __init__(self, port, documents_root, app):
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server_socket.setblocking(False)
        self.server_socket.bind(('', port))
        self.server_socket.listen(128)

        # Get server host name and port
        host, port = self.server_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        self.request_method = None  # GET
        self.path = None           # /hello
        self.request_version = None  # HTTP/1.1

        # 指定资源文件的路径
        self.documents_root = documents_root

        # 指定web框架调用的函数对象
        self.app = app
    
    def run_forever(self):
        """run server"""
        while True:
            new_sock, new_addr = self.server_socket.accept()
            new_sock.settimeout(3)
            new_process = multiprocessing.Process(target=self.dispatch_request, args=(new_sock, ))
            new_process.start()
            new_sock.close()

    def get_environ(self):
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def parse_request(self, context):
        request_line = context.splitlines()[0]  # 获取起始行
        #GET /a/b/c/d/index.html HTTP1.1
        ret = re.match(r'([^/]*)([^ ]+)(.*[^\r\n])', request_line)
        if ret:
            # request_line = request_line.rstrip('\r\n')
            (self.request_method,  # GET
            self.path,            # /hello
            self.request_version  # HTTP/1.1
            ) = ret.groups()

        
    def dispatch_request(self, client_sock):
        """tcp长连接"""
        while True:
            request = None
            try:
                request = client_sock.recv(1024).decode('utf-8')
            except BlockingIOError:
                # print('-->', ret)
                pass

            # 浏览器关闭连接            
            if not request:
                client_sock.close()
                return

            self.request_data = request
            self.parse_request(request)
            if self.path == '/':
                self.path = '/index.html'

            if not self.path.endswith('.py'):
                try:
                    f = open(self.documents_root+self.path, 'rb')
                except Exception as e:
                    response_body = 'file nt found, please make sure the right uri'
                    response_header = 'HTTP/1.1 404 not found\r\n'
                    response_header += 'Content-Type:text/html;charset=utf-8\r\n'
                    response_header += f'Content-Length: {len(response_body)}\r\n'
                    response_header += '\r\n'

                    response = response_header + response_body

                    # 将header返回给浏览
                    client_sock.send(response.encode('utf-8'))

                else:
                    content = f.read()
                    f.close()

                    response_body = content
                    response_header = 'HTTP/1.1 200 OK\r\n'
                    response_header += 'Content-Type:text/html;charset=utf-8\r\n'
                    response_header += f'Content-Length: {len(response_body)}\r\n'
                    response_header += '\r\n'
                    # 将header返回给浏览器
                    client_sock.send(response_header.encode('utf-8') + response_body)
            # 以.py结尾的文件，模拟是浏览需要动态的页面
            else:
                
                env = self.get_environ()
                response_body = self.app(env, self.set_response_headers)

                response_header = "HTTP/1.1 {status}\r\n".format(status=self.headers[0])
                response_header += "Content-Type: text/html; charset=utf-8\r\n"
                response_header += "Content-Length: %d\r\n" % len(response_body)
                for temp_head in self.headers[1]:
                    response_header += "{0}:{1}\r\n".format(*temp_head)

                response = response_header + "\r\n"
                response += response_body
                client_sock.send(response.encode('utf-8'))

    def set_response_headers(self, status, headers):
        """该方法会被web框架默认调用"""
        response_header_default = [
            ("Data", time.ctime()),
            ("Server", "python mini web server")
        ]
        
        self.headers = [status, response_header_default + headers]

        
g_static_docment_root = './static'
g_dynamic_document_root = './web'


def main():
    # # eg: python xx.py 5000
    # if len(sys.argv) == 3:
    #     port = sys.argv[1]
    #     if port.isdigit():
    #         port = int(port)
        
    #     # 获取web服务器需要动态资源时，访问的web框架名字
    #     web_frame_module_app_name = sys.argv[2]
    # else:
    #     print("运行方式如: python3 xxx.py 7890 my_web_frame_name:application")
    #     return


    # print("http服务器使用的port:%s" % port)

    # # 将动态路径即存放py文件的路径，添加到path中，这样python就能够找到这个路径了
    # sys.path.append(g_dynamic_document_root)

    # ret = re.match(r"([^:]*):(.*)", web_frame_module_app_name)
    # if ret:
    #     # 获取模块名
    #     web_frame_module_name = ret.group(1)
    #     # 获取可以调用web框架的应用名称
    #     app_name = ret.group(2)

    # # 导入web框架的主模块
    # web_frame_module = __import__(web_frame_module_name)
    # # 获取可调用的函数对象
    # app = getattr(web_frame_module, app_name)
    from web.demo_web import application

    http_server = WSGIServer(8888, g_static_docment_root, application)
    http_server.run_forever()


if __name__ == '__main__':
    main()