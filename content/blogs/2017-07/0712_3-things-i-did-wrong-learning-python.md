---
Title: 學習編寫 Python 時應該避免的三種錯誤
Slug: 3 mistakes to avoid when learning to code in Python
Date: 2017-07-12 13:13:29
Tags: 翻譯, Python, Programming
Category: Python

---


關於可變變數在 Python 作為參數使用一直是初入朋友的痛。尤其看起來執行起來一切正常的 Python Code，卻跑出不可預期的結果著實讓人心煩。

>本篇 **TL;DR**，文字太多有害身體健康。所以想 3 mins 搞懂這篇文章，歡迎你移駕[本篇](/posts/2017/02/Mutable%20data%20types%20in%20Python.html))，但想深入一點暸解就歡迎參考這篇翻譯拙作。

>文章為翻譯文，採對照方式寫作。歡迎給予各種指教。[原文網址](https://opensource.com/article/17/6/3-things-i-did-wrong-learning-python)


***

![#](/pics/201707/blocks_building.png "Image by : opensource.com")


承認做錯事從來都不是容易的事，但錯誤卻是學習過程的一部份，從一個新語言開始習得就像學習如何走路，像是 Python。


這裡列出三件我學習 Python 遭遇的錯誤，提出來也避免初入 Python 的程式設計人員可以避免犯下相同問題。這些錯誤都造成更大問題以至於我必須抽出很長的時間並且花費數小時去修復它。


年輕的夥伴們，這些錯誤真的都是浪費無謂的時間。


## 1. 在函式中的默認的參數使用了可變變數來定義


合理嗎？你撰寫一個小型函式，這個函式可以搜尋當前頁面上的連結並且將它附加到另外一個 list 裡。


```python
def search_for_links(page, add_to=[]):
    new_links = page.search_for_links()
    add_to.extend(new_links)
    return add_to
```


看到這邊，一切都非常的完美的，確實也可以正常的運作，但卻有些問題。假如我們期望傳遞一個 list 給 `add_to` 這個參數，會如預期中運作。然而假如我們在程式執行時給了預設值，有趣的事情就會發生了。


試試以下的程式碼：

```python
def fn(var1, var2=[]):
    var2.append(var1)
    print var2

fn(3)
fn(4)
fn(5)
```

預期的輸出結果：

[3]

[4]

[5]


但我們會非常詫異的發現實際上的結果：

[3]

[3, 4]

[3, 4, 5]


為什麼？你看到在每一次不同的呼叫裡使用了同樣的一個 list。在 Python 當我們撰寫一個如範例的函式時，list 會被初始化成在函示一部份當這個函式被定義時。因此它不會在每一次函式執行時被實例化（譯者補充：這裡原作者意思是 Python 在函式被定義時所有的參數值就已經產生，因此不會每一次呼叫時又產生一次）。這意味著函式維持了並且不斷使用同樣的 list 物件，直到我提供了其他的 list 物件:

```python
#定義了一個新的 list [4]
fn(3, [4])
```

[4, 3]


如何達到預期。正確的做法要像：

```python
def fn(var1, var2=None):
    if not var2:
        var2 = []
    var2.append(var1)
```

或是，將第一個範例改成：

```python
def search_for_links(page, add_to=None):
    if not add_to:
        add_to = []
    new_links = page.search_for_links()
    add_to.extend(new_links)
    return add_to
```


這樣就能變動`實例化`從每一次模組被加載時，讓每次函式被執行都能發生。但注意對於不可變動的資料型態像是：`tuples`, `strings` 或是 `ints` 這是非必要的。也意味著在對於非變動的資料型態這樣做是好的：

```python
def func(message="my message"):
    print message
```
<br>


## 2. 可變變數作為類別變數


緊跟在後的錯誤和前個錯誤非常相似。考慮下面幾點：

```python
class URLCatcher(object):
    urls = []

    def add_url(self, url):
        self.urls.append(url)
```


這段程式碼看起來完全正常。我們擁有一個物件，這個物件用來儲存 URLs。當我們呼叫 `add_url` 這個方法，儲存我們給定一個新增的 URL。完美？對吧。讓我們看看問題：

```python
a = URLCatcher()
a.add_url('http://www.google.')
b = URLCatcher()
b.add_url('http://www.bbc.co.')
```

**b.urls**

```
['http://www.google.com', 'http://www.bbc.co.uk']
```

**a.urls**

```
['http://www.google.com', 'http://www.bbc.co.uk']
```

等等，到底發生什麼事!？ 沒有預期這樣的結果啊。 我們實例化兩個單獨的物件，a 和 b。 a 給了一個 URL 然後 b 給另一個。怎麼兩個物件都變成擁有兩個 URLs？


這樣的結果和前面我們舉的第一個例子是一樣的問題。 當定義的類別被建立時 URLs 的 list 就已經被`實例化`。所有類別內的的實例都會使用同樣一個 list。現在這裡有些優秀的例子，但多數時候你不會想這樣做。你會希望不同的物件各自單獨的儲存。要做到這樣，我們必須針對程式碼做一些變動：


```python
class URLCatcher(object):
    def __init__(self):
        self.urls = []

    def add_url(self, url):
        self.urls.append(url)
```


現在這些 URLs 的 list 當物件被產生時才會被`實例化`。當我們實例化兩個單獨的物件時，他們將會個別擁有自己的 list。


## 3. 可變變數的賦值錯誤


這是困擾了我一段時間。讓我們做一些些改變，使用可變得資料型態 `dict` 

```python
a = {'1': "one", '2': 'two'}
```


現在讓我們宣告並將這個 `dict` 使用在其他區塊，並保留原區塊無缺。

```python
b = a

b['3'] = 'three'
```

很簡單吧，嗯？


接著看看原先的 `dict`, a 我們並不希望他被改變：


```python
{'1': "one", '2': 'two', '3': 'three'}
```

挖，等一會兒。那 b 看起來怎樣了？

```python
{'1': "one", '2': 'two', '3': 'three'}
```


等等，發生什麼事了？但... 讓我們還原然後確認假如我們使用不可變數形態, `tuple` 來做實例化：

```python
c = (2, 3)
d = c
d = (4, 5)
```

現在 c 是：

```
(2, 3)
```


接著 d 是：

```
(4, 5)

```


這個函式如我們所預期。所以範例到底發生什麼事了？ 當使用一個可變數型態，我們得到的一些行為很像是 C 的指標。當我說 `b = a` 在上述程式碼，實際上我們指的是： b 現在參考 a。在 Python 的記憶體，兩著指向相同的物件（譯者：指向相同的記憶體位址）聽起來很熟悉吧？這是因為相似於先前的問題，實際上這篇可以被稱為 **"The Trouble with Mutables."**


這樣的問題也會發生在 lists 內嗎？ 是的。所以如何解決它呢？嗯，我們必須非常小心。假如我們真的需要一個複製 list 的流程，我們可以這樣做： 


```python
b = a[:]
```


這樣將會執行並且複製一個參考內每一個項目到 list 然後配置一個新的區塊給這個新的 list(譯者：配這一塊新的記憶體空間給新的 list)。但是必須警示：假如任何物件在這個 list 而且是可變得，我們我們將要在一次得到他們的參考，而非完全複製。(譯者：例如 a=[], b=[1,2,b], 這時 b 也是可變動，這樣的複製只是淺複製，b 還是會產生這樣問題。關於這個問題可以參考 [copy](https://docs.python.org/3.6/library/copy.html))


想像有一張上有 list 的白紙。這個原創的範例，A 人類和 B 人類在看相同的一片白紙。假如 list 內有一些變動兩個人類都會看到變化。當我們複製這個參考，現在各自有自己的 list。但讓我們假設這是一個搜尋食物 list。假如 "fridge(冰箱)" 位於 list 第一個 point，接著複製它後，兩個項目在兩個 lists point 都會有同樣的一個冰箱。所以假如冰箱內被人類 A 改變，例如吃一掉一個奶油蛋糕，人類 B 將會發現奶油蛋糕消失了。不是容易理解，這僅僅只是讓你記住和編寫程式碼時不要造成這類問題。


`Dicts` 函式也是同樣道理，可以建立一個`昂貴`的複製：

```python
b = a.copy()
```


同樣，他也只是建立一個新的 dictionary 指標到同一個條目位置，因此假如我們有兩個相同 lists，我們改變其中一個指向可變物件 dict `a`，這個 dict 物件會立刻看到 dict `b` 被更動。


這些可變變數的災難在於他們非常強大。上述都不是真正問題; 而是要被謹記於心以防止出錯。在第三個項目中使用昂貴的複製操作在 99% 時間都是非必要的。你的程式應該要可以被修改讓這些複製不是非必要的。


開心的的編寫程式，並且歡迎留言提出任何問題在意見評論表中。

