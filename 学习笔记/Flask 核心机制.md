# Flask 上下文机制和线程隔离

> **1. 计算机科学领域的任何问题都可以通过增加一个间接的中间层来解决**， 上下文机制就是这句话的体现。
>
> **2. 如果一次封装解决不了问题，那就再来一次**

上下文：相当于一个容器，保存了Flask程序运行过程中的一些信息 源码：[flask/ctx.py](https://github.com/pallets/flask/blob/master/src/flask/ctx.py)

- 请求上下文：Flask从客户端收到请求时，要让视图函数能访问一些对象，这样才能处理请求，要想让视图函数能够访问请求对象，一个显而易见的方式是将其作为参数传入视图函数，不过这会导致程序中的每个视图函数都增加一个参数，除了访问请求对象,如果视图函数在处理请求时还要访问其他对象，情况会变得更糟。为了避免大量可有可无的参数把视图函数弄得一团糟，Flask使用上下文临时把某些对象变为全局可访问。**这就是一种重构设计思路**。
  - **request** 封装了HTTP请求的内容，针对http请求，也是一种符合WSGI接口规范的设计（**关于WSGI可参考我对该协议的理解和实现demo [mini-wsgi-web](https://github.com/Panlq/Py-Project/tree/master/mini-web)**），如 `request.args.get('user')`
  - **session** 用来记录请求会话中的信息，针对的是用户信息，如 `session['name'] = user.id`

- 应用上下文：应用程序上下文,用于存储应用程序中的变量
  - **current_app** 存储应用配置，数据库连接等应用相关信息
  - **g变量** 作为flask程序全局的一个**临时变量**, 充当者中间媒介的作用,我们可以通过它传递一些数据，g保存的是当前请求的全局变量，**不同的请求会有不同的全局变量，通过不同的thread id区别**

```python
# context locals
# 使用代理模式 LocalProxy
_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))
```

## 1. working outside application context

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from flask import Flask, current_app

app = Flask(__name__)
a = current_app
# is_debug = current_app.config['DEBUG']

@app.route('/')
def index():
    return '<h1>Hello World. Have a nice day! </1>'


if __name__ == '__main__':
    app.run(host='localhost', port=8888)
```

> 报错:
>
> Exception has occurred: RuntimeError
>
> Working outside of application context.

![](https://img2020.cnblogs.com/blog/778496/202007/778496-20200708133619522-1637712399.png)

## 2. flask 上下文出入栈

**flask上下文对象出入栈模型图**

![flask上下文对象出入栈模型图](https://img2020.cnblogs.com/blog/778496/202007/778496-20200708154936922-1740856449.png)



**在应用开发中可用直接引用`current_app`不会报错，是因为当在一个请求中使用的时候，flask会判断`_app_ctx_stack`栈顶是否有可用对象，如果没有就会自动推入一个App**. 我们获取的`current_app`就是获取的栈顶元素

```python
# flask/globals.py

def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app

current_app = LocalProxy(_find_app)
```

修改代码：将app对象推入栈顶

```python
# ...
# 将app_context 推入栈中
ctx = app.app_context()
ctx.push()
a = current_app

is_debug = current_app.config['DEBUG']
ctx.pop()
# ...

# 更有pythonnic的写法
# 将app_context 推入栈中
# with app.app_context():
#     a = current_app
#     is_debug = current_app.config['DEBUG']
```

![](https://img2020.cnblogs.com/blog/778496/202007/778496-20200708155134961-419020986.png)

不在出现`unbound`状态。可正常运行

既然flask会自动帮我们检测栈顶元素是否存在，为什么我们还要做这一步操作，**当我们在写离线应用，或者单元测试的时候就需要用到，因为请求是模拟的，不是在application context中的了。**

## 3. python中的上文管理器

1. **实现了`__enter__`和`__exit__`方法的对象就是一个上文管理器。**

```python
class MyResource:
    def __enter__(self):
        print('connect ro resource')
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connection')
        # return True
        # return False
    
    def query(self):
        print('query data')


try:
    with MyResource() as r:
        1/0
        r.query()
except Exception as e:
    print(e)
```

`with MyResour ce() as r` as 的别名r指向的不是上想问管理器对象，而是`__enter__`方法返回的值，在以上代码确实是返回了对象本身。

`__exit__` 方法 处理退出上下文管理器对象时的一些资源清理工作，并处理异常，三个参数

- exc_type   异常类型
- exc_value  异常原因解释
- tb               traceback 

**`__exit__`其实是有返回值的，`return True`表示，异常信息已经在本方法中处理，外部可不接收异常，`return False` 表示将异常抛出给上层逻辑处理，默认不写返回，即默认值是`None`,  `None`也表示`False`**

2. **另一种实现上下文管理器的方法是`contextmanager` 装饰器**

使用 `contextmanager `的装饰器，可以简化上下文管理器的实现方式。原理是通过 `yield` 将函数分割成两部分，`yield` 之前的语句在`__enter__` 方法中执行，`yield` 之后的语句在`__exit__` 方法中执行。紧跟在 `yield` 后面的值是函数的返回值。

```python

from contextlib import contextmanager


class MyResource:
    
    def query(self):
        print('query data')


@contextmanager
def my_resource():
    print('connect ro resource')
    yield MyResource()
    print('close resource connection')


try:
    with my_resource() as r:
        r.query()
except Exception as e:
    print(e)
```

两种方法并没有说哪一种方法好，各有优略，看代码环境的使用场景来决定。`contextmanager`

以下就是一个简单的需求，给文字加书名号。

```python
@contextmanager
def book_mark():
    print('《', end='')
    yield 
    print('》', end='')


with book_mark():
    print('你还年轻? peer已经年少有为!', end='')
```

**实际应用场景**，封装一些公用方法。

原本业务逻辑中是这样的, 在所有的模型类中，在新建资源的时候都需要`add`， `commit`, 或者`rollback`的操作。

```python
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        try:
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            db.session.add(gift)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
```

简化后

```python
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            db.session.add(gift)
```

其中数据库的封装如下

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


# 抽离公用代码，with 形式来完成db.commit  rollback
class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)
```

## 线程隔离机制

![](https://i.imgur.com/uU5G6SY.png)

**如何实现一个Reqeust 指向多个请求实例，且要区分该实例对象所绑定的用户？**

字典: 

> request = {'key1': val1, 'key2': val2}Local

flask引用 `werkzeug` 中的 `local.Local` 实现线程隔离

### Local

```python
# werkzeug\local.py
class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        object.__setattr__(self, '__storage__', {})
        object.__setattr__(self, '__ident_func__', get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # 获取当前线程的id
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
```

可以看到是使用线程ID来绑定不同的上线文对象。

### LocalStack

```python
class LocalStack(object):

    """This class works similar to a :class:`Local` but keeps a stack
    of objects instead.  This is best explained with an example::

        >>> ls = LocalStack()
        >>> ls.push(42)
        >>> ls.top
        42
        >>> ls.push(23)
        >>> ls.top
        23
        >>> ls.pop()
        23
        >>> ls.top
        42

    They can be force released by using a :class:`LocalManager` or with
    the :func:`release_local` function but the correct way is to pop the
    item from the stack after using.  When the stack is empty it will
    no longer be bound to the current context (and as such released).

    By calling the stack without arguments it returns a proxy that resolves to
    the topmost item on the stack.

    .. versionadded:: 0.6.1
    """

    def __init__(self):
        self._local = Local()

    def __release_local__(self):
        self._local.__release_local__()

    def _get__ident_func__(self):
        return self._local.__ident_func__

    def _set__ident_func__(self, value):
        object.__setattr__(self._local, '__ident_func__', value)
    __ident_func__ = property(_get__ident_func__, _set__ident_func__)
    del _get__ident_func__, _set__ident_func__

    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError('object unbound')
            return rv
        return LocalProxy(_lookup)

    def push(self, obj):
        """Pushes a new item to the stack"""
        rv = getattr(self._local, 'stack', None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(obj)
        return rv

    def pop(self):
        """Removes the topmost item from the stack, will return the
        old value or `None` if the stack was already empty.
        """
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return None
        elif len(stack) == 1:
            release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()

    @property
    def top(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None
```

> Local使用字典的方式实现线程隔离，LocalStack 则封装Local实现了线程隔离的栈结构

## 总结

1. flask上下文的实现使用了设计模式中的代理模式，`current_app`, `requsts`, 等代理对象都是线程隔离的, 当我们启动一个线程去执行一个异步操作需要用到应用上下文时(需传入`app`对象), 如果传入`current_app`, 此时的`app` 时` unbond`的状态, 由于线程id改变了, 所以在新的线程中 所有的栈都是空的, 但是在整个`web`中 由Flask 实例化的 `app`是唯一的, 所以获取app传入是可以的  `app = current_app._get_current_object()`
2. 线程隔离的实现机制就是利用线程ID+字典， 使用线程隔离的意义在于：使当前线程能够正确引用到他自己所创建的对象，而不是引用到其他线程所创建的对象
4. `current_app  -> (LocalStack.top = AppContext top.app = Flask)`
5. `request  ->  (LocalStack.top = RequestContext.top.request = Request)`

## 参考资料

[Python Flask高级编程-七月](https://coding.imooc.com/class/194.html)