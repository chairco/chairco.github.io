---
Title: PEP 557 -- Data Classes 擁抱更友善的資料模型
Slug: Python PEP 557 Data Classes introduction
Date: 2017-12-05 23:49:05
Modified: 2017-12-05 23:49:05
Tags: PEP, Data Classes
Category: Python
---

Python 的 Class 裡我們透過 `__init__` 來做初始化一個類別與所需變數，然後透過兩個底線的方法例如 `__repr__`, `__eq__` 來定義資料模型。有沒有更好的方法呢？[PEP 557](https://www.python.org/dev/peps/pep-0557/) 引入了一個嶄新的定義資料模型方式。結合對變數型態的宣告(PEP 526)，雖都知道變數型態的宣告在 Python 是經常被忽視，不過在 PEP 557 倒是有了很大的用處。


首先我們採用文件範例先用過去我們認知的寫法重新表示一次，再來比較新的方式：

```python
class InventoryItem:
    
    def __init__(self, name, unit_price, quantity_on_hand=0):
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand
    
    def __repr__(self):
        return f'InventoryItem(name={self.name!r} unit_price={self.unit_price!r} quantity_on_hand={self.quantity_on_hand!r})'
    
    def total_cost(self):
        return float(self.unit_price * self.quantity_on_hand)

>> item = InventoryItem('hammers', 10.49, 12)
>> print(item)
>> InventoryItem(name='hammers' unit_price=10.49 quantity_on_hand=12)
```

很平常的寫法，會生成一個 InvertoryItem 的物件，印出來是一個 `__repr__` 所返回的代表的描述。物件內有一個 `total_cost` 方法協助我們計算總花費。 但說實話很繁瑣，為了要清楚定義，必須要使用很多兩個底線的方法來處理 Python 的資料模型。


**但現在引入 dataclass 後我們只需要輕輕鬆鬆改寫成**：

```python
@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

>> item = InventoryItem('hammers', 10.49, 12)
>> print(item)
>> InventoryItem(name='hammers', unit_price=10.49, quantity_on_hand=12)
```


`@dataclass` 裝飾器會協助增加等價方法的自訂型態到類別內，就不需要在維護這些自訂型態。

```python
def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0) -> None:
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand
    
def __repr__(self):
    return f'InventoryItem(name={self.name!r}, unit_price={self.unit_price!r}, quantity_on_hand={self.quantity_on_hand!r})'

def __eq__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) == (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented

def __ne__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) != (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented

def __lt__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) < (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented

def __le__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) <= (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented

def __gt__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) > (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented

def __ge__(self, other):
    if other.__class__ is self.__class__:
        return (self.name, self.unit_price, self.quantity_on_hand) >= (other.name, other.unit_price, other.quantity_on_hand)
    return NotImplemented
```


為何需要額外為了資料模型而增訂這個 PEP? 已經有很多例子可以去做定義：

+ 標準庫的 collection.namedtuple 
+ 標準庫的 typing.NamedTuple
+ 流行的 attrs [1](https://www.python.org/dev/peps/pep-0557/#id16) 專案
+ 許多線上的範例食譜 [2](https://www.python.org/dev/peps/pep-0557/#id17), 套件 [3](https://www.python.org/dev/peps/pep-0557/#id18), 與問題 [4](https://www.python.org/dev/peps/pep-0557/#id19). 在 PyCon 2013 metaclass talk David Beazley 使用一個 form of data classes as the motivating example [5](https://www.python.org/dev/peps/pep-0557/#id20).


在 PEP 526 已經有一個簡潔方式去定義 class 的成員，而這個 PEP 在這個基礎之下提供一個簡單且不會太突兀的方式來定義資料模型，除了沒有指定屬性類型的設置。`dataclass` 是一個真正的類別，所以也不用擔心在繼承過程中影響其他的類別等副作用。


資料模型的建置目地是能有一個靜態的類別型態檢查器，在 PEP 526 的使用就是一例，這裡設計 `fields()` 函式與 `@dataclass` 裝飾器， 由於動態的本質，上面所提到的一些 library 會很難與檢查器一起使用。


哪裡不適合呢？

+ API 需要兼容 tuple 或 dict
+ 除了 PEP 484 和 526 提供的 type 驗證之外，還需要進行 value validation，或者需要進行值驗證或轉換。


以上，開始擁抱 Python 新的 Data Classes 吧！
