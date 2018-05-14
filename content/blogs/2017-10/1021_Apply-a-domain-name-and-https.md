---
Title: 個人網站申請一個網域名與掛上免費 https
Slug: Apply a domain name and https for personal websit
Date: 2017-10-21 14:20:38
Modified: 2017-10-21 14:20:38
Tags: Web, Gandi, Cloudflare 
Category: Web
---

> 前不久有寫過一篇文章 [Github.io 自訂網域名稱且透過 Cloudflare 申請免費 https](/posts/2017/06/Github.io%20Pages%20redirect%20to%20domain%20name%20and%20add%20HTTPS.html) 分享如何用免費的 Cloudflare 替網站掛上 HTTPS。

> 時隔一陣，我原始的網域名 **chairco.com.tw** 也到期了。掙扎很久再想到底要不要續約，但一直覺得用 `com.tw` 網域名稱來做個人網頁很怪(可能是太長吧)，但 `com` 又被買走，`tw` 有點狹隘感覺。既然網站是經驗分享，那就找個比較個人 style 的吧。所以 `me` 就成了我的選擇了。

> 不過重新購買過程出現小插曲，`Gandi`(網域名稱服務商) 似乎這一陣子改版了他們系統，原先是在一個稱為 [v4](https://v4.gandi.net/news/en/2012-10-23/798-gandi_v4_is_live/?lang=zh-hant) 網站上註冊與購買，但我透過他寄來提醒信連結到是 [v5](https://v5.gandi.net/zh-hant)。原本帳號無法通用在兩個系統，另外申請了一組帳號。結果一時不察在 v5 系統上用了後來新申請帳號購買，只好將錯就錯了。


> 新的網頁系統可能為了更人性化所以在流程與 UI 有調整，和舊的差距不小。因此再次記錄透過 Gandi 購買網域名稱和申請免費 https 的過程。


## 購買網域名

進到 Gandi v5 的新網頁如下，可以打你想要的網域名稱進行購買與註冊，範例我用 `g0v.tw` 來舉例。

![Imgur](https://i.imgur.com/6THSbpw.png)


因為 `g0v.tw` 已經被註冊了，所以推薦了幾個尚未註冊的網域名稱。不知道如何定價，但我猜應該就是根據市場上的熱度，比較有趣是 `cn` 網域似乎需要申請文件。

假設你選定了某個網域，就點選之後再按右上角購物車結帳。

![Imgur](https://i.imgur.com/WoE5j8f.png)


接著會進到購物車畫面。在這邊如果你有參加一些研討會例如：[PyCon TW](https://tw.pycon.org/2017/zh-hant/) 有 Gandi 贊助可能會得到一些第一年免費的序號，可以拿來用，但天下沒有白吃午餐，第二年開始通常就是恢復原價。如果有想要長期經營就選好選滿不要和我一樣。

確定好一些加值稅等就可以按下結帳。

![Imgur](https://i.imgur.com/i4Biyo0.png)


因為目前為止都尚未登入，所以可以登入你申請帳號或是重新申請一個新的。然後 v4 無法和 v5 共用帳號（無法理解原因？是因為當初申請的帳號比較特殊嗎？是 Gandi- 開頭的）

![Imgur](https://i.imgur.com/pJgE8em.png)


接著會請你輸入一些發票必要資訊（當然要輸入假的也行）我也不知道為什麼一定需要？不過我是輸入真實的，反正網站上遠本就透露這些訊息。

![Imgur](https://i.imgur.com/wMvlC61.png)


然後如果想試試 Gandi 的 Hosting 可以免費試用十天，個人是取消省得麻煩。接著就結帳付錢吧。

![Imgur](https://i.imgur.com/UKRPPV1.png)


完成之後可以進入管理介面，到左邊`域名`點選主畫面你剛剛購買的網域名稱來做設定吧。

![Imgur](https://i.imgur.com/wpB0jtZ.png)


## 轉址到網域名稱

因為我們的網頁是掛在 `github.io` 上，希望瀏覽器打入 `chairco.github.io` 時可以轉址到我們的網域名。這個步驟會許要做兩件事：

1. 設定 Gandi `區域設定檔`

2. 增加 CNAME 在主機上: 建立 CNAME 檔案在 `github.io` 的 `repo` 內。


### 設定區域設定檔

在`管理介面`點選`網域名稱`會看到如下面的圖。把原先的區域檔紀錄都刪除，增加三個。接著確認沒有打錯就儲存。

+ 名稱: a, ipv4: 192.30.252.153
+ 名稱: a, ipv4: 192.30.252.154
+ 名稱: CNAME, 主機名稱: {github 帳號}.github.io.


![Imgur](https://i.imgur.com/1Vb91tA.png)


### 主機上增加 CNAME 檔案

在 `github.io` 的 repo 內新增一個 CNAME 檔案，裡面就寫你的網域名稱，例如 `chairco.me`

![Imgur](https://i.imgur.com/3aEe3CB.png)


接著等一會兒吧（大概最快一分鐘），你在瀏覽器鍵入原本 `github.io` 網址就會成功轉址到你購買的新網域名稱上。恭喜你踏出第一步囉。接著開始設定 https。


## 掛載免費 HTTPS

不講太多 https 是什麼，google 一下 wiki 可能更清楚也不會偏誤。因為如果是自己的主機其實還挺容易的，但因為我們是掛載在 `github` 的主機，所以需要一些第三方服務，簡單說第三方服務的關係應該是：

```
【 Github.io 】<-->【 Gandi 】 <-->【 Cloudflare 】
```

所以概念上就不需要針對 `Github.io` 上的 repo 做任何事，只要讓 Cloudflare 能夠收到 Gandi 傳過來的封包，要做到這件事情就是要：

1. 設定 Cloudflare 上 DNS 和 Gandi 的區域設定檔案內容相同。

2. 設定 Gandi 的 DNS 是 Cloudflare 提供的位置。


假設你已經註冊了一個帳號，登入主畫面點選右上 `+Add site` 會看到下面畫面，就輸入網域名稱先讓 Cloudflare 偵測網域服務商 Gandi 的參數，偵測完成之後點選 `setup continue`。

![Imgur](https://i.imgur.com/9Si5Mlc.png)


通常可能會抓到錯誤的 Gandi 區域設定檔(要和前面我在設定一樣才對)，沒關係就等完成後再來修正。接著會問你要不要使用付費，點選免費後下一步。

![Imgur](https://i.imgur.com/0SgJJZk.png)


接著會偵測你目前的 DNS 並請你將網域名稱服務商提供的 DNS 改成 Cloudflare 以下兩個。

+ mario.ns.cloudflare.com

+ mira.ns.cloudflare.com

![Imgur](https://i.imgur.com/svNyeP2.png)


所以我們要回到 Gandi 的網站修改。點選`管理介面`內的網域名稱將原本的 DNS 修改，接著儲存後離開。

![Imgur](https://i.imgur.com/qJWTjCH.png)


接著完成所有程序，可以點選 `Recheckserver`(畫面裡被 google 翻譯的圖示擋住)。旁邊的描述有提到，最慢 SSL 的憑證可能會 24 hr 後生效。

![Imgur](https://i.imgur.com/Jb7coVG.png)


如果 Gandi 上的 DNS 有正確設定，那就會顯示如下面正確的圖示。

![Imgur](https://i.imgur.com/PzZdHq0.png)


最後一個步驟要設定 `page rules` 才允許網頁通過。如果沒有做這個設定那 Cloudflare 就不知道從 `chairco.me` 過來的網頁哪些要做 SSL 加密。

![Imgur](https://i.imgur.com/BfvjPpo.png) 


點選 Cloudflare 上 Page rules，接著輸入 `{網域名稱}/*`，因為全部通過所以用星號表示。

![Imgur](https://i.imgur.com/Oc4Wbvq.png)


就完成所有的程序了。以我的經驗應該頂多 30 mins 網站就會掛上 https。接著打開瀏覽器就開心地看到網頁上有憑證啦！

![Imgur](https://i.imgur.com/fDUFM88.png) 

