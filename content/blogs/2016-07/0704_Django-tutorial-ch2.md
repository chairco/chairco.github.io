---
Title: Django教學第二篇-建立第一個APP(下)
Date: 2016-07-04 10:46:15
Tags: Coding, Django
Category: Django
Slug: Django-Tutorial-02-2
---

兩篇內容好像太長了，看了會有點辛苦。所以我把第二篇分成 2 篇。上篇建立了 model，也用了 Django 的 Admin module 讓我們可以手動建立資料，接著可以開始寫 views 讓使用者可以透過瀏覽器來操作這個 APP。

在開始動手寫程式之前要先瞭解一下 Django 這個 [MTV] 架構(Model-Template-View)。簡單來說在 Django 是使用 View 去取得哪一筆資料並透過 Template 決定怎麼呈現。


### 第一個頁面

首先先來設計一個 `base.html` 的 template。 因為我們希望每個 pages 儘量精簡，因此在 project 最外層資料夾建立一個 `templates/base/base.html` 讓所有頁面可以繼承它。然後同時也建立一個 `static/base/...` 來放一些 css、js 檔案

直接看結構吧:

```
borrow
├── borrow
│   ├── __init__.py
│   └── 略...
├── loans
│   ├── __init__.py
│   ├── 略...
│   └── templates
│       └── loans
│           ├── _base.html
│           └── home.html
├── static
│   └── base
│       ├── css
│       │   └── 略...
│       └── js
│           └── 略...
└── templates
    └── base
        └── base.html

```

做完之後很重要一點是要修改 `settings/base.py` 裡 `TEMPLATES` 變數告訴 Django 新的 templates 位置:

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
                    os.path.join(BASE_DIR, 'templates/base').replace('\\', '/'),
        ],
略...
``` 

然後也新增 `STATICFILES_DIRS` 變數讓 Django 知道 static 位置(這個 folder 用來放 css, js 的 檔案):

```
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```

前面我們有提到在 Django View 是用來取得資料並且用 Template 來呈現資料樣貌，所以接下來我們可以開發第一個 view 了，打開 loans/views.py，然後鍵入下面的 code，這段 code 就是建立 function home 然後印出 `home.html` 這個頁面:

```python
def home(request):
    return render(request, 'loans/home.html')
```

接著要讓 Django 透過 WSGI 來拜訪這個頁面，因次我們打開 `borrow/urls.py` 來設定 routing 的位置:

```
from loans.views import home

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
]
```

Django 是用正規表達式( Regular Expression )來處理所有 urls pattern 的 routing, ，因此只要告訴 urls pattern function home 的位置就可以了囉。

但突然想起一件事，還沒有建立 template 呀！對，這才要回應前面第一段目的，在這邊我們的繼承關係會是這樣:

```
 templates/base/base.html
         ＾
         ｜       
 loans/templates/loans/_base.html 
         ＾
         ｜ 
 loans/templates/loans/home.html 
