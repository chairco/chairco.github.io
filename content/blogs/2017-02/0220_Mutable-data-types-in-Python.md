---
Title: Python 物件為可變參數時的使用
Slug: Mutable data types in Python
Date: 2017-02-20 20:00:00
Modified: 2018-1-6 15:11:00
Tags: Python
Category: Python

---

你可能會遇到，當物件參數需要預設給一個值時到底要給可變參數還是給一個 None 值？這個問題牽涉到 Python 設計的觀念 `object`，萬物都是一個 `object` 
所以當你產生一個 function 這個預設的參數值就產生了。我們用底下一個範例來說明：


```python
class Foo:
    def __init__(self, l=[]):
        self.l = l

class Bar(Foo):
    def __init__(self):
        Foo.__init__(self)

if __name__ == '__main__':
    f = Foo()
    b = Bar()
    f.l.append(5566)
    print(b.l)
```


如果你這樣做印出的 `b.l` 竟然是 `[5566]` 這太讓人驚訝了吧！？難道是什麼神奇的鬼魂在作怪？其實不是，因為 `l` 這個參數是使用一個可變變數 [] 
所以當你建立一個 f 的 `Foo()` 物件時他的預設參數也就產生了，因此當你建立 b 的 `Bar()` 物件時他其實是指向同一個記憶體位址。


那正確做法應該怎麼做呢？應該將 l 的變數設定為一個不可變的變數 None. 這樣才不會出現幽靈事件！


```python
class Foo:
    def __init__(self, l=None):
        if l is None:
            self.l = []
        else:
            self.l = list(l) # copy this list, not self.l = l, it will assign l to self.l also cause mutable error

    def remove(self, n):
        self.l.remove(n)

    def __repr__(self):
        return f'<foo {self.l}>'


class Bar(Foo):
    def __init__(self):
        Foo.__init__(self)

    def __repr__(self):
        return f'<Bar {self.l}>'


if __name__ == '__main__':
    # test 1
    f = Foo()
    b = Bar()
    f.l.append(5566)
    print(f)
    print(b)
    
    # test2
    l = [1,2,3,4]
    f = Foo(l=l)
    f.remove(4)
    print(l)
    print(f)


>>> <foo [5566]>
>>> <Bar []>
>>> [1, 2, 3, 4]
>>> <foo [1, 2, 3]>

```

**Cheers ！！!**



#### Update 2018/1/6

這邊在當初寫的時候有了一些錯誤，不過竟然隔了這麼久才發現 QQ，解釋一下 class Foo mutable 錯誤地方
原本是這樣寫的：

```
class Foo:
    def __init__(self, l=None):
        if l is None:
            self.l = []  <-- 這邊是正確
        else:
            self.l = l  <-- 這邊會有 mutable 的錯誤
```


剛開始為了解釋不同 class 之間繼承，如果可變參數沒有在初始化時 assign None 會造成錯誤，卻沒注意到如果有預設值時的問題。
`self.l = l` 的錯誤就在於，也指向了原本可變參數 l 的位置，因此我加了兩個 method `remove`, `__repr__` 作為示範，讓大家知道如果這樣做會造成錯誤：


```
>>> l = [1,2,3,4] # 建立一個 list = [1,2,3,4]
>>> f = Foo(l=l) # 建立 Foo 的物件為 f 且預設參數是 l
>>> f.remove(4) # 移除物件 f 內的 l 裡 4 這個值
>>> print(l) # 印出類別外的 l
>>> [1, 2, 3] # 錯誤了，原本了 l 不應該被移除
```

應該理解了吧，如果在一開始預設值沒有做可變參數複製，就會造成這樣錯誤。所以要改寫成 `self.l = list(l)` 接著來測試

```
>>> l = [1,2,3,4]
>>> f = Foo(l=l)
>>> f.remove(4)
>>> l
[1, 2, 3, 4]
>>> f
<foo [1, 2, 3]>
```

bingo 解掉問題了。不過發現這個錯誤是在面試時板書解題發現的，我也忘記為什麼那時候沒有注意。這真的是一個很低級的錯誤。希望大家可以吸取這個經驗。