---
Title: OSX 使用 brew 安裝指定 Python3 版本
Slug: installed specific Python3 version with brew in OSX
Date: 2017-07-24 09:37:39
Tags: brew
Category: Python

---

brew 改版前如果要安裝指定版本，例如 `Python 3.5.2_3`:

```shell
#列出 <formula> 所有版本
$ brew versions <formula>

#安裝某個指定版本
$ brew install <formula>
```

改版之後這個功能似乎被拿掉了，官方上面有說明可以改成：

>How do I install these formulae?
>Just brew tap homebrew/versions and then brew install.
>If the formula conflicts with one from homebrew/core or another tap, you can brew install homebrew/versions/.
>You can also install via URL:
>brew install https://raw.githubusercontent.com/Homebrew/homebrew-versions/master/.rb

這樣看起來還是只能區分 Python2 or Python3 沒辦法決定要安裝 Python3 的哪個版本。（謎之音：以前那個好像也不行噎。啊！抱頭）


後來查到一個解決方法，也很簡單，因為 brew 是透過 .rb 管理安裝，再透過 git 管理 .rb 套件版本，所以只要能夠用 git 去切換 .rb 歷程就解決了。 
但在此之前需要取得 homebrew/version 底下的 formula 版本，這樣才能手動切換：

```shell
$ brew tap homebrew/versions`
```

接著到 `/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula` (or cd `brew --prefix`)


來到這個資料夾底下就有所有套件的 .rb，這些 .rb 就是用來安裝不同 formula。用 git 指令列出 python3 commit 歷程：

```
git log python3.rb
```

會顯示類似：

```
commit b1f976bb3c76bbb2a8d76cf46fea8b2c2235f631
Author: BrewTestBot <brew-test-bot@googlegroups.com>
Date:   Mon Jul 17 16:06:58 2017 +0000

    python3: update 3.6.2 bottle.

commit 77f4ca91f509f9379842f23fa945e3d7be86039a
Author: ilovezfs <ilovezfs@icloud.com>
Date:   Mon Jul 17 08:40:36 2017 -0700

    python3 3.6.2

    Closes #15704.

    Signed-off-by: ilovezfs <ilovezfs@icloud.com>
```

接著回到你要的版本。例如我想回到 3.5.2_3，就：

```
git checkout ec545d45d4512 python3.rb
``` 

接著再重新 `brew install python3` 完成安裝了


***
參考：

+ 第一篇 [specific software with brew](http://blog.juxi.net/index.php/2016/05/05/installing-a-specific-software-version-with-brew/)

+ 第二篇 [brew 安裝特定版本套件](https://blog.kuoe0.tw/posts/2013/04/19/install-formula-of-specific-version-with-homebrew/)