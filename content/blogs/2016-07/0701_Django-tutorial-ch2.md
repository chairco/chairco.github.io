---
Title: Django教學第二篇-建立第一個APP(上)
Date: 2016-07-01 13:51:07
Tags: Coding, Django
Category: Django
Slug: Django-Tutorial-02-1
---

延續前一篇 [Django 教學第一篇-專案與環境設定] 一鼓作氣接著來開始建立第一個 APP 吧。

首先我們要先想像一下這個 APP 會包含哪些功能，然後我們會根據這些功能建立相對應的元件，接著根據這個架構規劃資料庫。我覺得一開始不要設計太複雜功能，先將主要框架給規劃出來，然後再根據這個架構疊床架屋慢慢開發。

一個借用系統應該會有幾個大功能，這每一個功能我們都希望是獨立的 APP，然後只有單一依賴性，原因是 Django 重視每個 APP 的獨立性，儘管你可以讓 a 這個 APP 去依賴 b (a depend on b, 有點像是在說以前的集合論，天雨地濕，地濕天不一定雨，胡扯一下) 但不要做出相互依賴關係。

所以我們會規劃三個 APP:

1. 使用者認證
2. 申請借用單
3. 自動傳送通知信件

### 建立 APP

開始動手的 APP 會先針對第二個申請借用單做開發，所以進入到 borrow 專案內用 `manage.py` 來建立一個新的 APP loans(名稱會用複數名, 原因是這個 APP 會管理很多借用需求單):

```python
(env)python manage.py startapp loans
```

增加一個新的 APP 後這個專案的結構就會長成這樣:

```
borrow
├── borrow
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   ├── urls.cpython-35.pyc
│   │   └── wsgi.cpython-35.pyc
│   ├── settings
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-35.pyc
│   │   │   ├── base.cpython-35.pyc
│   │   │   └── local.cpython-35.pyc
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── loans
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── manage.py
```

接著我們到 `settings/base.py` 下將這個 APP 加入到 `INSTALLED_APPS` 內告訴 Django 已經被加入。 APP 順序沒有一定，但因為 Django 的相依性是由上到下，所以習慣由上加下來[^1]。

```python
INSTALLED_APPS = (
    'loans',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
```

現在我們已經可以開始來規劃 loan's model 了。概念是希望使用者登入到系統並通過認證後可以填寫借用需求單，因此借用需求單應該會有兩個 table 一個 table 會儲存需求單( loan ), 另一張 table 會儲存機器( device )。因為一張 `loan` 可能會對應一到多台 `device`，因此這兩張 table 會是一個 1 對 多的關係:

```
|  loan    |           |  device  |
|----------|           |----------|
|  owner   |           |  ISN     |
|  purpose | 1 <---- n |  unit    |
|  menu    |           |  config  |

```
loan 的 table:

+ 兩個欄位和一個 Inlineform : `owner`, `purpose`, `menu` 有一個欄位指向 `device` 的 foreign key `ISN`，接著我們就可以開始撰寫 `models.py`。

```python
# loans/models.py
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Loan(models.Model):

    owner = models.CharField(
        max_length=100,
    )

    purpose = models.CharField(
        max_length=100,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')

    def __str__(self):
        return self.purpose

    @models.permalink
    def get_absolute_url(self):
        return reverse('loan_detail', kwargs={'pk': self.pk})


class Device(models.Model):

    loan = models.ForeignKey(
        'Loan',
        related_name='menu_items', 
        verbose_name=_('loan'),
    )

    config = models.CharField(
        max_length=10,
        blank=True, null=True,
    )

    unit_no = models.CharField(
        max_length=20,
        blank=True, null=True,
    )

    isn = models.CharField(
        max_length=20,
        blank=False, null=True,
        verbose_name=_('ISN'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def __str__(self):
        return self.isn

    @models.permalink
    def get_absolute_url(self):
        return ('device_detail', [self.pk])

```
這段 code 有點長。 照順序來說明:

+ Loan table 的兩個 fields: `owner` 和 `purpose`，都是 `CharField` 資料庫會以 `VARCHAR` 型別表示。
+ `created_at` 這個 fields 是自動產生，是希望這個表單能記錄建立的時間。
+ `def __str__(self):` 這是 python 轉換成字串的 hook。注意的點是 python 3.x 因為處理掉 Unicode 問題，在 python 2.x 要改成 `def __unicode__(self):`，不過我建議用 python 3.x 吧
+ `def get_absolute_url(self):` 和 @models.permalink 之後用到再說。
+ Device table 大同小異就不重複說了。

接著我們用 `makemigrations` 這個指令更新 `loans` 的 `models`

