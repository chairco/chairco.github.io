---
Title: Python 協同程序運作
Slug: how-python-coroutines-work
Date: 2018-06-12 08:35:12
Modified: 2018-06-12 08:35:12
Tags: Python, Coroutine
Category: Python
---


>要達成非同步(Asynchronous) I/O 有很多種策略，常聽到的是使用多執行緒(multithreading)達到非同步。雖然 GIL(Global Interpreter Lock) 讓 Python multithreading 更適合 I/O 頻繁的應用(concurrency)，實際上過多的的上下文切換(context-switch)反而消耗了更多時間。[^1]

>最近因為需要使用到 Python Asyncio library 更深入接觸到協同程序(coroutine)的概念。簡單說協同程序是在 single thread 下允許程式來決定程式執行的順序，而有效達成非同步 I/O 的一種方法

>要理解協同程序的運作，我覺得最棒的一篇是 Jesse Jiryu Davis 的教學 ["How Python Coroutines Work"](https://emptysqua.re/blog/links-for-how-python-coroutines-work/)，這篇教學先從如何達成 Asynchronous I/O，最後說明如何用協同程序(coroutine)來達成。


達成 Asynchronous I/O 有如下幾個條件:

+ non-blocking
+ callback
+ event loop

接下來先讓我舉例說明吧

---

這邊以 socket 舉例，假設以 Flask 開發一個網站(server)，這個網站有兩個 url: /foo 和 /bar，這邊我們對網址讀取做了些設定，每一次讀取網址時都需要耗費一秒鐘時間（注意，這是刻意的。）

以下是 server 端的程式碼:

```python
# server.py
from time import sleep

from flask import Flask, Response


app = Flask(__name__)


message = b'Hello PyConTW2018! ' * 100 + b'\n'
CHUNK_LEN = 100
N_CHUNKS = len(message) / CHUNK_LEN

@app.route("/foo")
@app.route("/bar")
def hello():
    def generate():
        i = 0
        while True:
            chunk = message[i:i + CHUNK_LEN]
            if chunk:
                yield chunk
                sleep(0.877 / N_CHUNKS)
                i += CHUNK_LEN
            else:
                break

    return Response(generate())

if __name__ == "__main__":
    app.run(threaded=True)
```


這時用戶端 (client) 如果要讀取網頁 (server) 時，一個網址就會花費一秒，所以讀取 /foo, /bar 兩個頁面，理所當然就要花費大約 2 秒的時間。

```
import socket

def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            return
```

```shell
HTTP/1.0 200 OK
HTTP/1.0 200 OK
sync took 2.0 sec
```


因為 `server.py` 程式我們設計一個 block 機制，導致程式在執行時會被阻塞住，導致暫停執行，非同步 I/O 的想法其實很單純，假如程式在執行過程中因為 I/O 暫停，但如果`不會被阻塞`住就能暫時把控制權切換給其它程式，這樣就不會浪費執行時間。


不過在這之前我們先試試看大家比較習慣使用的 multithreading，在 Python 3.x 後提供一個高階的 concurrent 函式庫直接可以使用，用法很簡單，就是建立一個 ThreadPool，然後決定要開多少數量執行緒，接著把函式與參數丟進去，可以注意到在這些階段，程式無法決定何時要執行與否，這些動作都是由系統做決定。

```python
import socket
import time
import concurrent.futures


URLS = ['/foo', '/bar']

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_to_url = {executor.submit(get, url): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
    
    print('multithreading took %.1f sec' % (time.time() - start))
```

```shell
HTTP/1.0 200 OK
HTTP/1.0 200 OK
multithreading took 1.0 sec
[Finished in 1.1s]
```



接著我們來聊聊如何達成非同步 I/O。


## non-blocking（非阻塞）

非同步 I/O第一個條件就是 `非阻塞 (non-blocking)`，以這個範例，我們要如何將 socket 改成非阻塞？


```python
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()

def get_non_blocking(path):
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    # non-blocking sockets
    selector.register(s.fileno(), EVENT_WRITE)
    selector.select()
    selector.unregister(s.fileno())

    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ)
        selector.select()
        selector.unregister(s.fileno())

        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            return
```


Python socket 世界 `setblocking(False)` 就可以很方便可以將其設定為阻塞或是非阻塞模式，接著用 selectors 函式來註冊 socket 狀態。

selectors 是一個很棒的 high-level I/O multiplexing 模組，可以很簡單的來建構多路復用。因此我們先將連接的 socket 先註冊成可以寫入的狀態:

```python
selector.register(s.fileno(), EVENT_WRITE)
selector.select()
selector.unregister(s.fileno())
```

接著我們送出 request 然後在一個大迴圈裡將 socket 註冊成可以讀寫的狀態，接著就像前面讀取網頁一樣可以正常被讀取。

```python
selector.register(s.fileno(), EVENT_READ)
selector.select()
selector.unregister(s.fileno())
```


## callback（回呼）

首先我們將 socket 調整成為 non-blocking (非阻塞)，接著需要有個辦法知道完成了，這個方法是 callback，所以我們需要建立兩個函式，一個是 `connected`, 一個是 `readable`。

```python
import 略...

selector = DefaultSelector()

def get_callback(path):
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    callback = lambda: connected(s, path)  #(1)
    selector.register(s.fileno(), EVENT_WRITE)
    selector.select()
    callback()


def connected(s, path):
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    callback = lambda: readable(s, chunks)  #(2)
    selector.register(s.fileno(), EVENT_READ)
    selector.select()
    callback()


def readable(s, chunks):
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable(s, chunks)  #(3)
        selector.register(s.fileno(), EVENT_READ)
        selector.select()
        callback()
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        return
```


這邊我們用 lambda 來建構 callback，然後將 callback 想像成一個 stack:
```
        (3, readable())-----
                          |
    (2, connected())--- <--
                         |
(1, getcallback())---- <--
```

首先會從 (1) 開始呼叫，接著 (2) 最後在 (3) 時等待結果，最後再回傳給 (2) 最後 (1)。
發現了嗎? 在這個 stack 中是一個 single-thread，透過 callback 方式把狀態傳遞回來，所以在 readable 內會不斷遞迴自己直到訊息都被消化完。


## Event-loop（事件迴圈）

有了 callback 就能有個想法，能不能建立一個事件迴圈去監控，當事件沒有回傳值回來就去處理其他事情？
可以的，這時就會用到 select 來協助我們建立一個事件迴圈`紀錄`。

首先需要建立一個全域變數來控制事件迴圈是否要執行，接著將要執行工作全部註冊進入 selector 內。

```
def get_eventloop(path):
    global n_jobs  # 全域變數
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    callback = lambda: connected_event(s, path)  # closure
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_WRITE, data=callback) # 將 callback 註冊


def connected_event(s, path):
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    callback = lambda: readable_event(s, chunks)
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_READ, data=callback)


def readable_event(s, chunks):
    global n_jobs
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable_event(s, chunks)
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ, data=callback)
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        n_jobs -= 1
```


接著在最外層建立一個事件迴圈來運作，當我們將要執行得工作都丟入 select 內後，事件迴圈就會在一個 while loop 內不斷去檢查是否完成，直到所有事件都消化完畢跳出迴圈。

```
get_eventloop('/foo')
get_eventloop('/bar')

while n_jobs:
    print('%d, took %.1f sec' % (n_jobs, time.time() - self.start))
    events = selector.select()
    # what next?
    for key, mask in events:
        cb = key.data
        cb()

return('event_loop took %.1f sec' % (time.time() - self.start))
```


## Coroutine（協同程序）

這個情境裡頭最大的問題在於 callback(回呼)，對於大多數人來說很難一時之間理解某一段 callback 程式在做什麼，而過多的 callback 可能也讓程式碼看起來比較不那樣美觀，而以上的這些問題也就被某些人稱作 callback hell(回呼地獄)，下圖就用 js 極端的圖片例子:

![callback_hell](https://i.imgur.com/hOC70h2.gif) 


而為什麼會有 callback 的產生？在於程式之間的傳遞是用函式溝通，今天呼叫 A 函式得到一個回傳值，如果要把結果再讓 A 函式運算，就必須再把得到值丟回 A（這個例子是遞迴）


如果今天要讓程式間`資料的傳遞`更直覺，就必須將原本的函式溝通改善成為一個流程，於是 Python 的 generator（產生器）就發生作用，接著我們需要一個東西當事件被暫停時他要能把控制權拋出，於是需要時做一個 Future，有了上述兩點還需要去執行這些流程間工作，於是 Task（任務） 也是重點。


因此協同程序又被稱作 micro-thread(微執行緒)，在 Single-thread 由程式決定執行的順序。


所以要發展一個 Coroutine 需要幾樣東西:

+ generator
+ Future
+ Task


那要怎樣做呢？

首先 Future 實作直接使用 Python 3.5 之後定義的 [PEP 492](https://www.python.org/dev/peps/pep-0492/) __await__，就是一個 Awaitable。

Task 的實作很單純就是驅動協同程序運作，驅動方式就是發送一個 None 值。

```python
class Future:

    def __init__(self):
        self.callbacks = None

    def resolve(self):
        self.callbacks()

    def __await__(self):  #(1)
        yield self


class Task:

    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            f = self.coro.send(None)  #(2)
        except StopIteration:
            return

        f.callbacks = self.step
```

接著重點就來囉，因為有了 Future 讓我們可以讓程式將控制權拋出，所以就不需要 connected_event 與 readable_event 兩個函式，可以隨時用 await 來中斷程式執行。

這樣我們的程式看起來是否就簡潔多了呢？

```python
async def get_coroutines(path):
    global c_n_jobs
    c_n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()  #(1)
    selector.register(s.fileno(), EVENT_WRITE, data=f)
    await f  #(2)
    # s is writable
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    #callback = lambda: readable_coroutine(s, chunks)
    while True:
        f = Future()
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ, data=f)
        await f
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            break

    body = (b''.join(chunks)).decode()
    print(body.split('\n')[0])
    c_n_jobs -= 1

```

接著將 get_coroutines('/foo') 丟入 Task 內然後再透過事件迴圈不斷去檢視完成與否。

```python
Task(get_coroutines('/foo'))
Task(get_coroutines('/bar'))

while c_n_jobs:
    events = selector.select()
    # what next?
    for key, mask in events:
        fut = key.data
        fut.resolve()

return('coroutines took %.1f sec' % (time.time() - self.start))
```

接著試試看效果，ya 達成！

```shell
HTTP/1.0 200 OK
HTTP/1.0 200 OK
coroutines took 1.0 sec
```


希望這篇 Python 內實作協同程序方式分享你會喜歡，還有更多細節（包含 Asyncio）如果有空再來補完吧。



[^1]: http://cenalulu.github.io/python/gil-in-python/