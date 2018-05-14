---
Title: Django教學第三篇-用CBV來做程式開發
Date: 2016-07-06 14:59:23
Tags: Coding, Django
Category: Django
Slug: Django-Tutorial-03
---

有了觀念之後，在撰寫程式過程中就會有一些很直覺的想法，面對繁瑣的流程也就比較容易駕輕就熟(好像學習數學的感覺啊)

這個教學也希望用這種方法來開發，畢竟一時間要搞懂所有的觀念與技術對多數人來說都比較困難，但做中學讓自己投入，就會像堆積木一樣慢慢把不足的知識補足。

回顧前面兩篇文章，其實我們已經把整個 Django 後端都建立起來。接下來就是將前端與後端做一個橋接，前端就像是一個動作流程，後端就是邏輯執行。

所以在回顧一下流程與程式邏輯:

```
1. 新增表單 -> [urls pattern 找到對應 view] -> [view 根據對應 template] -> [顯示 html]
2. 填寫表單 -> [view 根據 form 找到 model ] -> [ 印出對應欄位給使用者填寫 ] -> [如果有多筆 device， 按下增加按鈕就會透過 js 新增一個欄位給使用者填寫]
3. 送出表單 -> [view 會檢查欄位內容的型態是否正確] -> [正確就會存進資料庫] -> [網站轉址]
```

所以我們需要的程式邏輯應該會有:

+ Create, Add loan request: 新增表單
+ Edit, Update loan request: 編輯表單
+ Mixin both form: Loan and Device: Loan 和 Device 兩個 table 的 form 要合併在一起。

### 建立 view 與 form 取得資料

所以我們可以開始建立 view, 首先是新增表單的部分，不要忘記我們也希望使用者在新增表單同時也可以新增 Device 這時就需要透過 forms.py 來處理這個部分。

主程式會長這樣，`class LoanCreateView()` 會繼承 `FormsetMixin` 和 `Createview`，前面我們有提到這個繼承自 `django.views.generic` 的 class `Createview` 可以協助我們透過 `get_form` 產生 form class 再與 我們指定的 template_name 結合 response。

```python
#  loans/views.py
from django.views.generic import CreateView

from .models import Loan

from .forms import LoanForm, LoanFormSet

class LoanCreateView(FormsetMixin, CreateView):
    template_name = 'loans/loan_formset.html'
    model = Loan
    form_class = LoanForm
    formset_class = LoanFormSet
```

如果我們單純只是要處理某一個 table 並把裡面的 field 回傳 form 那大概到這邊就完成了，但因為我還想將 `Device` table 內的 field 也整併一起這時我們就需要做一些處理:

```python
class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
```

首先上面這段程式碼，是讓我們告訴 Django 有兩個 form, 一個是 Loan 的 form 一個是回傳自 `forms.py` 透過 `from django.forms.models import inlineformset_factory` 處理過後的 form，然後透過 `FormsetMixin` 將兩個 form 合併之後回傳。

至於 `forms.py` 是透過 `inlineformset_factory` 這個函式將 Loan 和 Device 做合併，然後可以設定一開始要印出的數量，還有需要填寫的 field。

```python
from django.forms.models import inlineformset_factory

LoanFormSet = inlineformset_factory(
    Loan, Device,
    extra=0,
    min_num=1,
    fields=('isn', 'config')
)
```

---

想不到今天有點拖太久先暫時停筆，等有時間再把內容做更詳細補完和說明吧 :)

---

好了，人有惰性，但拖稿也不能拖太久 XD

前面我們透過 `views.py` 和 `forms.py` 兩隻程式幫我們處理好後端整合兩個關聯性 table 的邏輯後，接著就可以透過前端撰寫 `html` 來處理 template 展現資料的方法。


### 透過 template 呈現畫面

首先我們在 `loans/templates/` 底下新增一個 html 檔案叫 `loan_formset.html` 這個 html。其實眼尖的朋友應該想起來 `views.py` 下面的 `class LoanCreateView(FormsetMixin, CreateView)` 一開始就有設定一個 `template_name` 就指向這個檔案位置，也就是說當我們呼叫 `class CreateView` 下的方法函式 `as.view()` 他自動會 response 一串 `dict` 內容給這個 `html`

所以我們開始編輯 `loan_formset.html`，一樣繼承 `loans/_base.html`。然後...

