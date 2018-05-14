---
Title: RESTful web services cookbook 
Slug: Restful-web-services-cookbook
Date: 2018-01-18 22:17:01
Modified: 2018-01-18 22:17:01
Tags: Python, RESTful, API
Category: RESTful
---


這份文件主要是整理過去在開發 RESTful web services 的一些觀念，在 Django 裡有套很棒的第三方套件叫 [Django REST framework](http://www.django-rest-framework.org/) 可以讓使用者很輕鬆的打造 Web APIs 但我覺得還是有必要確認自己過程中是否真正了解 REST 的觀念以及再使用其他 framework 時也能正確的操作，因此有了這份紀錄的產生。

但首先也是先提一下有人問我 REST 是什麼？我覺得我的回答會是 REST 是一種風格，目的是透過簡潔方法達到類似 SOAP, XML-RPC 等方法。這個風格是基於 HTTP、URL、XML、HTML 這些標準與協定。然後具備 REST 風格的 Web API 被稱為 RESTful API。如果有人覺得可以更詳細的補充請告訴我。

接著就從動詞，使用情境等紀錄，希望也在做這些開發的朋友如有發現錯誤能給予指教。



## 動詞
+ GET - 得到**一個**資源描述(情境為安全下使用)
+ PUT - 建立與更新**一個**資源
+ DELETE - 用於刪除資源
+ POST - 建立**多個**新資源，或對多個新資源進行他種變更


### GET

不要將 GET 用於不安全的操作上，例如購物車上的`添加商品`、`發送訊息`、`刪除訊息`等等操作。但如果一定要使用 GET 來做務必確認以下幾點：

1. 確保這個操作沒有做暫存： Catch-control:no-catch
2. 確保副作用(side effect)都是良性的，不會影響重要的資料
3. 在 server 上最好是將這些操作做成可以重複執行


### POST

POST 的重點覺得應該是在多個資源的操控，而且他能將很多資料包成一個資料結構傳輸。例如在做查詢時候，要丟很長串資料 GET 可能會受限於 URL 在瀏覽器上的長度。 POST 就能解決這類問題。不過還是有些情境如下整理：

1. 將資源視為一個工廠(factory)
2. 透過一個控制器來修改一或多個資源
3. 執行大數據的傳輸查詢
4. 執行不安全或非冪等(no Idempotent)操作


整理了適用的情境：

1. 對已經存在的資源註解
2. 對信箱列表、新聞群組或是類似群組發送訊息
3. 資料模組，例如表單送到資料處理後的結果
4. 額外操作擴充資料庫

也因此暫存不會儲存這些方法造成影響，爬蟲工具不會發出 POST 請求，大部分通用的 HTTP 工具不會重複的傳送 POST 請求。


雖然適合用 GET 但用 POST 更為適合情境:

1. 瀏覽器發出的請求，如果將相關內容用 URL 做傳遞可能會洩漏敏感訊息例如：信用卡資料等等，如果無法使用 TLS 時候就可以考慮用 POST。
2. 客戶送出的資料有太多的參數時。

POST 創建資源方法是採用 factory 模式。


### PUT

用來創建與更新單一資源。與 POST 差異在於當用戶端知道創建資源的 URL 時才能使用 PUT 不然就使用 POST，因此在這樣方法下伺服器需要和用戶端解釋 URL 如何組成，什麼樣的 URL 是合法或是非法的。同時還要顧慮到伺服器端是否有設定 URL 的模式或是過濾規則。通常會使用範圍較小的 URL 來創建資源。


## 設計

RESTful API 透過 URL 來標示`資源(resource)`的實體。因此會使用 HTTP 描述與格式來包裝這些實體與實際的標頭。接著稍微介紹一下我知道的部分：


### Header 的描述包含以下幾項

+ Content-Type: 描述 Header 類型與包含的參數
+ Content-Length: 正文字串長度
+ Content-Language: 指定得語言
+ Content-MD5: 採 MD5 驗證的摘要
+ Content-Enconding: gzip, compress or deflate 編碼時使用
+ Last Modified: 資源被修改的時間


```html
# 範例
Content-Type: application/xml;charset=UTF-8 
Content-Language: en-US
Content-MD5: bbdc7bbb8ea5a689666e33ac922c0f83
Last-Modified: Sun, 29 Mar 2009 04:51:38 GMT

<user xmlns:atom="http://www.w3.org/2005/Atom"> <id>user001</id>
<atom:link rel="self" href="http://example.org/user/user001"/> <name>John Doe</name>
<email>john@example.org</email>
</user>
```


#### Content-Type

描述 header 的類型，通常會說 media-type or MIME。例如：text/html、image/png 這些都是一種 header，目的是告訴你要將這種訊息要編譯成哪一種格式的方法。XML、JSON 這些都是。所以如果沒有標頭就只能猜測。


#### Content-Length

讓接收方來判斷是否接收正確的數據長度。但 HTTP 1.1 有了`分塊傳輸編碼 (chuncked transfer encoding)` 讓接收方不需要預先知道數據長度，因為最終會有一個 0 的塊結束。但如果是 HTTP 1.0 並未包含分塊傳輸編碼所以還是需要 Content-Length。


#### Content-Language

本地化的語言需求。


#### Content-MD5

用來驗證數據文本的完整性。但不能保證是否數據被竄改。


#### Content-Enconding

表示數據壓縮的方式，但是因為沒有方法知道 server 使用的壓縮法，所以儘量避免使用除非很清楚知道。


#### Last Modified

用來表示資源最後被修改時間。

---