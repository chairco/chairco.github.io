---
Title: 用 Python 來理解動態規劃 (Dynamic Programming)
Slug: Understand_Dynamic_Programming_usining_Python
Date: 2017-08-27 12:53:00
Tags: Dynamic Programming, Python
Category: Algorithms
---

動態規劃的想法就是 divide and conquer (分治法) + memoization (記憶法) 把問題細分成子問題然後做記憶。

## 回顧分治法的簡單概念

>把大問題分成小問題在各個擊破。白話講就是分解動作。和遞歸(Recursive)概念相同，取其遞迴精神。在進行這件事會有三個流程：Divide, Conquer, Combine。流程是切割問題、解決問題、合併解答。但在分治法比較特別是有時子問題不需要全部解決，例如二分搜尋法。在找尋問題時子問題與原問題相同但範圍不同被稱為 遞迴(recurrence)，通常我們會把其寫成遞迴公式，例如爬樓梯的問題。
>動態規劃雖然和分治法很相似，但選擇動態規劃一很重要原因是：如果採取分治法其中的遞歸實作會不斷用相同函式求解造成效率不佳，而動態規劃則是在求解過程把子問題答案先儲存在記憶體內，之後再去查表取出，這樣就能避免不斷堆疊的函式求解。


## <a name="menu"></a>動態規劃問題

整理了一些常見簡單的 DP 經典問題，點選可以快速跳到對應錨點(⚓️)

