## 1. python 相关面试题 

```golang
class Parent(object):
    x = 1

class Child1(Parent):
    pass

class Child2(Parent):
    pass

print(Parent.x, Child1.x, Child2.x)
Child1.x = 2
print(Parent.x, Child1.x, Child2.x)
Parent.x = 3
print(Parent.x, Child1.x, Child2.x)
```

> python 中 类变量在内部是作为字典处理的。一个变量的名字没有在当前类的字典中发现，将搜索祖先类(如父类)直到直到被引用的变量名被找到（如果这个被引用的变量名既没有在自己所在的类又没有在祖先类中找到，会引发一个 AttributeError 异常 ）。

#### 1.生成三个随机的字典

```&#39;&#39;python
from random import randint, sample
s1 = {k: randint(1, 4) for k in sample('asdfsdfsdf', randint(3, 6))}
```

#### 2. 两个数组 组成字典

```python
key = [1, 2, 3]
value = [4, 5, 6]
res = dict(zip(key, value))
```

#### 3. 对某英文文章的单词，进行词频统计，找到出现次数最高的10个单词，统计出现次数

```python
"""
1)创建文件对象f后，解释f的readlines和xreadlines方法的区别？
    python2 的才有xreadlines 方法, 返回一个迭代器
    python3 中fileobj便是一个迭代器 _io.TextIOWrapper 
    readlines 返回列表

2)追加需求，引号内元素需要算作一个单词，如何实现？
    读取所有内容用 引号切分，偶数索引部分划分单词, 奇数部分则算作一个单词
用正则模块里的 re.split()函数，配合字符串的正则操作
"""
import re
from collections import Counter


def resplit(text, sep=r"[0-9\W]+"):
    return re.split(sep, text)


def get_hf_words(filename, num=10):
    with open(filename, encoding="utf-8") as f:
        content = f.read()
    res = resplit(content)  # 根据非单词字符分割, \w 匹配单词字符包括, 大小写字母,0-9和_下滑下
    c = Counter(res)  # 返回对应频度一个字典
    h = c.most_common(num)  # 返回的是列表，元素以元组的形式存在
    print(h)


def get_hf_words_spilt_quote(filename, num=10):
    """
    读取所有内容用 引号切分，偶数索引部分划分单词, 奇数部分则算作一个单词
    """
    words = []
    with open(filename, encoding="utf-8") as f:
        content = f.read()
    
    text_list = resplit(content, r'\s?\"\s?')
    length = len(text_list)
    for i in range(0, length, 2):
        words += resplit(text_list[i])
        if i + 1 < length:
            words.append(text_list[i + 1])
        
    c = Counter(words)
    result = c.most_common(num)
    print(result)
```

#### 4. python 正则表达式中的

- “.” Matches any character except a newline.

- re.S DOTALL “.” matches any character at all, including the newline.

- re.I ignorecase



#### 5. GIL的概念，以及对python多线程的影响，编写一个多线程抓取网页的程序，并阐明多线程抓取程序是否可比单线程性能有提升，并解释原因。

