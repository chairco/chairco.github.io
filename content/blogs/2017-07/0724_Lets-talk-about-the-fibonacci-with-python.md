---
Title: Python 實作斐波那契（Fibonacci）兩三事
Slug: Lets talk about the fibonacci with python
Date: 2017-07-24 18:31:26
Tags: python, fibonacci
Category: Algorithms

---

>Fibonacci 是在資料結構上說明遞迴一個很直覺的範例，不過在演算法上也是不可或缺的指導教材。最近陸續在準備一些線上考試回來看才發現自己其實低估了這些科普教材對於自我訓練的重要性。

>本篇會從一些遇到的範例，並試著從遞迴、效率的觀點來探討，同時也檢測自己對程式設計與演算法上是不是有不足之處。如果發現在觀念上有錯誤，希望讀者給予指教。

>範例程式碼都會以 Python 來實作。


##遞迴(Recursion)

計算機概論或是資料結構開始講遞迴(recursion)時都會以 Fibonacci 來講解怎麼讓函式不斷 callback 來解出最後的答案，程式碼會像是這樣

```python
def fibonacci(n):
    if n == 0 or n ==1:
        return n
    else:
        return fibonacci(n-1)+fibonacci(n-2)
```

一般程式新手比較無法理解的就是 `return fibonacci(n-1)+fibonacci(n-2)` 這段，簡單來說就是程式不斷 callback 自己來重複處理問題。缺點就是時間複雜度很高（ `O(f((2^n))` ），這段程式碼如果用個人電腦 MAC MBPR 來跑大概 `fibonacci(n=30)` 應該就會卡住了。不過大學的資料結構也就提到這邊，要再深入一點去用其他解法可能要到演算法部分。

***


所以接下來我就來討論以演算法的觀點:

1. Top-down

2. Bottom-up

!['#'](http://www.csie.ntnu.edu.tw/~u91029/DPRecurrence8.png)


##Bottom-up

訂定一個計算順序，然後由最小的問題開始計算。特色是程式碼通常只有幾個迴圈。這個實作方式的好處與壞處與前一個方式恰好互補([引用網站](http://www.csie.ntnu.edu.tw/~u91029/DynamicProgramming.html#1))。

以上面遞迴的範例來看，在 Bottom-up 就會訂定一個順序，然後把算出來的解答存起來，這樣就可以不用一直去重複，效率也快很多，時間複雜度會降到（`O(f(n))`）：


```python
def fibonacci(n, fib=[0,1]):
    if n >= len(fib):
        for i in range(len(fib), n+1):
            fib.append(fib[i-1]+fib[i-2])
    return fib[n]


if __name__ == '__main__':
    for i in range(0, 20):
        print(fibonacci(n=i))
```

上面這段程式碼其實依賴於 Python 實作好的 `list` 資料結構特性，透過一個順序，把計算好的答案放進 `list` 內，下一步驟把算法的答案取出來在計算。


當然如果你想用 C 的方法來思考也可以，在堆疊上我們稱為遞迴堆疊，就是透過一個變數，預先儲存上個答案：

```python
def fibonacci(n):
    if n == 0 or n == 1:
        return n
    a, b = 0, 1
    for i in range(2, n+1):        
        temp = b
        b = a + b
        a = temp
    return b


if __name__ == '__main__':
    for i in range(0, 20):
        print("n={}, fin={}".format(i, fin(n=i)))
```

概念上大概都是一樣，就是用空間換取時間，記憶體先把答案存起來，然後需要再把它拿出來用。


##Top-down

簡單來說這個演算法概念就是不管順序，所以不必走過每一段路。

```python
class dpFib(object):
    def __init__(self):
        self.__result = {0: 0, 1: 1}

    def fib(self, x):
        if x in self.__result:
            return self.__result[x]

        r = self.fib(x-1) + self.fib(x-2)
        self.__result[x] = r
        return r


if __name__ == '__main__':
    dpfib = dpFib()
    print(dpfib.fib(x=8181))

```


##延伸思考

既然對於資料結構與演算法有了些概念，就有了些有趣的問題，例如我要怎麼透過 Python 將 fibonacci 計算後的所有數字再做一次三次方(pow)?


```python

cube = lambda x: x**3 # complete the lambda function 

def fibonacci(n):
    # return a list of fibonacci numbers    
    if n == 0:
        fib = []
    elif n == 1:
        fib = [0]
    else:
        fib = [0,1]
    if n >= len(fib):
        for i in range(len(fib), n):
            fib.append(fib[i-1]+fib[i-2])
    return fib


if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))
```

概念其實就很簡單，會用到 Python 的 built-in function `map`。在 `def fibonacci(n)` 內會先透過 `list` 儲存結果，接著用 `map` 搭配 `lambda` 將陣列內每個值都抓出來做三次方的計算。



不過上面的函式可以更精簡，不知道你有想到嗎？

```python
cube = lambda x: pow(x,3)# complete the lambda function 

def fibonacci(n):
    # return a list of fibonacci numbers
    lis = [0,1]
    for i in range(2,n):
        lis.append(lis[i-2] + lis[i-1])
    return(lis[0:n])
```

***

做一些紀錄，其實演算法是一個能夠訓練大腦的方法，接下來我會嘗試用 Dynamic programming(動態規劃)的方法來思考與講解這些例子。

