
## 背景
[hug:How to stream upload a file using multipart/form-data](https://github.com/hugapi/hug/issues/474)

windows环境, 使用hug框架, 做上传文件的功能, 获取文件名称和文件对象


## 问题描述
1. 使用 https://github.com/yohanboniface/falcon-multipart
windows环境下, 上传文件读取数据时, 由于EOL差异会导致无响应
```python
# cgi.parse_multipart
# Read lines until end of part.
def parse_multipart(fp, pdict):
    """Parse multipart input.
    """
    #...
    lines = []
    while 1:
        line = fp.readline()   # windows读取bytesIO时会卡在这里
        if not line:
            terminator = lastpart # End outer loop
            break
        if line.startswith(b"--"):
            terminator = line.rstrip()
            if terminator in (nextpart, lastpart):
                break
        lines.append(line)
    # Done with part.
    #...
```

> cgi module cannot handle POST with multipart/form-data in 3.x https://bugs.python.org/issue4953  

> linux EOL is "\n", windows is "\r\n" so cgi.FieldStorage in windows has a problem
the multipart parser adapted it!

```python

def _lineiter(self):
    # ...
    for line in lines:
        if line.endswith(b"\r\n"):
            yield line[:-2], b"\r\n"
        elif line.endswith(b"\n"):
            yield line[:-1], b"\n"
        elif line.endswith(b"\r"):
            yield line[:-1], b"\r"
        else:
            yield line, b""
    # ...
```

## 解决方案
1. 在linux环境中跑服务(eg: app2.py) [falcon-multipart](https://github.com/yohanboniface/falcon-multipart)
2. 替换multipart-form-data 工具(eg: app.py) [multipart](https://github.com/defnull/multipart)


## test

```bash

curl -v -H "Content-Type: multipart/form-data" \
            -F "foo=hellohello" \
            -F "bar=0123456789" \
            -F "upload_file=@example_file" \
            -X POST ${url}/upload

```