答：[Python3 源码阅读-深入了解Python GIL](https://www.cnblogs.com/panlq/p/13081161.html)

- python语言跟GIL没半毛钱关系，仅仅是由于历史原因在Cpython解释器(虚拟机)，难以移除GIL
- GIL： 全局解释器锁，每个线程在执行的过程都需要先获取GIL，保证同一时刻只有一个线程可以执行代码。
- 线程释放GIL锁的情况: 在IO操作等可能会引起阻塞的system call之前，可以暂时释放GIL,但在执行完毕后,必须重新获取GIL Python 3.x使用计时器（执行时间达到阈值后0.005秒，当前线程释放GIL）或Python 2.x，ticke计数达到100
- python使用多进程是可以利用多核的CPU资源的
- 多线程爬去比单线程性能有提升，因为遇到IO阻塞会自动释放GIL锁

  在处理类似科学计算，这类需要持续使用cpu密集型的任务市，单线程会比多线程快

  在处理类似IO操作等引起阻塞的任时，多线程比单线程快。



```python
# 一个简单的多线程爬虫demo
# coding=utf-8
import requests
import threading
from queue import Queue

class Spider(object):
    def __init__(self):
        self.html_queue = Queue()
        self.url_queue = Queue()
        self.content_data_queue = Queue()

    def gen_url(self):
        pass

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url)
            self.html_queue.put(reponse.content.decode('utf-8'))
            self.url_queue.task_done()

	def get_content_list(self):
        html_str = self.html_queue.get()
        "parse html"
        # parse_res = parse_data()
     	self.content_data_queue.put(parse_res)
        self.html_queue.task_done()
        
     def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.gen_url)
        thread_list.append(t_url)
        for i in range(3): # 启动三个线程
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        t_content = threading.Thread(target=self.get_content_list)
        thread_list.append(t_content)
        
        for t in thread_list:
            t.setDaemon(True)
            t.start()
            
        for q in [self.url_queue, self.html_queue, self.contetn_data_queue]:
            q.join()
            
if __name__ == "__main__":
    Spider().run()

```

#### 6. 删除序列中的空字符串

```python
a = ['A', '', 'B', None, 'C', ' ']
# filter()函数把传入的函数一次作用于每个元素，然后根据返回值是True 还是 False决定保留还是丢弃该元素
print(list(filter(lambda s : s and s.strip(), a)))
```

#### 7. 生成0-100素数

```python
class PrimeNum(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def isPrimeNum(self, k):
        if k < 2:
            return False
       	for i in range(2, k):
            if k % i == 0:
                return False
        return True
    
    def __iter__(self):
        for k in range(self.start, self.end + 1):
            if self.isPrimeNum(k):
                yield k
                
if __name__ == '__main__':
    for i in PrimeNum(1, 100):
        print(i, end=" ")
```

#### 8. 实现一个小数range函数/类

```python
from deecimal import Deciaml

class FloatRange(object):
    def __init__(self, start, end, step=0.1):
        self.start = start
        self.end = end
        self.step = step
        
    def __iter__(self):
        t = self.start
        while t <= self.end:
            yield t
            # 使用decimal, 提高浮点精度
            t = Decimal(str(self.step)) + Decimal(str(t))
            
    def __reversed__(self):
        t = self.end
        while t >= self.start:
            yield t
            t = Decimal(str(self.step)) - Decimal(str(t))
            
# 创建对象
for x in FloatRange(4.0, 8.0, 0.5):  # 小数至少得大于0.5，迭代出来的才会是0.5的步进
    print(x)
    
```

9. 定义函数findall，实现对字符串find方法的进一步封装，要求返回符合要求的所有位置的起始下标，如字符串"helloworldhellopythonhelloc++hellojava"，需要找出里面所有的"hello"的位置，最后将返回一个元组(0,10,21,29)，即将h的下标全部返回出来，而find方法只能返回第一个

```python
def findall(string, sub):
    ret = []
    index = 0
    while True:
        index = string.find(sub, index)
        if index != -1:
            ret.append(index)
            index += len(sub)
        else:
            break
    return tuple(ret)

print(findall("helloworldhellopythonhelloc++hellojava", "hello"))
```



#### 10. 函数默认参数设置为可变类型的问题

[Why are default values shared between objects?](https://docs.python.org/3/faq/programming.html?highlight=lambda#why-are-default-values-shared-between-objects)

```python
>>> def generate_new_list_with(my_list=[], element=None):
...     my_list.append(element)
...     return my_list
...
>>> list_1 = generate_new_list_with(element=1)
>>> list_1
[1]
>>> list_2 = generate_new_list_with(element=2)
>>> list_2
[1, 2]
```

> Python函数的参数默认值，是在编译阶段就绑定的，之后所有的函数调用时，如果参数不显示的给予赋值，那么所谓的参数默认值不过是一个指向那个在`compile`阶段就已经存在的对象的指针。如果调用函数时，没有显示指定传入参数值得话。

**为什么要这么设计？**：出于Python编译器的实现方式考虑，函数是一个内部一级对象。而参数默认值是这个对象的属性。在其他任何语言中，对象属性都是在对象创建时做绑定的。因此，函数参数默认值在编译时绑定也就不足为奇了。

参考:[Python函数参数默认值的陷阱](http://cenalulu.github.io/python/default-mutable-arguments/)





[python中的None和空字符比较](https://www.jianshu.com/p/627232777efd)

None是python中的一个特殊的常量，表示一个空的对象，空值是python中的一个特殊值。数据为空并不代表是空对象，例如[],''等都不是None。None和任何对象比较返回值都是False，除了自己。

因为None在Python里是个单例对象，一个变量如果是None，它一定和None指向同一个内存地址。



### 经典面试题集结：

[stackoverflow-py-top-qa python top问题](https://github.com/wklken/stackoverflow-py-top-qa)

[TCP为什么是三次握手，而不是两次或者四次？](https://www.zhihu.com/question/24853633)

[Nginx面试题（总结最全面的面试题！！！）](https://juejin.im/post/5e941ec4e51d45471263ef32)