+ [費式數列](#dp_1)
+ [爬樓梯](#dp_2)
+ [階乘](#dp_3)
+ [樓梯路線](#dp_4)
+ [背包價值問題](#dp_5)
+ [找錢問題](#dp_6)


### <a name="dp_1"></a>費式數列 <small>*[回到最上層](#menu)*</small>


但想分享一個以遞迴做寫法但使用 Python 在 functools 裡有提供一個函式叫 `lru_cache` 解決堆疊函式被重複使用多次效能的問題。

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


>>> [fib(n) for n in range(16)]
>>> [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
```

如果對改寫成 DP 有興趣可以去看看**先前文章有稍微介紹**，[參考](/posts/2017/07/Let's%20talk%20about%20fibonacci%20with%20python.html)。


---

### <a name="dp_2"></a>爬樓梯 <small>*[回到最上層](#menu)*</small>
如果以一階或兩階方式爬樓梯，給定 n 階層樓梯，一共會有多少種走法？這問題就很適合來做分治法。首先走上第一階樓梯只有一種（一階一階爬），走上第二階層有兩種（兩階兩階爬或一階一階爬），但到了第三階他的走法就會是（一階一階爬）＋（兩階兩階爬）的總和，也就能歸納出 `f(n) = f(n-1) + f(n-1)`

這用遞迴很簡單，寫個函式不斷呼叫自己來加總。但可想而知樓梯的 n 越大堆疊越多，效能越不好。 
```python
def recursive_climbStairs(n):
    """
    :type n: int
    :rtype: int
    """
    if n == 1 or n == 2:
        return n
    else:
        return recursive_climbStairs(n-1) + recursive_climbStairs(n-2)
```

改成用分治法加上記憶法的動態規劃來處理。首先 `dynamic_programming(n)` 在迴圈過程會不斷向前去找已經計算過的答案。


先補充在做 DP 時的兩種實作方式:

1. Bottom-up
2. Top-down

`Bottom-up` 就是建立一個順序，往前去查詢已經計算好的結果來完成當前的計算。優點效率佳，但會把所有的問題都解出來，而不是只解出我們要的答案。所以 `dynamic_programming(n)` 會先順序地把所有結果都計算並且儲存起來。但因為我們只要最終結果，`climbStairs(n)` 回傳最終的結果。


```python
def climbStairs(n):
    """
    :type n: int
    :rtype: int
    """
    t = dynamic_programming(n=n)
    return t[-1]


def dynamic_programming(n):
    table = [1, 1]
    for i in range(2, n+1):
        table.append(table[i-1] + table[i-2])
```

看懂上面程式碼，發現可以將函式精簡。

```python
def climbStairs(n):
    if n < 3:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-2] + dp[i-1]
    return dp[n]
```

`Top-down` 就是可不按照順序，遞迴的由小到大處理各個子問題。這樣方法無法控制記憶體順序和效能較上面方法差？這是一個有趣問題，意思是說在處理過程才會逐步把子問題補滿。


```python
def topdown_climbStairs(n):
    if n == 0 or n == 1:
        return 1

    table = [0] * (n+1)
    table[0] = 1
    table[1] = 1

    i = 2
    while i <= n:
        if not table[i]:
            table[i] = table[i-1] + table[i-2]
        i += 1

    print(table)
    return table[n]
```

---

### <a name="dp_3"></a>階乘（factorial）<small>*[回到最上層](#menu)*</small>

撰寫階乘通常會立刻想到遞迴寫法。這想法太直覺了，範例如下：

```python
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)
```

不過這個會非常耗用記憶體資源，而且如果堆疊太深的話在 Python 會跑出 `RecursionError: maximum recursion depth exceeded in comparison` 這種超出堆疊限制的錯誤。這時候你還要設定 `sys.setrecursionlimit(5000)` 允許遞迴深度。因此 factorial 使用遞迴寫法看起來真不是一個好主意。

如果要改寫成動態規劃該怎麼做呢？做法很簡單，從階層的公式來看就是不斷的和前一個數字相乘得出的結果，因此我們做的迴圈將問題做分割，接著和前一個數字相乘把問題在組合起來。
這樣時間複雜度只需要 O(N)，空間複雜度 O(N) 但如果只處理一個 n! 問題那麼空間複雜度就是 O(1) 容易吧！

```python
def fib_dp(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f
```


---

### <a name="dp_4"></a>樓梯路線（ Staircase Walk ）<small>*[回到最上層](#menu)*</small>
假設一個方格棋盤大小為`(x, y)`。要從左上角(0,0)走到右下角(x,y)只能往右或是往下走，一共會有幾種走法？
反過來想從抵達位置來看，就是從上面來的或是從左邊來的。


用圖來看會比較清楚(圖引用自[演算法網站](http://www.csie.ntnu.edu.tw/~u91029/DynamicProgramming.html)):

![#](http://www.csie.ntnu.edu.tw/~u91029/DPCounting1.png)
![#](http://www.csie.ntnu.edu.tw/~u91029/DPCounting2.png)


所以就是從上面走來和從左邊走來相加就是走法。
數學上來表達加總走法： c(i, j) = c(i-1, j) + c(i, j-1)。這樣就可以做遞迴了。

![#](http://www.csie.ntnu.edu.tw/~u91029/DPCounting3.png)


所以概念就是建立一個二維陣列一個個 cell 把它加起來。

![#](http://www.csie.ntnu.edu.tw/~u91029/DPCounting4.png)


首先程式碼先建立一個 `x*y` 的二維陣列，接著把 `x = 0`, `y = 0` 的位置都設為 1（因為從這個位置出發）
接著每往左往下到達下一個 cell 就是將上和左的 cell 相加。

```python
def stairswalk(x, y):
    table = [[0 for i in range(x)] for j in range(y)]

    for i in range(0, x):
        table[i][0] = 1
    for j in range(0, y):
        table[0][j] = 1

    for i in range(1, x):
        for j in range(1, y):
            table[i][j] = table[i - 1][j] + table[i][j - 1]

    return "由(0,0)到({},{})共有{}種走法".format(x-1, y-1, table[-1][-1])


if __name__ == '__main__':
    print(stairswalk(x=8, y=8))
```

---

### <a name="dp_5"></a>背包價值問題 (Knapsack Problem) <small>*[回到最上層](#menu)*</small>

演算法在動態規劃裡都會提到它，有一堆物品個標示其金錢價值與重量，有一個背包可以裝物品，如何讓背包裝的物品價值金錢總價值最高。這個問題有個前提包背只限制重量不限制形狀，所以不需要考慮東西裝不裝得進去，只考慮重量與最高價值。

分割問題的方法是**放**與**不放**，接著放的重量與價值，不放後的重量與價值。

用函式表達會像是這樣

`k(n, w) = max(k(n-1, w), k(n-1, w-weight[n]) + cost[n])`

n: 0 ~ n 個放進背包內物品
W: 背包的負載重量
knapSack(n, w): 0 ~ n 個物品耐重為 w 的答案
wt[n]: n 物品的重量
val[n]: n 物品的價值


需要考慮的條件

1. 考慮邊界條件，耐重不足或是沒有物品。 
    W < 0 return 0
    n < 0 return 0
    n = 0 and W >= 0 return 0

2. 避免存取負的物品與耐重。 
    n = 0 return 0
    n > 0 and W-wt[n] < 0 return knapSack(n-1, w)


採用 top-down 方式解題

```python

# Returns the maximum value that can be put in a knapsack of
# capacity W

def knapSack_topdown(W, wt, val, n):
    # Base Case
    if n == 0 or W == 0 :
        return 0
 
    # If weight of the nth item is more than Knapsack of capacity
    # W, then this item cannot be included in the optimal solution
    if (wt[n-1] > W):
        return knapSack(W , wt , val , n-1)
 
    # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(val[n-1] + knapSack(W-wt[n-1] , wt , val , n-1), 
            knapSack(W , wt , val , n-1))


if __name__ == '__main__':
    val = [60, 100, 120]
    wt = [10, 20, 30]
    W = 50
    n = len(val)
    print(knapSack_topdown(W , wt , val , n))
```


採用 bottom-up 方式解題

```python
def knapSack_bottomup(W, wt, val, n):
    K = [[0 for x in range(W+1)] for x in range(n+1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n+1):
        for w in range(W+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w] 
    return K[n][W]


if __name__ == '__main__':
    val = [60, 100, 120]
    wt = [10, 20, 30]
    W = 50
    n = len(val)
    print(knapSack_bottomup(W , wt , val , n))
```


---

### <a name="dp_6"></a>找錢問題 <small>*[回到最上層](#menu)*</small>


---

參考資源:

+ [動態規劃題目](http://www.geeksforgeeks.org/dynamic-programming/#concepts)


---
