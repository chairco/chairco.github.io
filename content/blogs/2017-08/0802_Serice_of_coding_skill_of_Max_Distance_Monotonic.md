---
Title: 寇汀技巧系列之 Max Distance Monotonic
Slug: serice of coding skill of Max Distance Monotonic
Date: 2017-08-02 22:45:02
Tags: Coding, Max Distance Monotonic
Category: Python

---

>寇汀技巧系列應該稱我的 Codility 落敗系列筆記。因為做了一些 Codility 線上測驗發現自己看完題目沒有辦法立刻反應要考哪種技巧，再來是很久沒有認真在寫程式時注意資料結構，所以在時間複雜度的拿捏不好。

>希望可以藉由自修方式把這部分補足。也可以改進自己在寫程式老喜歡硬幹的壞習慣。


***


## Max Distance Monotonic, Caterpillar method

>關於 Max Distance Monotonic（最大距離）和在這個題目底下的變形 Caterpillar method（毛蟲法）是經常線上測驗會出的變化題，這類變化考得到不是測試正確性，反倒有一半是在考驗程式效率。整理了幾個變化題來思考。



基本題型原文會是這樣：
>You can still give it a try, but no certificate will be granted. The problem asks you to find a pair of
indices (P, Q), such that A[P] <= A[Q] and the distance between P and Q is maximal, that is
the value Q − P is maximal.

中文意思是 list (串列) A, 有 N 個 Integer。 串列有幾個變數 P, Q，表示 A 的 index。
要找出成對 (P, Q) 為最大值（The distance between P and Q maximal(Q-P)）條件 0 <= P <= Q <= N，A[P] <= A[Q]。


### solution 1
看到太令人興奮，兩個迴圈就能解決，也很直觀。第一個迴圈從 0~N-1(因為 A[P] <= A[Q]), 第二個迴圈從 P-1 ~ N，接著兩兩比較 Q - P 一直找到最大的。

但會有個問題：

+ 第一個時間複雜度太高，把所有可能都跑完的時間複雜度最高可能是 O(N**2)。


```python
def solution(A):
    N = len(A)
    result = 0
    for P in range(N-1):
        for Q in range(P+1, N):
            result = max(result, Q-P)
    return result
```


### solution 2
首先要解決時間複雜度的問題就是要降低迴圈層數，有這個目標想法就是空間換時間。

朝能不能先用一個迴圈把部分問題先解決來想。仔細思考要簡化的方法是: 如果能先解決 A[P] <= A[Q] 這個子問題。因為一個串列是根據 index 來排序，但每個 index 所對應的值大小不同，所以必須要做兩兩比較。但如果我們能先把這個串列的值排序就能解決要用兩層迴圈兩兩比較的問題。

```python
def solution(A):
    N = len(A)
    result = 0
    pairs = []
    for i in range(N):
        pairs.append((A[i], i))
    pairs.sort()
    
    minOriginalPos = N
    for (value, idx) in pairs:
        minOriginalPos = min(minOriginalPos, idx)
        result = max(result, idx-minOriginalPos)
    
    return result
```

和 `solution 1` 差別在建立一個 pairs 的串列來存值，這樣方便我們做排序。
接著根據小到大排序，因為要滿足 A[P]<=A[Q]。有了排序再來計算 Q-P 就簡單了。

首先建立一個 minOriginalPos 變數是串列的長度，因為已經將值排序，所以概念是我希望從小值到大值找到最大的 index 差值。概念上上這個已經排列好的串列透過 min() 兩兩比較儲存最小的 idx 接著用 result 去計算哪個差是最大的。因為對於我們而言已經解決 A[P] <= A[Q] 所以 value 是什麼並不在意。


### solution 3
竟然還有更好的解法？好吧就留給讀者去想想了。因為我也是參考了大神的教學發現，但看了也是跪拜啊（雖然一開始有想過，但沒想到這是好解法）給個提示（for + while 會是好方向）


## 變化題

接著來思考關於這個變化題，原本在討論的是在 A[P]<=A[Q] 條件下 (P,Q) 最大值。那假設 0 <= P <= Q <= N 會產生一個 sum-distance A[P]+A[Q]+(Q-P)，換成要找一個 maximal sum-distance?


### solution 1
先來看看直覺解法，但效能不是很好

```python
def solution(A):
    N = len(A)
    result = 0
    for P in range(N-1):
        for Q in range(P-1, N):
            result = max(result, A[P]+A[Q]+(Q-P))
    return result
```


### solution 2
動動大腦，如果我們要精簡問題，享用空間換取時間從哪邊可以下手？看起來可以從 A[P]+A[Q]? 因為我們有個準則是 P<=Q。

解法是 Caterpillar method（毛蟲法）來思考，透過 while 迴圈與兩個變數讓串列往左或是往右。

```python
def solution_1(A):
    value = 2000000000
    front_ptr = 0
    back_ptr = len(A)-1
    A.sort()
     
    while front_ptr <= back_ptr: 
        value = min(value, A[front_ptr] + A[back_ptr] + (back_ptr - front_ptr))
        if abs(A[front_ptr]) > abs(A[back_ptr]):
            front_ptr += 1
        else:
            back_ptr -= 1
             
    return value
```


大概這類題型變化不出這幾種，希望如果有機會大家遇到這樣考題可以有更多不一樣思考。
 
