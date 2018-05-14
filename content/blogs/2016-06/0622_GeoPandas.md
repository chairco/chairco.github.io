---
Title: GeoPandas and Taiwan CRS以高雄腳踏車道做簡介
Date: 2016-06-23 09:00
Tags: Coding, Jupyteer, GeoPandas, Pandas, CRS
Category: Python
Slug: GeoPandas-TWD97-CRS
---

PyCon TW 2016 聽了一場有趣的演講 [From Pandas to GeoPandas - 地理資料處理與分析] 講者很清楚地把目前世界與臺灣的地理座標系統做了一些簡介，還展示了一些使用 Jupyter 與 GeoPandas 方法。

恰巧不巧剛好看到朋友在[臉書]上也在處理這類資料，就做了些演講心得與使用記錄。


### 臺灣座標系統

臺灣較常見的座標系統有 WGS84 的經緯度座標、與投影後的二度分代投影座標(TM2): TWD67、TWD97，經緯度座標系和 TM 二度分代投影座標系主要差異是前者是三維空間後者是二維空間。

兩類可從數字的大小立刻辨別一筆資料是屬於前後者（TM2 的值會很大），至於 TM2 的 TWD67 與 TWD97 則可以根據資料量測時間來簡單分辨，因為 1999 年發生集集 921 大地震，地理型態因此產生一些變化，很多地理位置使用 TWD97 有重新測量，這是一個簡單的判斷準則。

更多的資訊可以參考[大地座標系統與二度分帶座標]


### 環境設定與套件安裝

我的電腦是用 OS X + Python3，要建立一個新的資料 kbike 夾與虛擬環境 venv：

```
$ Jason mkdir -p kbike
$ Jason python3 -m venv env
$ Jason source source env/bin/activate
$ (env)Jason
```

建立之後就可以用 pip 開始安裝 GeoPandas 和 Jupyter 兩個套件然後進入 kbike 資料夾下載檔案：

```
$ Jason pip install GeoPandas
$ Jason pip install Jupyter
```

因為這次 sample 是高雄自行車道地理資訊，所以建立完之後就可以下載[高雄自行車路線]解壓縮到 kbike 資料夾內。
這次下載資料有三個，因為都是中文我改了檔案名稱：

```console
kbike0324.dbf
kbike0324.shp
kbike0324.shx
```

這三個檔案會使用到 .shp 裡頭儲存著二維座標系的位置。


### 處理資料

萬事俱備只欠東風，現在就可以將前面我們安裝好的 Jupyter Notebook 打開然後 import GeoPandas。

```
$ Jason jupyter notebook
``` 

打開預設瀏覽器後會看到右上角一個 new 的按鈕，點開然後選擇 python3，這時會跑出一個 console mode，就先 import 套件然後設定產生圖的 size:

```python
import geopandas as gpd
%pylab inline
pylab.rcParams['figure.figsize'] = (20.0, 20.0)
```

接著就是把 .shp 檔案讀進來然後印出來看看檔案的樣子：

```python
villages_shap = gpd.read_file('kbike0324.shp')
villages_shap.head()
```

這份資料主要由 1029 rows × 2 columns 組合而成，因為 GeoPandas 是依附在 Pandas 所以資料只會印出一部分：

|  |geometry|system|
|--|:------:|:----:|
|0|LINESTRING (182419.7414554919 2523932.41148585...|阿公店自行車道|
|1|LINESTRING (183981.184590639 2522441.403167007...|阿公店自行車道|
|2|LINESTRING (183909.7255066092 2522962.24337105...|阿公店自行車道|
|3|LINESTRING (183963.1446304776 2523100.414426, ...|阿公店自行車道|


接著我們要將這份資料的地理座標系印出，因為只是範例就簡單找了兩個腳踏車道 阿公店自行車道和博愛世運大道 來處理囉。

```python
broad = villages_shap[villages_shap['system'] == '阿公店自行車道']
loveroad = villages_shap[villages_shap['system'] == '博愛世運大道']
```

然後就會把圖檔順利產生囉。
範例就在 [gihub] 歡迎下載參考。




[From Pandas to GeoPandas - 地理資料處理與分析]: https://tw.pycon.org/2016/en-us/events/talk/69477625352945724/#speaker-content
[臉書]: https://www.facebook.com/VioletVivirand/posts/10209329811942815
[大地座標系統與二度分帶座標]: http://www.sunriver.com.tw/grid_tm2.htm
[高雄自行車路線]: http://data.kaohsiung.gov.tw/Opendata/DetailList.aspx?CaseNo1=AD&CaseNo2=2&Lang=C&FolderType=O
[gihub]: https://github.com/chairco/Kaohsiung-bike-GeoPandas/blob/master/.ipynb_checkpoints/Untitled-checkpoint.ipynb


