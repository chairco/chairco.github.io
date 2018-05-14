---
Title: Github.io 自訂網域名稱且透過 Cloudflare 申請免費 https
Slug: Github.io Pages redirect to domain name and add HTTPS 
Date: 2017-06-29 15:33:03
Tags: https, domain name, Cloudflare, gandi
Category: Web

---

這個部落格也快一年，雖然進化得很慢但還是有在進步。最近進步的一件事（應該不能說是進步，要說跟上）終於想把用了很久的 [blog](https://chairco.github.io) 掛上網域名稱（之前是把網域名稱導過來 chairco.github.io, 喂，你搞什麼啊！！）

大概半年前在 Gandi 有申請一個 chairco.com.tw 的網域，不過當時比較麻煩問題是不知道怎麼掛上 https，查一下解法是買一個主機架設 DNS，但就有點貴了。 Gandi 似乎有提供免費？但可能我是免費一年序號，所以要花錢買，大概沒有繼續處理就這樣苟且偷生下去了。

主要是最近 **pay.taipei** ([事件緣起](https://www.facebook.com/schreibmal/media_set?set=a.10212928669916690.1073741842.1388906446&type=3&pnref=story)) 然後看到很多人在講這件事，結果很多部落主在批評時也被反說他的網站也沒做 HTTPS。心裡覺得要洗別人臉自己臉真的要洗乾淨所以就決定來完成它了。


架設 Blog、自訂網域名稱、設定 https 主要分成三塊服務商：

+ Github：靜態網頁
+ Gandi：網域名稱供應商
+ Cloudflare：提供 DNS、HTTPS 傳輸服務


## Github
大概多數靜態網頁都很容易架設，可以參考完整的[官方教學](https://pages.github.com/)


## Gandi
網域名稱供應商，註冊之後可以付費購買網域名稱，網域名稱購買之後要怎麼讓 github.io 轉址，就只需要在 github.io 靜態網頁下建立一個 CNAME。另外也要編輯在 Gandi 的 zone file。[完整教學參考](http://spector.io/how-to-set-up-github-pages-with-a-custom-domain-on-gandi/) 接著原本的 github.io 網址就會被導到新網域。

不夠清楚可以參考這篇 [blog](https://blog.dmoon.tw/github-pages-custom-domain/index.html)

不過這裡有個要注意的，在編輯 zone file 時一定要確認編輯完成之後 Gandi 有吃到修改的設定檔，通常有吃到之後，下圖的 **Operations** 會出現運作的數量，代表正在進行 DNS 設定。如果沒有就要注意一下。設定時間大概 40~60 min 會完成。

![#](/pics/201706/gandi_dash.png)


## Cloudflare
有了自訂網域名稱，而且也可以轉址但預設是 http，因此可以透過 Cloudflare 提供服務掛上 https。

先到 [Cloudflare](https://www.cloudflare.com/) 註冊一個帳號，接著會收到回傳信件，只要根據回傳信件內容到網站上面設定好網址。接著再將它提供的 dns 位置到 Gandi 去替換就完成囉。

設定完成時在 **overview** 畫面會顯示要你點擊測試，如果成功會顯示下面畫面：

![#](/pics/201706/Cloudflare_overview.png)

最後如果要成功掛上 https 需要針對瀏覽頁面設定 SSL 為 Flexible 才會顯示正確憑證，方法是在 Page rules 下增加一組 rules，以範例是指允許網域下所有頁面都透過 Flexible 認證方式：

![#](/pics/201706/Cloudflare_pagerules.png)

方法可以參考 [blog](https://blog.dmoon.tw/github-pages-with-free-ssl/)

這邊要注意，前面 Gandi 的 zone settings 都設定完成再來啟用 Cloudflare，接著再回去設定 DNS，不然你先設定 Cloudflare, 會吃到 Gandi 不對的 zone file 設定，導致 Cloudflare 的 DNS 參數不正確。一般來說應該會只有三個：

![#](/pics/201706/Cloudflare_DNS.png)


## Disqus 留言轉換
簡單來說 Disqus 判斷一篇留言方式是透過網址，因為我們將 url 轉換到新的網域名稱自然而然原本的留言就會失效。不過 Disqus 有出一個不錯的工具叫 **Migration Tools** 可以協助作轉換。

登入 Disqus 打入以下網址：
```
https://{disqus_name}.disqus.com/admin/discussions/migrate/
``` 
會顯示下圖 **Upload a URL map**:

![#](/pics/201706/disqus_migrations.png)

點進去之後點選 `you can download a CSV here.` 的按鈕，他會寄送一份 csv 檔案，接著叫照他的說明兩兩對照，舊在前新在後：

```
http://example.com/old-path/old/postb.html, http://example.com/new-path/new/postb.html
```

接著把改好的 csv 檔案上傳，根據網頁上是說最快 24hr 會全部轉換完成。但我只有 9 則留言，一下就轉換完成了 XD。

如果我寫的太簡陋看不懂，可以參考[這篇](http://iotchef.cc/posts/2015-10-14-disqus-url-mapper-to-correct-post-url.html)。