```python
(env)python manage.py makemigrations
```

```
Migrations for 'loans':
  0001_initial.py:
    - Create model Device
    - Create model Loan
    - Add field loan to device
```

看到上面畫面就代表已經將新增 Loan 與 Device 間的關聯訊息存並且放到 `migrations\0001_initial.py`。然後我們再執行寫入到 loans project 指令讓正式寫入資料庫內。

```python
(env)python manage.py migrate loans
```

當你看到這個畫面代表已經成功在資料庫建立 `Loan` 和 `Device` 兩個 table。

```
Operations to perform:
  Apply all migrations: loans
Running migrations:
  Rendering model states... DONE
  Applying loans.0001_initial... OK
```

###Django Admin

不過到現在為止我們還是很抽象的建立資料庫欄位，不過好在 Django 幫我們建立 Admin module，因此我們可以快速用 Admin 介面確認剛剛建立的資料庫欄位。首先要先建立一個 superuser 來做登入動作(帳號密碼都可以自訂，Email 可以按 return 鍵跳過):

```python
(env)python manage.py createsuperuser
Username (leave blank to use 'chairco'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

接著在瀏覽器網址列鍵入 `http://127.0.0.1:8000/admin/` 輸入帳號與密碼就可以看到漂亮的 Admin 畫面，但似乎還缺少了什麼呢？？

原來剛剛建立的 `Loan` 和 `Device` 表格都沒有顯示在畫面裡。原來還需要透過 `admin.py` 告訴 Admin module 要顯示哪些 table。

所以我們打開 Admin.py 輸入一些內容然後重新整理，剛剛的網頁就會看到兩個剛剛註冊的 table:

```python
# loans/admin.py
from django.contrib import admin

from .models import Loan, Device

#admin.site.register(Loan)
#admin.site.register(Device)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['owner', 'purpose', 'created_at']


@admin.register(Device)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['isn', 'unit_no', 'config']
```

上面這段 code 你會發現我註解掉兩行註冊 table 的程式碼，取代是兩個用 decorator 註冊的類別，因為如果只留下註解的兩行程式碼， admin 畫面只會顯示 model 內 `def __str__(self)` 所定義的回傳值，為了讓畫面豐富與彈性，這不過是是自行定義顯示畫面的一些技巧罷了。

看看例子就更清楚，上下兩張圖差異:

![django-tutorial-ch2-1-p1](/pics/201607/django-tutorial-ch2-1-p1.png)

![django-tutorial-ch2-1-p2](/pics/201607/django-tutorial-ch2-1-p2.png)


然後點選 ADD LOAN+ 開始嘗試增加一些資料玩玩看吧！

誒，有點怪！馬上就發現一個問題，這個需求一開始不是希望再開需求單時就能夠填寫機器的序號嗎？可是現在變成要到各自的表格去新增資料？ 沒關係這就是 Django Admin 強大的地方。

![django-tutorial-ch2-1-p3](/pics/201607/django-tutorial-ch2-1-p3.png)


說到這順便分享一下今年 PyCon TW 2016 有一個講題是[那些年，我用 Django Admin 接的案子]講者當年就是靠 Django Admin 這個模組就能做出接案網站，所以不要小看這個不起眼的小模組呢。

不過話題扯遠了，接下來我們將用模組內的 `inline admin` 將 `Device` 的 table 嵌入到 `Loan` 的 table。

```python
class DeviceInline(admin.TabularInline):
    model = Device
    extra = 1


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['owner', 'purpose', 'created_at']
    inlines = [DeviceInline]
```

上面我們新增一個類別叫做 `DeviceInline` 然後添加一個 inlines 的變數並且 assign 成為 `list` 且 `list` 內存放 `DeviceInline`。

接著我們重新整理下網頁，嘗試再一次新增一筆 Loan 資料。 這時 Device 已經會自動顯示在下方了。Jack 這真是太神了啦！

![django-tutorial-ch2-1-p4](/pics/201607/django-tutorial-ch2-1-p4.png)


---
那今天我們就先到這邊，下回待續囉。



[^1]: 關於這個觀點是 TP 大大提出，可以參考這篇內容 [django-apps]


[https://github.com/chairco/django-tutorial-borrow]: https://github.com/chairco/django-tutorial-borrow

[Django 教學第一篇-專案與環境設定]: /posts/2016/06/Django-Tutorial-01.html#Django-Tutorial-01

[django-apps]: https://github.com/uranusjr/django-tutorial-for-programmers/blob/master/05-django-apps.md

[那些年，我用 Django Admin 接的案子]: https://tw.pycon.org/2016/en-us/events/talk/69827266518974528/#speaker-content