```html
{# loans/loan_formset.html #}
{% extends 'loans/_base.html' %}

{% load crispy_forms_tags %}

{% block title %}Loans Formset | {{ block.super }}{% endblock title %}

{% block link %}{{ block.super }}
    <style type="text/css">
    .errorlist {
        list-style: none;
        color: #B94A48;
        margin: 0px 0px 9px 0px;
        padding: 0px;
    }
    </style>
{% endblock link %}

{% block js %}{{ block.super }}
{% endblock js %}

{% block content %}

    <ul class="breadcrumb">
        {% block bar %}{{ block.super }}
            {% if object.purpose %}
                <li class="active">{{ object.purpose }}</li>
            {% else %}
                <li class="active">Loan edit</li>
            {% endif %}
        {% endblock bar %}
    </ul>

    <div class="page-header">
        <h1>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Loans and Device</h1>
    </div>

    <form action="." method="post">
        {{ formset.management_form }}
        {% csrf_token %}

        <legend>Loan</legend>
        <div class="Loan">
        {{ form|crispy }}

        </div>

        <legend>Device</legend>
        <div class="loans form-inline">
            {% for form in formset %}
                {{ form|crispy }}
            {% endfor %}
        </div>
        <hr></hr>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save</button>
        </div>
        <hr></hr>

    </form>

{% endblock content %}
```

等等啊，這裡出現一個疑問了。還記得我們在 `forms.py` 內設定 `LoanFomrset` 預設的值是 1 啊，那要怎樣讓使用者新增一個新的 field 來填寫呢？

沒錯，聰明的你應該已經想到了，就是 Javascript。不要忘記很多前端互動介面還是要仰賴 Javascript 來協助我們處理呢。

所以這段 js code 就會長成這樣:

```javascript
<script type="text/html" id="loan-template">
<div id="loan-__prefix__">
    {{ formset.empty_form|crispy }}
</div>
</script>

<script>
$(function() {
    $('.add-loan').click(function(ev){
        ev.preventDefault();
        var count = parseInt($('#id_menu_items-TOTAL_FORMS').attr('value'), 10);
        var tmplMarkup = $('#loan-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count)
        console.log(compiledTmpl);
        $('div.loans').append(compiledTmpl);
        $('#id_menu_items-TOTAL_FORMS').attr('value', count + 1);
    });
});
</script>
```
程式邏輯就是設定一個變數 `count` 然後當使用者觸發新增按鈕時，就會把 `count + 1` 然後根據這個 id 去新增一組 field。

同時我們也要新增一個按鈕讓使用者可以新增。所以這段程式碼的整合後樣子就會是這樣:

```html
{# loans/loan_formset.html #}
{% extends 'loans/_base.html' %}

{% load crispy_forms_tags %}

{% block title %}Loans Formset | {{ block.super }}{% endblock title %}

{% block link %}{{ block.super }}
    <style type="text/css">
    .errorlist {
        list-style: none;
        color: #B94A48;
        margin: 0px 0px 9px 0px;
        padding: 0px;
    }
    </style>
{% endblock link %}

{% block js %}{{ block.super }}
    {# js 位置 #}
    <script type="text/html" id="loan-template">
    <div id="loan-__prefix__">
        {{ formset.empty_form|crispy }}
    </div>
    </script>
    
    <script>
    $(function() {
        $('.add-loan').click(function(ev){
            ev.preventDefault();
            var count = parseInt($('#id_menu_items-TOTAL_FORMS').attr('value'), 10);
            var tmplMarkup = $('#loan-template').html();
            var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count)
            console.log(compiledTmpl);
            $('div.loans').append(compiledTmpl);
            $('#id_menu_items-TOTAL_FORMS').attr('value', count + 1);
        });
    });
    </script>

{% endblock js %}

{% block content %}

    <ul class="breadcrumb">
        {% block bar %}{{ block.super }}
            {% if object.purpose %}
                <li class="active">{{ object.purpose }}</li>
            {% else %}
                <li class="active">Loan edit</li>
            {% endif %}
        {% endblock bar %}
    </ul>

    <div class="page-header">
        <h1>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Loans and Device</h1>
    </div>

    <form action="." method="post">
        {{ formset.management_form }}
        {% csrf_token %}

        <legend>Loan</legend>
        <div class="Loan">
        {{ form|crispy }}
        </div>

        <legend>Device</legend>
        
        {# 按鈕位置 #}
        <div class="pull-right"><a href="#" class="btn btn-primary add-loan"><i class="icon-plus icon-white"></i>Add Device</a>
        </div>
        
        <div class="loans form-inline">
            {% for form in formset %}
                {{ form|crispy }}
            {% endfor %}
        </div>
        <hr></hr>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save</button>
        </div>
        <hr></hr>

    </form>

{% endblock content %}
```
然後 template 就完成囉，那接下來就是告訴 Django 的 WSGI 他要怎麼連到這個頁面。


### urls pattern 連接對應的頁面

這邊就簡單了，想像就像一個程式已經完成，你只是透過一個方法作為程式的進入點。所以我們就打開 `loans/urls.py`，輸入 `url(r'^add/$', views.LoanCreateView.as_view(), name='loan_add'),` 到 urlpatterns:

