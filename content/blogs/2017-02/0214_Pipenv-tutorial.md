---
Title: Pipenv 使用教學
Date: 2017-02-14 09:59:40
Tags: Pipenv, Python
Category: Python
Slug: Pipenv tutorial
---

Pipenv 是一個整合 Pipfile, pip, virtualenv 的套件管理工具。

根據開發者得說法：

>Pipenv是一個實驗性項目，旨在將所有最好的包裝世界帶到Python世界。它將Pipfile，pip和virtualenv整合到一個單一的工具。


Python 目前開發環境已經非常成熟，各種類型的套件只要隨手一個 pip install 就信手拈來讓開發者省去很多力氣。再來 Python 的生態系裡不像 node js 有非常多的版本，目前 Pytchon 的生態系主要就分成兩個分支 Python 2.x 與 Python 3.x，簡單來講 Python 就是一個簡單易懂又容易的語言。

不過這不代表 Python 就不需要一個好的套件管理。至少 Python 在不同的 2.x 與 3.x 透過 six 這些套件完美的橋接不同的套件，但事實上在開發過程中我們有更多使用 Python 所開發的 framework，這些 framework 相依著很多不同的套件，例如 Django 有一個很棒的套件叫 `Django-Debug-Toolbar` 這個套件在 1.5 可以支援 Django 1.9.x 的版本，但當 Django 1.10.x 後一些 api 作了改變就壞掉惹！這時就必須要升到 `Django-Debug-Toolbar` 1.6 的版本。所以其實還是需要一個好的套件管理協助我們避免這種事情發生。

要怎麼安裝這個套件呢？首先還是先用 `pip` 來安裝 `pipenv` 這個套件。（如果有 py2.x, py3.x 只要在其中一個環境安裝就可以了）

Python 2.x:
`pip install pipenv`

Python 3.x:
`pip3 install pipenv`


安裝完成之後可以試試看在 commandline 下輸入 `pipenv` 就會輸出相關使用方法：

```
Usage: pipenv [OPTIONS] COMMAND [ARGS]...

Options:
  --where          Output project home information.
  --venv           Output virtualenv information.
  --rm             Remove the virtualenv.
  --bare           Minimal output.
  --three / --two  Use Python 3/2 when creating virtualenv.
  --python TEXT    Specify which version of Python virtualenv should use.
  -h, --help       Show this message then exit.
  --version        Show the version and exit.


Usage Examples:
   Create a new project using Python 3:
   $ pipenv --three

   Install all dependencies for a project (including dev):
   $ pipenv install --dev

   Create a lockfile:
   $ pipenv lock

Commands:
  check      Checks PEP 508 markers provided in Pipfile.
  install    Installs provided packages and adds them to...
  lock       Generates Pipfile.lock.
  run        Spawns a command installed into the...
  shell      Spawns a shell within the virtualenv.
  uninstall  Un-installs a provided package and removes it...
  update     Updates pip to latest version, uninstalls all...

```

然後管理的方法很簡單，只要執行 `pipenv --three` 就會在預設資料夾底下(mac: /Users/{username}/.virtualenvs) 建立一個和這個資料夾同名稱的虛擬環境。
接著你就可以試試透過 `pipenv install requests` 安裝 requests 這個套件。安裝完後你可以執行`cat Pipfile` 看內容如下，這時 `requests` 已經被記錄在 Pipfile 了。

```
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true

[packages]
requests = "*"
```

你可以看到安裝完成了，接著用 `pipenv lock` 鎖定 dependence，`cat Pipfile.lock` 看到內容會如下，你會看見他會產生一個 hash 值，這個值其實就是讓你這個虛擬環境下能保持 requests == 2.13 相依性。

```
{
    "default": {
        "requests": {
            "version": "==2.13.0",
            "hash": "sha256:1a720e8862a41aa22e339373b526f508ef0c8988baf48b84d3fc891a8e237efb"
        }
    },
    "develop": {},
    "_meta": {
        "sources": [
            {
                "url": "https://pypi.python.org/simple",
                "verify_ssl": true
            }
        ],
        "requires": {},
        "hash": {
            "sha256": "da2810af0c3b5333e0de2fce9bea2a228812e2014e5f5fe3b1c533badc6c24e4"
        }
    }
}%
```
最後如果要執行 Python shell 一樣透過 pipenv 輸入 `pipenv shell` 就能進去。（不過筆者不知道為什麼不行 ＠＠，至少上稿前還找不到原因。）

用很簡單篇幅介紹這個新的工具，如果有更多想參考可以到 [Pipenv 教學]。


***

更新在 6/19，用了一陣子 Pipenv 覺得實在太好用了。不過有一些 Pip 使用習慣轉換過來做些紀錄。

+ 要如何在 Pipfile 內新增從 github 下載安裝的套件？
執行：`pipenv install git+https://github.com/django/dango.git#egg=Django` 這邊和 pip 不同是網址後一定要加上 **.git#egg={套件名稱}**

+ 如果有 requirements.txt 時要怎麼自動轉換過去 Pipfile?
很簡單，只要在同一目錄底下執行: `pipenv install` 接著會顯示：`Requirements file found, instead of Pipfile! Converting...` 套件會花點時間將 requirements.txt 轉換成 Pipfile 格式（大約要三分鐘以上 QQ 沒有研究為什麼要這麼久）

+ 要怎麼在我的環境安裝 Pipfile 的套件呢？
執行: `pipenv install --dev` 接著輸入 `pipenv shell` 就完成囉。記得要退出時要執行 `exit`

+ `pipenv shell` 沒有反應
感覺像是環境變數問題，[issue#415](https://github.com/kennethreitz/pipenv/issues/415) 有人在聊但沒仔細看。現在是安裝完成後可以 `pipenv --venv` 然後直接手動去吃環境變數。有點蠢。


**2017-09-26 更新**: 後來找到原因，因為安裝 pyenv 導致，原因在 [issue#184](https://github.com/kennethreitz/pipenv/issues/184)。解決[方法](https://github.com/kennethreitz/pipenv/issues/237)):

+ `pipenv shell --compat`  或是

+ 在環境變數設定 `export PIPENV_SHELL_COMPAT=true`。



[Pipenv 教學]: http://docs.pipenv.org/en/latest/

