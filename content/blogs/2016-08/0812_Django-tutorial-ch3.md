---
Title: Django教學第三篇-用CBV做程式開發(續)
Date: 2016-08-12 09:48:38
Tags: Coding, Django
Category: Django
Slug: Django-Tutorial-03-2
---

接下來我們為系統加點功能，想想一個借用系統如果沒有權限控管就不容易追蹤使用系統的人和流程。所以我想為這個系統加上權限控管。

很棒的是 Django 本身就有權限管理功能，只要在 `borrow/urls.py` 加上 `url(r'^accounts/', include('django.contrib.auth.urls')),` 這個路徑就可以啟用登入的功能。所以現在 `borrow/borrow/urls.py` 這個檔案會長這樣：

```python
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from pages.views import index


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='home'),

    url(r'^loan/', include('loans.urls')),
    url(r'^faship/', include('faships.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
```


有了登入的 router 後接著要建立一個 login 的 template，所以在 `borrow/templates/` 先建立一個資料夾 `registration` 接著再到資料夾內建立一個 `login.html`。

`loging.html` 就是 `url(r'^accounts/', include('django.contrib.auth.urls'))` 的 template，打入這個路徑後就會顯示編輯頁面，內容像是這樣：

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block body %}
{{ block.super }}
<div class="container">
  <div class="row">
    <div class="col-lg-4 col-md-6 col-lg-offset-4 col-md-offset-3">
      <h2 class="form-signin-heading">Please Sign In</h2>
      <form method="post">
      {% csrf_token %}
      {{ form|crispy }}
      <button type="submit" class="btn btn-primary">登入</button>
      </form>
    </div>
  </div>
</div>
{% endblock body %}
```

一樣是繼承 base.html 然後用 crispy_forms_tags 來修飾我們的 form。比較特別是建立了一個 submit 的 button 來觸發行為。接著你可以試試看鍵入 [http://127.0.0.1:8000/accounts/login/] 就會顯示出類似下面的登入畫面

![django-tutorial-ch3-2-p1](/pics/201608/django-tutorial-ch3-2-p1.png)


有看到上面圖片右上角的登入畫面嗎？總是要有一個接入的端口，這時就需要在 `base.html` 裡的 `<nav>` 標籤裡再增加 `<div>` 的標籤。所以我們打開 `borrow/templates/base/base.html` 加一些東西，就會顯示登入的按鈕，試試看能不能用你在 admin 增加的帳號登入吧。

```html
...
<nav>
    <div>
        <form class="navbar-right navbar-form" method="post" action="{% url 'logout' %}">
            {% if user.is_authenticated %}
            {% csrf_token %}
            <input type="hidden" name="next" value="{% url 'home' %}">
            <button class="btn btn-default" type="submit">{{ user }} 登出</button>
            {% else %}
            <a class="btn btn-default" href="{% url 'login' %}">登入</a>
            {% endif %}
        </form>
    </div>
</nav>

```

不過到這邊還不夠，應該還要限制某些頁面需要登入後才能瀏覽對吧？通常用 FBV 來開發會很習慣在 views.py 內針對需要管理的頁面透過 decorator 來處理，例如：

```python
from django.contrib.auth.decorators import login_required

@login_required
def hello_world(request):
    return render(request, 'hello_world.html', {'current_time': datetime.now()})
```

不過因為用 CBV 來開發，這個方法可能就不適用。不過令人開心的是 login_required 這個 decorator 是可以透過將 CBV 的 as_view() 函式當作參數，一樣就可以實做這個功能。

那來實作一下吧，以這個範例需要登入才能動作應該是新增一個需求，所以到 `borrow/faships/urls.py` 找到新增的 router，將 login_required 當作一個函數，將 `views.FashipCreateView.as_view()` 傳遞進去。

```python
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    ...
    url(r'^add/$', login_required(views.FashipCreateView.as_view()), name='faship_add'),
    ...
]

```

試試看先把帳號登出，然後點選新增功能時 Django 是不是會自動幫你導到登入畫面呢？很棒吧，所有功能幾乎都幫我們開發好了，今天實做的功能幾乎都是在寫 html。


---


花了一點時間寫了這份教學，其實到這邊所學的 Django 也是進階再進階了，接下來其實就是閱讀更多的官方文件，加強 JS 和 CSS 照理說沒有做不出來的功能，當然這裡沒有教大家如何 deploy 到雲端平台，關於這個問題我想還是留給大家自我學習吧， Django girl 的官方網站是用 pythonanywhere，當然不僅僅只有這個，還有一樣棒的雲端平台，至於如何選擇就取決於你對於平台掌握度。

那這個主題就到這個段落，很歡迎大家提出問題一起討論，但我想這個只是我心裡的期待，不過還是希望當你讀過之後能幫助到你，不管是出於工作、興趣或是單純打發時間。

接著我將會寫些 python 的其他主題，也許會關於一些機器學習的部分(ML)。下回見吧。



[http://127.0.0.1:8000/accounts/login/]: http://127.0.0.1:8000/accounts/login/