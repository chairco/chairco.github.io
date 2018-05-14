---
Title: 讓我們來談談 Django apps 上的測試吧
Slug: Let’s talk about testing Django apps
Date: 2017-07-20 15:39:46
Tags: Django, testing
Category: Django 

---


>好的測試設定帶你上天堂，不好的測試設定讓你手動到離不開機房。

>今天翻譯 Django 了一篇測試的文章，[原文在此](http://www.b-list.org/weblog/2017/apr/03/testing-django-apps/?utm_content=bufferca6f9&utm_medium=social&utm_source=facebook.com&utm_campaign=buffer) 

>文章大概在說明測試 Django apps 的一些設定概念、工具與經驗。希望想多瞭解一些 Django apps 的測試設定朋友會有興趣。

>不過譯者後來發現這位作者原創的做法後來被自己翻盤了（他原本想用 `Makefile` 做到完美的測試設定，後來還是回到他最不想要的 `tox`。好吧，來看看他遭遇的困境與經驗也不錯啊！）

***


至今有段時間，我維護[幾個 Django 的開源應用程式](http://www.b-list.org/projects/)。在不久的將來會兼容 Django 1.11，也是時候我要進行一些改變然後順便一起清理掉掛在 issue 上的問題，這樣我才可以繼續推出新的兼容官方的版本。當開始進行時，我總是喜歡嘗試評估是否可以在目前最佳的技術狀況下轉換成成更好的執行方式，由於 Django 在每個版本發佈時都會有新的功能，社群的朋友也會不斷提出更好的方法來處理常見的一些常見任務或是問題。


最近，一直在我腦海裡的一件事是測試。我是一個測試粉（譯者：在軟體裡有派 TDD 喜歡所有的 future 都要有測試，可能是這種粉絲吧），同時我自己個人的 apps 我都有做 CI 設定，針對維護的 `Django/Python` 版本完整的組合矩陣，當每一次 pull request 和每一次的 push commit 。我也使用 [coverage.py](https://coverage.readthedocs.io/)，當測試涵蓋率低於 100% 就會停止軟體的建置。


到目前為止一切都很棒。當然， Django 本身也支援[許多 built-in 工具來讓測試更為容易和美好](https://docs.djangoproject.com/en/dev/topics/testing/tools/)。


但我仍舊覺得要讓 Django 的測試做得更好，最好的測試模式是分成一區塊，所以讓我們來看看一些通點。


##Testing apps


假如你正在建置了一個 Django 的網站，你會希望這一堆的 apps 有它們各自的測試，然後並列在 `INSTALLED_APPS`（譯者：INSTALLED_APPS 是一個參數設定讓 Django 知道有哪些 apps），接著測試會很簡單：只需要 run `manage.py test`。你也可以在命令列上透過參數傳遞來執行一個應用程式的測試，或是執行一個子集合的測試。


但測試應用程序的層級怎麼辦呢？ Django 應用程序需要設置可用，是為了可以做任何事，你的這些特殊設定對應用程序並非層及。再一次說，假如你僅僅只是建立一個 app 並且將發布 並且整合進入一個單一網站或是多個服務，這不會是個很大的阻礙，你可以有個更大型的設置來進行測試，但假如這裡指的是一個分散式程序且在許多地方被重複使用呢？


對此，你需要提供 Django 可以運行的一個最小配置設定，接著執行你的測試。我已經增加一個稱為 `runtests.py` 的檔案到我的應用程序內，包含測試應用程序所需要的配置，和適當的呼叫來執行測試。[這裡提供一個 django-registrtion 範例](https://github.com/ubernostrum/django-registration/blob/master/registration/runtests.py); 透過 checkout 將程式碼拉下來 (譯者: git clone 網址)，或是解壓縮一個發佈的 package (譯者：github 可以透過下載方式取得壓縮的 package)，你就可以執行 `python runtests.py` 接著就會開始工作了。


Django 內建置了兩個功能：一個是 `django.conf.settings.configure()`, 這個功能讓你的函式提供你使用 `settings` 內的參數關鍵字，也就不需要建立設定檔或是 `DJANGO_SETTING_MODULE` 變數; 另一個是 `django.setup()`, 這個函式則是允許你 (在設定配置後) 初始化安裝的應用程式並且讓 Django 可以使用。一旦你完成這兩件事，你就可以實例化一個測試器，並且使用它去執行測試; 這以上都是 `run_tests()` 鏈結的文件。


這就能根據所需運作測試，但當然這裡（至少）有一個以上的問題被遺留需要被解答：人們如何呼叫它？這個簡單的問題答案是：`python runtests.py`，當然，也能使用 `converage run runtests.py` 來執行並且做到覆蓋率的支持。但會感覺到有一些些特別。


##Testing with setuptools


Python 的標準函式庫包含 `distutils` 模組用來建置和運作包裝後的 Python code。它也是 [setuptools](https://setuptools.readthedocs.io/)，用來開始進行許多重要的事（有雄心壯志）。目前，用 `setuptools` 提供一些常見對於 packaging-related 相當便利，其中一項很方便的就是在 `setup.py` 指定 `test_suite` 參數到 `setup()` 函式。假如你這樣做，這樣就可以透過 `python setup.py test` 指令來執行你的測試。舉個例：如果要測試 django-registration 可以透過 `setup.py` 內撰寫指令 `test_suite=registration.runtests.run_tests` 接著執行 `python setup.py test` (或是 `converage run setup.py test`) 可以作為宣傳測試指令使用，也可以定義在 CI 的參數檔案。


這感覺起來很不錯，只要告訴人們執行一個在 repository/package 內的 random scripy: 它使用一個 standard-ish 的 Python 模組（假如有 `pip`，那你也會有 `setuptools`），它是掛接標準 package-related 的 Python 命令列，且是很多 packages 可以做的事。所以 `python setup.py test` 是讓人們學習只做一件事且一次又一次的做。


但這裡有件沒提到的事。一方面來說你還是得有一個現成能夠執行測試的環境。對一個 Django 應用程式，代表至少需要一個可以支援 Django 和 Python 的版本環境。你可以做出很多個 `setuptools`，當然：你可以對每個 `install_requires` 和  `python_requires` 做定義告訴環境要使用哪種版本的 Django 和 Python 來支援。 接著 `setuptools` 將會安裝你指定的 Django 版本，但萬一你使用到不支援的 Python 對應版本的則會暫緩安裝。你甚至可以進步指定 `test_require` 來確保測試的可用相依性（在我的案例，converage 和 [flake8](http://flake8.pycqa.org/)）


然而，這只能針對已知且支持的 Python 與 Django 版本進行測試。假如 - 有非常多人同時測試 - 你會希望測試引擎能夠包含支援所有的 Python/Django 版本？


##Aside: tox


我不會去使用 [tox](https://tox.readthedocs.io/)，應該要在這邊暫停一下。這並非 `tox` 很糟或是有問題 - 我知道很多 folks 非常喜歡使用它 - 是因為 tox 不太適合我個人。我經常使用 [pyenv](https://github.com/pyenv/pyenv) 和 [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) 來管理各種不同版本的 Python 並切換、建立與使用 `virtualenvs` 不同的 Python 版本在我個人筆電上。


不過 `tox` 看起來似乎在這部分沒有運作得很好; 它希望能在不同 Python 版本找到一個共同的 Python 直譯器，每一次都需要透過手動竄改 `PATH` 將 `pyenv` 的直譯器安裝到 `tox` 找得到的位置（我也嘗試過 [tox-pyenv](https://pypi.python.org/pypi/tox-pyenv/1.0.3)，但仍然無法不讓 `tox` 根據 `PATH` 來尋找）。


假如你的本機端僅只有安裝一個版本，那 tox 會工作的很順利，或是你覺得可以讓 `tox` 來做 `PATH` 搜尋和 `pyenv` 一起運作，我會鼓勵你使用 `tox` 來進行測試。下面我將詳細介紹部分在本地端使用 `tox` 測試，但某種程度可以自動與 `pyenv` 一起工作。


##Go ahead, make my tests


最近我正在嘗試一些比較古早的東西。雖然 `python setup.py test` 這個測試執行指令是個很不錯的 Python-specific 標準，它仍然僅屬於 Python 特定。這裡有一個更古早且無關於語言可方法來做測試：`make test`。


在 Unix 世界，[make](https://en.wikipedia.org/wiki/Make_(software)) 是一個極為古老用來進行建立軟體的自動化流程方法。它的原生想法來自於圍繞在會發生的指定的任務，且相依於它們，接者呼叫需要運作的任何任務。在原生的案例，將會編譯 C 的資源檔接著鏈結它們並建立一個最終執行檔，但這不代表你必須要使用 C - 這是一個通用的工具。


任務 - 在 `make` lingo 稱為 “目標” - 是一個特殊的檔案，通常被稱之為 Makefile。每個目標都會成為傳遞給 `make` 命令的名稱，並且可以讓任何目標間指定相依的關係，以確保它們先發生。


假如你曾經手動使用 [Sphinx](http://www.sphinx-doc.org/) 建置文件（Sphinx 是個好東西 - 你應該使用它來做文件！），代表你曾經使用過，因為 Sphinx 生成一個 `Makefile` 來協調建構不同任務。假如你希望 HTML 文件，舉例，你就執行 `make html`，就會呼叫 `Makefile` 其中一個目標來執行所有必須的步驟從你的來源文件檔案去生成一個 HTML。 


在許多領域，`make test` 是一個預期用來執行 codebase 測試的標準方法。你需要做的只是提供 `test` 的目標在 `Makefile`，接著它就會根據正確的指令去執行。


所以我建立一個 `Makefile` 來開始進行我想要的測試。以下有幾間是需要知道：


+ 在一個 `Makefile` 中，你可以設置用來測試的變量。你可以在命令列或是設置環境變數來傳遞變量。

+ 在每個 `make` 目標中，每條指令都是一條邏輯。這代表假如你需要講一條指令分散成數條，你需要使用一個反斜線讓不同的行間的數條指令被視為同一個邏輯指令。

+ 每條邏輯行都是一個指令會被執行，所以它必須是符合 Bash-script-like 的風格，你可以使用 Bash 測試（像是確認某個 檔案/資料夾 是否存在）同時以邏輯運算來控制怎樣運行。

+ 通常， `Makefile` 的每個目標都會描述如何編譯/建構相同名稱的目標檔案。你可以使用 `.PHONY` 來聲明哪些名稱是不符合規範的。 


所以[這邊有個 django-registration 的範例](https://github.com/ubernostrum/django-registration/tree/58c7e8bdb9d2312277f3c3bdc129187353e59ea1)(譯者：後來文章作者好像拿掉使用 Makefile 來做測試，改用 tox)
。它允許使用參數的 Python/Django 版本，這代表他可以在一個循環中確認版本組合。這裡很重要的目標有：

+ venv 是使用 `pyenv` 來建立與啟用一個 virtualenv 來對應目標的 Python 版本。同時預設 virtualenv 名稱為 `registration_test`。假如一個 virtualenv 已存在同樣名稱，會忽略並且使用既有的 virtualenv 且不會管 Python 使用的版本為和。 

+ `lint` 會在 codebase 上執行 `flake8`，來確認 Python 風格是否有錯誤。

+ 根據涵蓋率在 test suite 執行測試，並且印出涵蓋率報表。

+ `testdown` 會在之後清除並且刪除 virtualenv


這裡有一些目標要執行像是安裝測試相依的檔案，安裝需要的 Django 版本等。所以現在我可以在我的 CI 設定檔案內指定 `make test` 為指令，並且知道要安裝哪些相依檔案（之前我不得不手動安裝或是使用 `test_requires`），對於本地測試我可以指定任何我想要的 Django/Python 版本組合。舉個例，執行 Django 1.9 與 Python 3.5.2:


```shell
$ make venv test teardown PYTHON_VERSION=3.5.2 DJANGO_VERSION=1.9
```


當然，這其實還只是個實現，這裡會有幾件事我想修好它。現在幾個比較大的問題：


+ 指定安裝 Django 版本。不幸的是，Python 上的符號使用方法並非我想要的，所以這邊我用一些黑客的方法在 `Makefile` 內的連結，確保我是指定 “1.8” 或是 “1.9”，但實際上他們都是安裝最近版本（簡短版本像是 Django~=1.9 將會安裝 Django 1.10, 但是 Django~=1.9.0 就會安裝最近的 1.9）


+ 清理。我在 `Makefile` 做了幾次複製/貼上在儲藏庫中用來執行刪除 `__pycache__` 資料夾和 `.pyc` 檔案。需要做些調整來處理深入程式碼的目錄(django-registration，例如，要深入目錄幾層)


+ 有些重複使用的問題，目前 `Makefile` 設定使用 `pyenv`，但我知道並不是每個人都使用 `pyenv`。目前，依賴 virtualenv 是設置為選項，人們可以選擇使用他們想要的環境而不必使用 `pyenv`。


## The future


我可能繼續修改 `Makefile` 一段時間，至少我個人應用程式，如果可以解決上面的問題我會繼續下去。但如果沒有我可能就會回到 `setup.py test`，或是探索看看其他選項（或是屈服在 `tox` 下）


在這個期間，我對於嘗試其他方法很感興趣; 我還沒有嘗試任何科學或是偽科學上的關於 Django 流行的應用程序調查來看看是否有其他獨立的測試應用的共識。
