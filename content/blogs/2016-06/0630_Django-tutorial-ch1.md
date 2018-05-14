--- 
Title: Django教學第一篇-專案與環境設定
Date: 2016-06-30 13:37:22
Tags: Coding, Django
Category: Django
Slug: Django-Tutorial-01
--- 

[GITHUB 專案連結](https://github.com/chairco/django-tutorial-borrow])

開始我們第一篇教學吧。一開始還是要感謝 TP 大大的教學文件，覺得一個好的文件遠比看了一堆東抄西抄的文件來的受用，那為什麼要重新寫一次，原因是記得以前讀過一本 羅傑斯(E.M.Rogers)所寫的管理書籍叫做 __創新的擴散__，大意是創新分了幾個階段，對於我而言接觸 Django 這樣的處理方法也想象成是一種創新，經過評估、試驗與採納。最後希望能夠把這樣一個好方法提供給大家。


### 環境說明
Django 要開啟一個新的專案主要有幾個步驟：

+ 建立虛擬環境
+ 建立 Django 專案
+ 建立 settings 資料夾與設定環境變數
+ 建立一個新的 APP
+ 開始開發程式

通常許多教學內容比較少談論到怎麼處理 Django 的環境變數與設定專案資料夾內的 `setting.py`，因為 Django 是透過專案內的 `wsgi.py` 這隻檔案把專案變成 WSGI 應用程式[^1]，打開 `wsgi.py` 的內容會發現它可以設定 `setting.py` 位置，並透過 `setting.py` 來處理專案的環境變數[^2]，因為這個方式，可以據此來切換不同模式例如 共同設定、開發模式與部署正式機設定[^3]。


### 專案說明
這次想做一個專案是類似借東西系統，因為有參與產品研發，在研發初期會有很多不同 Function Team 要借用產品進行驗證與測試，希望可以透過一個平台根據序號與目的填寫借用表單。

因為一個借用單可能一次包含很多產品需求，因此要能夠一張表單對應多個產品序號。


### 建立虛擬環境與設定 Django 環境變數
因為 Python 3.x 已經很成熟了，而且改正了很多 Python 2.x 煩人 [Unicode 問題]，過去第三方套件也逐漸支援，實在沒有不用的理由。最重要的是 Python 3.x 已經內建虛擬環境套件，可以更方便與本機端的套件庫做區隔。

在開發這個專案我們總會需要安裝不同套件，再來 Django 版本也不斷演進，為了不干擾其他專案建立一個虛擬環境 env 然後啟動它:

```
python3 -m venv env
source env/bin/activate
(env) 
```

這個指令會幫你建立一個 env 的虛擬環境變數（你可以命名為其它的名稱），這等於是建立一個全新的 python 3 環境，可以試試在終端機鍵入 `pip list` 指令，會發現原本機端套件都消失了。不過我習慣在這之前先 update 一下 pip 這個套件然後再進行 Django 的安裝。這個教學撰寫時 Django 已經演進到 1.9.7 版本，如果你還是習慣 1.8.x 版本記得安裝時指定一下 `pip install "django<1.9"`，但我喜歡 1.9.x 之後 admin 畫面所以就安裝最新版:

```
(env)pip install --upgrade pip
(env)pip install django
```

現在已經可以先建立一個 Django 專案，專案名稱我們就取名叫 borrow:

```
(env)django-admin startproject borrow
```

這個專案的結構會長這樣, borrow 專案內所產生的 borrow 資料夾放的就是專案的環境變數:

```
borrow
├── borrow
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

如之前所說，因為開發 Web 時會先在本機端開發，然後再把程式部署到正式機，需要處理環境變數。首先在這邊我會做簡單整理與歸納目前我看 3個教學分出的 2 種方法：

* 官方: 全部放在預設 setting.py
* TP: 建立 settings/ 再區分
* Django Girl: 全部放在預設 setting.py


其實就是建立一個 `settings` 資料夾再歸納不同的環境變數 `.py`。
所以接下來將 `settings.py` 移到 `settings` 資料夾並改名為 `base.py`。然後在 settings 目錄裡建立三個空白檔案：`__init__.py`、`local.py`、`production.py`:

```
(env)cd cd borrow/borrow
(env)mv settings.py ./settings/base.py
(env)touch __init__.py local.py production.py
```

最後專案結構就會像下面一樣:

```
borrow
├── borrow
│   ├── __init__.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

接下來照 TP 的解釋這三個新設定作用會是：

+ `base.py`：用來存放所有設定中共通的部分。
+ `local.py`：本機（開發機）用的設定。
+ `production.py`：正式部署到 production server 時用的設定。

新增內容到這 `local.py`:

```python
from .base import *

SECRET_KEY = '某個產生的 secret key 值，請自行代換'
DEBUG = True
```

修改 `base.py` 內容 mark `#SECRET_KEY` 和 `#DEBUG = True`, 並修改 `BASE_DIR` 如下:

`BASE_DIR` 這個內容是要傳回當前執行檔的所在路徑，因為多了一個 `settings` 資料夾，因此要再多一層 `os.path.dirname()` 這個很直覺。

```python
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '某個長串亂數值'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
```

寫到這邊，覺得前面那個 `os.path.dirname()` 說明得太含糊，順便解釋一下好了 `os.path.dirname()` 這個函式其實就是回傳 `os.path.split()` 的第一個元素。乾脆在 `settings` 底下建立一個 `test.py` 來驗證:

```
print(os.path.abspath(__file__))
/Users/chairco/OneDrive/SourceCode/django/allo/borrow/borrow/settings/test.py

print(os.path.split(os.path.abspath(__file__)))
('/Users/chairco/OneDrive/SourceCode/django/allo/borrow/borrow/settings', 'test.py')

print(os.path.dirname(os.path.abspath(__file__)))
/Users/chairco/OneDrive/SourceCode/django/allo/borrow/borrow/settings
```
* 第一個範例可以看到因為變數代入是 `__file__` 所以印出了 `test.py` 所在位置
* 第二個範例只是要告訴你 `os.path.split()` 就是把檔案位置和檔案名稱回傳一個 `iterator`, 第一個元素傳位置，第二個元素傳名稱
* 第三個範例就是告訴你多加一個 `os.path.dirname()` 就把檔案位置在上提一層，所以當多加一層目錄就要多一個 `os.path.dirname()` 來往上移動囉。

所以應該明白這一串長長的程式碼意思，夠直覺了吧。


最後來到比較重要部分，因為設定三個 `.py` 目的就是為了要區分本機開發環境與部署的環境，最前面我們有提到 Django 是透過一個 `wsgi.py` 來設定環境變數，打開的內容是長這樣滴:

```
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borrow.settings")

application = get_wsgi_application()
```

所以只要在目前的虛擬環境告訴 Django 目前開發端要使用的環境變數為 `local.py`, 接著到部署機器的環境將變數設定成 `production.py` 就完成我們想要區分本機端與部屬端的環境變數囉。

``` 
export DJANGO_SETTINGS_MODULE=borrow.settings.local
```

為了方便切換到這個虛擬環境，可以將上面設定環境變數寫入到我們虛擬環境的 `env/bin/activate` 但要記得切換到 env 目錄上一層在執行如下指令:

```
(env)echo export DJANGO_SETTINGS_MODULE=borrow.settings.local >> env/bin/activate
```
---

走到這邊大概 Django 的環境也設定差不多了，接下來我們處理一下資料庫的環境變數，就可以進入到第二篇的 APP 開發囉。

因為 Django 是一個 MVC 架構(正確來說是 MTV) 因此資料庫對 Django 來說是一個很重要的賣點，在 Django 稱資料庫這塊為 Model 因此我們會透過撰寫 app 內的 `models.py` 程式碼來與資料庫進行溝通。

Django 預設的資料庫為 SQLite 3，當然如果你喜歡 NoSQL 的 MongoDB，或是在 python 底下一直都很高使用率的 PostgreSQL 與關聯式資料庫的 MySQL 官方都有支援套件。所以如果你要用其他資料庫記得要用 `pip` 安裝合適的套件。

如同之前所說本機端和部署端可能用不同資料庫因此我們要將 `base.py` 內的資料庫設定移轉到 `local.py` 和 `production.py`。

Mark `base.py` 的這段設定:

```
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
```

然後將上面那段程式碼加入到 `local.py`(記得註解要拿掉)，接著我們做了幾個修改:

+ 修改資料庫位置: `os.path.join(os.path.dirname(BASE_DIR)`。這邊要做說明為什麼要把資料庫再往外移出一層原因是，這樣在做 source control 如 git 時就可以不用特別排除本機端機料庫檔案。
+ 修改資料庫名稱: `'borrow_db.sqlite3'`

最後修改後的 `local.py` 會長成這樣:

```
from .base import *

SECRET_KEY = '自行加入 secret key'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'borrow_db.sqlite3'),
    }
}
```

設定完成之後就可以做 migrate 來初始化資料庫了，所以我們切換路徑到 `manage.py` 底下然後執行:

```python
python manage.py migrate
```

如果出現類似像這樣錯誤畫面，確認一下你有沒有正確 export Django settings 的環境變數。可以再重複執行一下 `export DJANGO_SETTINGS_MODULE=borrow.settings.local` 

```
Traceback (most recent call last):
  File "manage.py", line 10, in <module>
    execute_from_command_line(sys.argv)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/core/management/__init__.py", line 353, in execute_from_command_line
    utility.execute()
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/core/management/__init__.py", line 345, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/core/management/__init__.py", line 195, in fetch_command
    klass = load_command_class(app_name, subcommand)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/core/management/__init__.py", line 39, in load_command_class
    module = import_module('%s.management.commands.%s' % (app_name, name))
  File "/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5/lib/python3.5/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 986, in _gcd_import
  File "<frozen importlib._bootstrap>", line 969, in _find_and_load
  File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 673, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 662, in exec_module
  File "<frozen importlib._bootstrap>", line 222, in _call_with_frames_removed
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/core/management/commands/migrate.py", line 16, in <module>
    from django.db.migrations.autodetector import MigrationAutodetector
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/autodetector.py", line 14, in <module>
    from django.db.migrations.questioner import MigrationQuestioner
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/questioner.py", line 12, in <module>
    from .loader import MigrationLoader
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/loader.py", line 10, in <module>
    from django.db.migrations.recorder import MigrationRecorder
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/recorder.py", line 12, in <module>
    class MigrationRecorder(object):
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/recorder.py", line 26, in MigrationRecorder
    class Migration(models.Model):
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/migrations/recorder.py", line 27, in Migration
    app = models.CharField(max_length=255)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/models/fields/__init__.py", line 1072, in __init__
    super(CharField, self).__init__(*args, **kwargs)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/db/models/fields/__init__.py", line 166, in __init__
    self.db_tablespace = db_tablespace or settings.DEFAULT_INDEX_TABLESPACE
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/conf/__init__.py", line 55, in __getattr__
    self._setup(name)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/conf/__init__.py", line 43, in _setup
    self._wrapped = Settings(settings_module)
  File "/Users/chairco/OneDrive/SourceCode/django/allo/env/lib/python3.5/site-packages/django/conf/__init__.py", line 120, in __init__
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
```

如果看到這個畫面恭喜你已經成功了（淚奔啊，怎麼一個設定要搞這麼久）

```
Operations to perform:
  Apply all migrations: sessions, auth, admin, contenttypes
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying sessions.0001_initial... OK
```

接著我可以開始執行指令啟動網站，確認一下是不是真的成功了

```python
python manage.py runserver
```

看到以下畫面:

```
Performing system checks...

System check identified no issues (0 silenced).
July 01, 2016 - 02:39:05
Django version 1.9.7, using settings 'borrow.settings.local'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

然後打開你的瀏覽器在網址列鍵入 `localhost:8000` 或是 `127.0.0.1:8000` 看到瀏覽器出現下面這個標題代表你已經成功啟動 Django，接下來我們將開始撰寫第一個 APP 來感受一下 Django 的魅力吧。

```
It worked!
Congratulations on your first Django-powered page.
```

這個專案目前已經放在 GITHUB [https://github.com/chairco/django-tutorial-borrow] 歡迎 clone 下來。



[^1]: WSGI的全寫是 Web Server Gateway Interface，它的發音有點像是 whiskey，它是Python定義網頁程式和伺服器溝通的介面。可以參考這一篇文章有很詳細說明[化整為零的次世代網頁開發標準: WSGI]

[^2]: [how-does-django-work] 很清楚說明 Django 的 wsgi.py 的關係。

[^3]: 網頁開發比較麻煩就是在本機端測試完成後部署到正式機需要不同的環境設定變數，身為開發者當然希望有更聰明與簡單的方式避免出錯，因此針對不同的需求區分環境變數是需要的。可以見此篇 [run-your-project]


[化整為零的次世代網頁開發標準: WSGI]: http://blog.ez2learn.com/2010/01/27/introduction-to-wsgi/

[how-does-django-work]: https://github.com/uranusjr/django-tutorial-for-programmers/blob/master/02-how-does-django-work.md

[run-your-project]: https://github.com/uranusjr/django-tutorial-for-programmers/blob/master/04-run-your-project.md

[Unicode 問題]: http://uranusjr.logdown.com/posts/2013/12/20/write-python-3-codes-that-run-on-the-python-2-interpreter

[https://github.com/chairco/django-tutorial-borrow]: https://github.com/chairco/django-tutorial-borrow