```

有點繁瑣，講一下概念:

+ `templates/base/base.html`: 所有 app 網頁的 base，像 nav 等物件都放在這邊。
+ `loans/templates/loans/_base.html`: 這是每一個 app 的 base，這邊可以設定 `<body></body>`
+ `loans/templates/loans/home.html `: 實際處理內容的 template

所以 template 的 code 會長成這樣:

```
{# base/base.html #}
{% load staticfiles %}

<!DOCTYPE html>
<html>
<head>
<title>{% block title %}物品借用系統{% endblock title %}</title>
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
</head>

<body>

{% block body %}
<nav class="navbar navbar-default navbar-static-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="{% url 'home' %}">物品借用系統</a>
    </div>
  </div>
</nav>
{% endblock body %}

<script src="//code.jquery.com/jquery-2.1.1.min.js"></script>
<script src="{% static 'base/js/base.js' %}"></script>
{% block js %}{% endblock js %}

</body>
</html>

```

```
{# loans/_base.html #}
{% extends 'base.html' %}

{% block body %}
{{ block.super }}
<div class="container">{% block content %}{% endblock content %}</div>
{% endblock body %}
```

```
{# loans/home.html #}
{% extends 'loans/_base.html' %}

{% block content %}
{% endblock content %}
```

輸入 `http://localhost:8000/` 看看是不是跑出畫面了呢？

![django-tutorial-ch2-2-p1](/pics/201607/django-tutorial-ch2-2-p1.png)


---

有一點成就感了嗎？ 其實 Django 架構真的很複雜，第一次總會遇到些問題打擊信心，但一步步慢慢來總是可以學會。然後隨著架構愈趨複雜你會發現這些前置步驟的重要性。

先喘一下，我們會加快腳步用最快速度把第一個系統建立起來囉。

---

### 進入開發第一步

打鐵要趁熱，接下來我們要建立一個借用系統表單流程，這個流程的使用者情境 (user story) 應該會是這樣:

```
新增表單 -> 填寫表單 -> 送出表單
```

但對於系統開發流程大體來說會是這樣:

```
1. 新增表單 -> [urls pattern 找到對應 view] -> [view 根據對應 template] -> [顯示 html]
2. 填寫表單 -> [view 根據 form 找到 model ] -> [ 印出對應欄位給使用者填寫 ] -> [如果有多筆 device， 按下增加按鈕就會透過 js 新增一個欄位給使用者填寫]
3. 送出表單 -> [view 會檢查欄位內容的型態是否正確] -> [正確就會存進資料庫] -> [網站轉址]
```

所以我們在開發順序的思維就會是

+ 建立 view (當需要輸入資料庫就需要編輯 form)
+ 透過 template 呈現畫面
+ urls pattern 告訴 django 連接對應的頁面

還記得一開始時我們在 admin module 建立了幾筆資料嗎？ 那就先從印出資料畫面著手吧，首先打開 `loans/views.py`。

這邊會捨棄 FBV(Function-Based-View) 直接用 CBV(Class-Based-View) 來做開發[^1]，程式碼會長這樣:

```python
#  loans/views.py
from django.views.generic import ListView

from .models import Loan

class LoanList(ListView):

    model = Loan

```

你沒看錯，就短短的幾行這就是 CBV 威力。我們透過繼承 `ListView` 這個 class，然後呼叫 as_view() 這個 function 印出 model 內所有值[^3]。

接著就是撰寫 template 來呈現資料樣貌，所以我們在 `loans/templates/loans/` 底下新增一個 `loan_list.html` 然後裡面的程式碼如下:

```python
{# loans/loan_list.html #}
{% extends 'loans/_base.html' %}

{% block title %}Loans | {{ block.super }}{% endblock title %}

{% block content %}
    <div class="page-header">
        <a class="btn btn-primary pull-right" href="{% url 'loan_add' %}">Add Loan Request</a>
        <h1>Loan List</h1>
    </div>

    <table class="table table-striped">
        <tr>
            <th>#</th>
            <th>purpose</th>
            <th>owner</th>
            <th>created_at</th>
        </tr>
        {% for object in object_list %}
        <tr>
            <td>{{ object.id }}</td>
            <td><a href="{{ object.get_absolute_url }}">{{ object.purpose }}</a></td>
            <td><a href="#">{{ object.owner }}</a></td>
            <td>{{ object.created_at }}</td>
        </tr>
        {% endfor %}
    </table>
{% endblock content %}
```

首先不要忘記繼承 `loans/_base.html` 這個 template，然後在 `{% block content %}{% endblock content %}` 的內容之間撰寫 HTML 的程式碼。

這個頁面我希望用表格方式顯示，所以用 for 迴圈把從 `views.py` 內取得的回傳得值 `object_list` 資料印出來。

其中一行程式碼 `{% url 'loan_add' %}` 要先改成 `#` 因為 `loan_add` 是我們在 urls pattern 可用來代換的名稱，因為當我們有一天修改 urls pattern 裡對應 `views.py` 的函式時，就不需要再去修改 template 內的超連結網址囉。

但是目前在 urls pattern 內還沒有這個名稱，所以我們就先用 `#` 來代替，不然網頁執行就會因為找不到名稱而出錯。

最後只要在 urls.py 建立 pattern。先跳出來說明，Django 專案建立時會在專案名稱目錄下產生一個 `urls.py` 以這個範例來看就是位於環境變數的資料夾底下 `borrow/urls.py`。

但你要想想，一個專案可能有很多 APP，而這些 APP 可能有一些類似功能，我們總不希望把所有 pattern 扁平化吧？還是希望分層，如果根據 APP 名稱會是不錯的方法。因此一個網站的分類就會如下:

```
localhost:8000/
localhost:8000/aaa/list
localhost:8000/bbb/list
```

所以有這個觀念後就在 `loans/` 路徑底下建立一個 `urls.py`，所以你看到的結構會是這樣

```
borrow
├── borrow
│   ├── __init__.py
│   ├── 略...
│   ├── urls.py
│   └── wsgi.py
└── loans
    ├── __init__.py
    ├── 略...
    ├── urls.py
    └── views.py

```

所以我們要在 `borrow/urls.py` 告訴他 APP loans 的位置，然後再到 `loans/urls.py` 設定 `loan_list`

```python
# borrow/urls.py
from django.conf.urls import include, url
from django.contrib import admin
from loans.views import home


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loan/', include('loans.urls')),
    url(r'^$', home, name='home'),
]
```  

```python
# loans/urls.py
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.LoanList.as_view(), name='loan_list'),
]
```

設定完之後，我們打開瀏覽器打入網址 `http://localhost:8000/loan/` 看看是不是輸入的資料都跑出來了呢？

![django-tutorial-ch2-2-p2](/pics/201607/django-tutorial-ch2-2-p2.png)


哇，有沒有發現其實開發網頁並沒有想像中的困難嘛，接下來我們就照著這樣的開發思維接著進入下一個流程，建立一個頁面讓使用者可以填單囉。(再複習一次):

+ 建立 view (當需要輸入資料庫就需要編輯 form)
+ 透過 template 呈現畫面
+ urls pattern 告訴 django 連接對應的頁面

教學還是有點冗長，但已經陳述了一個基本的開發流程。
接下來我們要正式進入第三篇 _建立 MODEL 和用 CBV 來做程式開發_ 把我們的第一個 Django 網站建立起來！



[^1]: 使用過 Class 類別都知道在開發程式碼時有時我們會儘量避免重複的程式碼一直出現，在 python 裡有一個格言是 there should be one—and preferably only one—obvious way to do it[^2] 中文翻譯 "用一種方法，最好是只有一種方法來做一件事"。 CBV 就是用繼承方式避免重複的程式碼不斷發生，可參考 TP 這一篇 [class-based-view]。

[^2]: Peters, Tim (19 August 2004). [PEP 20 – The Zen of Python]. Python Enhancement Proposals. Python Software Foundation. Retrieved 24 November 2008.

[^3]: 關於詳細的實作可以參考 [ccbv ListView]


[MTV]: http://mropengate.blogspot.tw/2015/08/mvcdjangomtv.html "MTV(Model-Template-View)"

[class-based-view]: https://github.com/uranusjr/django-tutorial-for-programmers/blob/master/19-class-based-view.md

[PEP 20 – The Zen of Python]: https://www.python.org/dev/peps/pep-0020/

[ccbv ListView]: http://ccbv.co.uk/projects/Django/1.9/django.views.generic.list/ListView/