```python
# loans/urls.py
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.LoanList.as_view(), name='loan_list'),
    url(r'^(?P<pk>\d+)/$', views.LoanDetail.as_view(), name='loan_detail'),
    url(r'^add/$', views.LoanCreateView.as_view(), name='loan_add'),
]
```

不過這邊你一定有個疑問 `url(r'^(?P<pk>\d+)/$', views.LoanDetail.as_view(), name='loan_detail'),` 這段是幹什麼的啊？

因為我們希望當使用者輸入完成並也送出之後可以看到完成的畫面，有的會寫一個 html 只顯示已完成，但以我們這個範例是跳轉的完成表單的內容，所以回顧一下在 `views.py` 是哪一段程式碼幫我們處理？


```python
def form_valid(self, request, form, formset):        
    self.object = form.save()
    formset.instance = self.object
    formset.save()
    return redirect(self.object.get_absolute_url())
```

可以發現 `form_valid` 會幫我們確認 `field` 內容是否有符合規範，然後和建立一個 loan 和 device 的 `formset instance` 接著儲存。儲存之後會回傳 `get_absolute_url()` 這個函式，使用者的頁面就會轉換過去。但 `get_absolute_url()` 是？？？

因為 Django 是一個 MTV 架構，因此一些固定邏輯我們會希望在 Model 處理，所以我們打開 `models.py` 回顧一下當時我偷偷加的函式

找到 `class Loan` 的最下面就看到這個函式，我們透過 decorator `@models.permarlink` 可以直接呼叫 get_absolute_url()，不過別忘記提供 pk 參數，這樣才知道要取得哪一筆資料。
_寫這篇同時發現 2013 後 Django 不建議用 permalink 這個 decorator[^1]_

```python
@models.permalink
def get_absolute_url(self):
    #return reverse('loan_detail', kwargs={'pk': self.pk})
    return ('loan_detail', [self.pk])
```

然後再重複一遍開發流程 views -> template。所以在 views.py 建立一個 `class LoanDetail(DetailView)` 用來取得資料。嘿嘿，有發現用 CBV 好處了嗎？ 

```python
class LoanDetail(DetailView):

    model = Loan
```

然後再建立 `loans/loan_detail.html` 的 template。

> 這邊有人會問說可是在程式碼裡面都沒有告訴 `class LoanDetail(DetailView)` template 是在哪邊呀？ 這就是 `DetailView` 聰明的地方，在 class 內有一個 `get_context_data` 的方法函式預設的 template 內就是 **model 名稱轉小寫 + _detail.html** 當然你也可以用 `template_name` 來指定囉。

```html
{# loans/loan_detail.html #}
{% extends 'loans/_base.html' %}

{% block title %}Loans Detail | {{ block.super }}{% endblock title %}

{% block content %}

    <ul class="breadcrumb">
        {% block bar %}{{ block.super }}
            <li class="active">{{ object.purpose }}</li>
        {% endblock bar %}
    </ul>

    <div class="page-header">
        <a class="btn btn-primary pull-right" href="{% url 'loan_edit' pk=object.pk %}"><i class="icon-edit icon-white"></i>Edit</a>
        <h1>{{ object.purpose }}</h1>
    </div>

    <table class="table table-striped">
        <tr>
            <th>isn</th>
            <th>config</th>
            <th>unit no.</th>
        </tr>
        {% for item in object.menu_items.all %}
        <tr>
            <td>{{ item.isn }}</td>
            <td>{{ item.config }}</td>
            <td>{{ item.unit_no }}</td>
        </tr>
        {% endfor %}
    </table>

    <p>By {{ object.owner }}</p>

{% endblock content %}
```
最後我們打開瀏覽器輸入 `http://localhost:8000/loan/`

**頁面就會像下面這樣:**

![django-tutorial-ch3-p1](/pics/201607/django-tutorial-ch3-p1.png)

---

**新增頁面:**

![django-tutorial-ch3-p2](/pics/201607/django-tutorial-ch3-p2.png)

---

**新增多筆 Device:**

![django-tutorial-ch3-p3](/pics/201607/django-tutorial-ch3-p3.png)

---

寫到這邊不知不覺已經完成了所有功能，有沒有很興奮呢。
我想要在短短幾篇裡面講完所有重點真的是有點困難，不過好在現在用 __google__ 大神很容易，當你發現問題或是錯誤訊息時，嘗試尋找一下關鍵字，也許有人也犯過一樣錯誤而且解決了呢。

總之，內容肯定不夠完美，如果有不清楚地方再請包涵囉，那下一篇我們再來加點新功能吧！



[^1]: 目前建議是用 `from django.core.urlresolvers import reverse` 然後 回傳 reverse() 來取代 permalink [what-is-permalink-and-get-absolute-url-in-django]

[what-is-permalink-and-get-absolute-url-in-django]: http://stackoverflow.com/questions/13503645/what-is-permalink-and-get-absolute-url-in-django




