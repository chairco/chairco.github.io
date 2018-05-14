---
Title: Python inspect 實用功能與一級函式 First-class function
Slug: Python useful module inspect and first class function
Date: 2017-09-26 20:17:31
Modified: 2017-09-26 20:17:31
Tags: Python, Inspect
Category: Python
---

![#](https://www.python.org/static/img/python-logo@2x.png)
## 起因

因為試著使用 Python 內的 **inspect module**， 發現可以透過 `inspect.signature` 來檢查 function 型態，下面是一個範例((引自 Louie blog))，用來檢查計算最大公因數時限制輸入的數字要為 `int` 形態。

```shell
>>> from functools import wraps
>>> def checked(func):
...     ann = func.__annotations__
...     sig = inspect.signature(func)
...     @wraps(func)
...     def wrapper(*args, **kwargs):
...         bound = sig.bind(*args, **kwargs)
...         for name, val in bound.arguments.items():
...             if name in ann:
...                 assert isinstance(val, ann[name]), \
...                     f'Expected {ann[name]}'
...         return func(*args, **kwargs)
...     return wrapper
... 
>>> @checked
... def gcd(a: int, b: int) -> int:
...     while b:
...         a, b = b, a % b
...     return a
... 
>>> gcd(2.7, 3.6)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 9, in wrapper
AssertionError: Expected <class 'int'>
>>> gcd(27, 36)
9
>>>
```

既然都做了這件事就順便來複習一下 Python 一級函式的概念。

## 萬物皆是物件
因此在 Python 內函式也是種物件，現在我們可以嘗試建立一個函式讀取 `__doc__` 屬性，接著可以看到函式物件本身就是 function 類別實例：

```shell
>>> def factorial(n):
...     '''return n!'''
...     return 1 if n < 2 else n * factorial(n-1)
... 
>>> factorial(10)
3628800
>>> factorial.__doc__
'return n!'
>>> type(factorial)
<class 'function'>
>>> 
```

因此我們也就可以將函式做變數來指派並且用變數呼叫，也可以將函式作為引數傳遞：

```shell
>>> fact = factorial
>>> fact
<function factorial at 0x10d96f9d8>
>>> map(fact, range(10))
<map object at 0x10d9821d0>
>>> list(map(fact, range(10)))
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
```

除了可以讓使用者**自訂函式**外還有其他呼叫型態，像是**內建函式**、**內建方法**、**方法**、**類別**、**類別實例**、**產生器**。可以用 callable() 來確認是否可以呼叫。


## 函式自我檢查

除了前面提到 `__doc__` 的屬性外還有其他:

```shell
>>> dir(factorial)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

接著看看空函式以及空類別在實例函式的差異

```shell
>>> class C: pass
... 
>>> obj = C()
>>> def func(): pass
... 
>>> sorted(set(dir(func)) - set(dir(C)))
['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']
```

這個差集就是自訂函式地屬行，這些屬性其中的也可以用來作為傳入函式引數的檢查。


## 使用關鍵字參數

使用 `*args` 以及 `**kwargs` 是 Python 內傳遞參數很方便的方法。

註: cls 是 Python 3 用來傳遞 class 屬性

```python
def tag(name, *content, cls=None, **attrs):
    """Generte one or more html tags"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' %(attr, value)
                           for attr, value
                           in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                        (name, attr_st, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

if __name__ == '__main__':
    print(tag('br'))
    print(tag('p', 'hello'))
    print(tag('p', 'hello', 'world'))
    print(tag('p', 'hello', id=33))
    print(tag('p', 'hello', 'world', cls='sidebar'))
    print(tag(content='testing', name='img'))
    my_tag = {'name':'img', 'title': 'Sunset Boulevard',
              'src': 'sunset.jpg', 'cls': 'framed'}
    print(tag(**my_tag))
```

```shell
<br />
<p>hello</p>

<p>hello</p>
<p>world</p>

<p id="33">hello</p>

<p class="sidebar">hello</p>
<p class="sidebar">world</p>

<img content="testing" />

<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />

```

但要如何讓函式知道需要有什麼參數與是否有預設值呢？在前面我們有提到函式物件內 `__default__` 它會保存一個 tuple，裡頭有定位與關鍵字引數的預設值。關鍵字引數預設值會被存在 `__kwdefaults__`，引數的名稱則放在 `__code__` 屬性。這些屬性內可以用來讓我們判斷參數的性質。


但從這些屬性內來判定實在不方便，這時開始要用到前面提到一個很棒的 Python module: `inspect`。


`inspect.signature` 可以將函式回傳一個 `inspect.Signature` 的物件，裡頭有個 `parameters` 屬性讓你讀取 inspect.Parameter 物件有序名稱映射:

```shell
>>> def bob(a, b=123):
...     if a == 'Hello':
...         return b
...     else:
...         return 321
... 
>>> from inspect import signature
>>> sig = signature(bob)
>>> sig
<Signature (a, b=123)>
>>> for n, p in sig.parameters.items():
...     print(p.kind, ':', n, '=', p.default)
POSITIONAL_OR_KEYWORD : a = <class 'inspect._empty'>
POSITIONAL_OR_KEYWORD : b = 123
```


`inspect.Signature` 內有個 bind 方法用來取用任何數量的參數，並指派給簽章內參數。下面可以見到我們將 bind 方法內 `arguments.items()` 印出所有參數。

另外強制移除參數後會告訴我們缺少移除的參數。


```shell
>>> from tags_test import tag
>>> import inspect
>>> my_tag = {'name':'img', 'title': 'Sunset Boulevard',
...               'src': 'sunset.jpg', 'cls': 'framed'}
>>> sig = inspect.signature(tag)
>>> bound_args = sig.bind(**my_tag)
>>> bound_args
<BoundArguments (name='img', cls='framed', attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>
>>> for n, v in bound_args.arguments.items():
...     print(n, '=', v)
... 
name = img
cls = framed
attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}
>>> del my_tag['name']
>>> bound_args = sig.bind(**my_tag)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/chairco/.pyenv/versions/3.6.0/lib/python3.6/inspect.py", line 2934, in bind
    return args[0]._bind(args[1:], kwargs)
  File "/Users/chairco/.pyenv/versions/3.6.0/lib/python3.6/inspect.py", line 2849, in _bind
    raise TypeError(msg) from None
TypeError: missing a required argument: 'name'
```

另外 `__annotation__` 也以 dict 存放參數與回傳註釋。因此在檢查參數形態就可以與 bind 方法內的 `arguments.items()`來做比較。當我們在撰寫函式時可以利用 inspect 這個模組協助參數檢查。

---

其實 Python 內的一級函式真的是有很多東西可以來提。大概就簡單從 inspect 這個套件回顧，並且說明為什麼可以用這個套件來做參數檢查用。

