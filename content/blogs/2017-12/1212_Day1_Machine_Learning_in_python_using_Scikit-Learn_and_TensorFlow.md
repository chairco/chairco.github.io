---
Title: Day1 一天一篇機器學習 in python using Scikit-Learn and TensorFlow 系列
Slug: day1_machine_learning_in_python_using_scikit-learn_and_tensorflow
Date: 2017-12-17 16:13:56
Modified: 2017-12-17 16:13:56
Tags: Python, Classification, Scikit-learn
Category: Machine Learning
---

今天介紹的是 Machine Learning 一個很基礎的方法：分類(Classification)，然後採用 MNIST 的 dataset 來做。MNIST 是一個擁有 70,000 個小圖片的資料，每張圖都會有標記它代表的數字。MNIST 很像初學程式語言時的 `HELLO WORLD` 所以就拿它來做學習。

scikit-learn 提供一個函式可以輕鬆取得這個資料集，同時可以注意到 scikit-learn 回傳是一個 dictionary 的資料結構，`DESCR` 是這個資料集說明，`data` 是資料集資料，array 結構，一個 row 包含實例，一個 row 包含特徵, `target` 是標籤(label)

```python
>>> from sklearn.datasets import fetch_mldata
>>> mnist = fetch_mldata('MNIST original')
>>> mnist
{'COL_NAMES': ['label', 'data'],
 'DESCR': 'mldata.org dataset: mnist-original',
 'data': array([[0, 0, 0, ..., 0, 0, 0],
        [0, 0, 0, ..., 0, 0, 0],
        [0, 0, 0, ..., 0, 0, 0],
        ..., 
        [0, 0, 0, ..., 0, 0, 0],
        [0, 0, 0, ..., 0, 0, 0],
        [0, 0, 0, ..., 0, 0, 0]], dtype=uint8),
 'target': array([ 0.,  0.,  0., ...,  9.,  9.,  9.])}
```


接著可以看看資料內容

```python
>>> X, y = mnist['data'], mnist['target']
>>> X.shape
(70000, 784)
>>> y.shape
(70000,)
```

一共有 70,000 個 images 和 784 個特徵，784 是因為每個 images 的 pixels 為 28x28，然後每個特徵值代表是像素的強度：從 0(white)~255(block) 我們可以將其顯示出來：

```python
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

some_digit = X[36000]
some_digit_image = some_digit.reshape(28, 28)
plt.imshow(some_digit_image, cmap=matplotlib.cm.binary,
           interpolation="nearest")
plt.axis("off")
plt.show()
```

![#](https://i.imgur.com/lf0kZGV.png)

接著印出 label 上的值

```python
>>> y[36000]
5.0
```

然後 MNIST 的資料集也協助我們將資料切割成兩部分分別為前 60,000 筆資料讓我們可以方便地去做訓練，後面 10,000 資料做測試。
同時對於訓練資料我們也需要做 shuffle 訓練資料，這樣可以讓我們在做交叉驗證時(cross-validation)會有一致性。ps.提示一點，很多演算法對於訓練資料的順序很敏感，像是得到一連串相同的資料。

所以用 numpy 來打亂資料

```python
>> import numpy as np
>> shuffle_index = np.random.permutation(60000)
>> X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]
```

接著我們來訓練一個二元分類(Binary Classifier)，例如選定一個數字 5，二元分類就會只有 5 或是 非 5 兩種，接著我們來建立一個目標向量的分類任務:

```python
y_train_5 = (y_train == 5)
y_test_5 = (y_test == 5)
```

接著我們就可以開始選擇一個分類器並且訓練他。這邊選用是一個統計學的演算法叫 Stochastic gradient descent (梯度下降法)，會用到 Scikit-learn 的 SGDClassifier 類別。我們會設置一個 random_state 參數，因為這個方法重視資料的隨機性。

```python
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42, max_iter=1000)
sgd_clf.fit(X_train, y_train_5)
```
然後注意一點，因為 0.19 版本的類別增加了一個參數叫 `max_iter` 如果沒有設置會出現警告，可以不需要理會，但不想出現警告可以隨意設置一個值例如 1000。[參考](https://github.com/ageron/handson-ml/issues/90)

可以用下面函式來偵測數字 5

```
>>> sgd_clf.predict([some_digit])
array([ True], dtype=bool)
```

接著我們要開始驗證，要驗爭資料準確性 (accuracy) 通常會採用交叉驗證 (Cross-Validation)，這邊我們會使用 cross_val_score()，使用的方法是 K-fold, 意思就是拆解成 k 個子樣本來做交叉測試：

```python
from sklearn.model_selection import cross_val_score
cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring='accuracy')
array([ 0.96905,  0.9682 ,  0.9707 ])
```

顯示高達 96% 的準確度 (accuracy)。
接著可以來試試 非 5 的分類，首先撰寫一個 class：

```python
from sklearn.base import BaseEstimator

class Never5Classifier(BaseEstimator): 
    def fit(self, X, y=None):
        pass
    def predict(self, X):
        return np.zeros((len(X), 1), dtype=bool)
        
        
>> never_5_clf = Never5Classifier()
>> cross_val_score(never_5_clf, X_train, y_train_5, cv=3, scoring="accuracy")
array([ 0.91345,  0.9095 ,  0.906  ])
```

準確度到 90% 左右了，但這是合理的，因為大約只有 10% 數字是 5，因此在猜測中大概有 90% 機會是正確的。這也告訴我們一件事，準確性通常不會是分類器重視的指標，尤其對於傾斜資料 (skewed dataset)。


另外一個測試分類氣的方式是混淆矩陣 (Confuion Matrix) ，概念有點像是統計裡的 type I, type II 錯誤。

+ TT: 預測是, 實際是
+ TF: 預測是, 實際不是
+ FT: 預測不是, 實際是
+ FF: 預測不是, 實際也不是

|       |  預測沒下 | 預測下 |
| :---:  | :----: | :----: |
| 實際下  |  TF(type I)  | TT |
| 實際沒下|  FF  |  FT(type II) |


因此在開始之前你需要建構一個預測集，用來進行比較。在 scikit-learn 可以使用 `cross_val_predict()` 這個函式。和前面我們使用 `cross_val_score()` 一樣也會使用交叉驗證，但不同是他不會返回一個分數，而是返回 k-fold 的一組實例。意思是他會返回 [true, false, false...] 這樣的結果。接著就能開是做 Confusion Matrix。


在 scikit-learn 提供 `confusion_matrix` 函式，接著參數指定一組`訓練資料`與`預測資料`。

```python
>>> from sklearn.metrics import confusion_matrix
>>> confusion_matrix(y_train_5, y_train_pred)
array([[53954,   625],
       [ 1216,  4205]])
```

這個二維陣列表示`實際`與`預測`我們簡單用表格表示。

+ 第一行表示實際非 5, 53,954 代表正確預測也非 5 (true negatives)，625 則表示分類錯誤, 錯誤預測 (false positive) 
+ 第二行表示實際是 5, 1,216 分類錯誤，預測錯誤(false negative)，4,205 預測和實際 5 正確(true positive)

|       |  預測非5 | 預測是5 |
| :---: | :----: | :----: |
| 實際非5 | *53,954*(TN) | 625(FP) |
| 實際是5 | 1,216(FN) | *4,205*(TP) |


當然我們也可以做個簡單驗證，假設我們有個完美預測(perfect train data)，那照理說就不會有預測錯誤的問題。簡單方法就是把訓練資料當成預測資料。這時你會發現預測錯誤的部分都是 0，賓果！

```python
>>> y_train_perfect_predictions = y_train_5
>>> confusion_matrix(y_train_5, y_train_perfect_predictions)
array([[54579,     0],
       [    0,  5421]])
```

混淆矩陣提供我們一個判斷，透過矩陣讓我們可以計算出所謂精確度(precision):
`true positive(tp)/true positive(TP) + false positive(FP)`


但是精確度可能會零一種狀況是萬一發生 1/1 = 100% 會無法有效地去避免只有一個正確的數字情況，因此通常會和 recall 來做使用，稱為 sensitivity or true positive rate(TPR) 稱為靈敏度或是真正率:
`recall = true positive(tp)/true positive(tp)+false negative(fn)`

在 sickit-learning 有兩個函式可以協助 precision_score, recall_score

```python
>>> from sklearn.metrics import precision_score, recall_score
>>> precision_score(y_train_5, y_train_pred)
0.87060041407867494 # 4205/4205+625
>>> recall_score(y_train_5, y_train_pred)
0.77568714259361737 # 4205/4205+1216
```
這代表意思是你有 87% 可以準確的判斷出預測為 5 實際也是 5，只能檢測到實際是 5 的機率 77%。看起來和之前使用交叉驗證得到的分數有些差距。

從 precsion 和 recall 我們還可以推導出一個 [Piotroski F-Score](https://baike.baidu.com/item/f-measure)，他是 precsion 和 recall 的加權調和平均數。可以用來判斷模型好壞，所以我們用它來判斷分類器。

f1 公式與推導:

```
2 * PR / P + R = TP / TP + (FN + FP / 2)

P = TP/TP+FP
R = TP/TP+FP
```

一樣在 sickit-learning 用 f1_score 這個函式來計算：

```python
>>> from sklearn.metrics import f1_score
>>> f1_score(y_train_5, y_train_pred)
0.82040776509608826
```

雖然 F1-score 給了我們一個方法判斷分類器，但有時候這個並不是我們需要的。因為不同時候你關切的可能是 prescision 或是 recall 其中一個。

舉個例如果你關希望分類器幫你辨別好的影片(這邊假設是適合兒童看，沒有任何暴力或是性的影像)，那你可以能會比較關切精確度 (prescision)，因為你在乎的是排除不好的影片，而不會關切是否有好的影片被排除。(寧可放過不可錯殺)
另一個例子是如果你希望寧可錯殺也不願放過，像是偵測扒手資料，那可能 recall 會讓你比較關切。因為不是扒手被抓到的機率對你而言不重要，你並不想放過任何一人。(寧可錯殺不可放過)

這裡從統計觀點來看 prescision 就是所謂 type I error, recall 就是 type II error。如果站在法律觀點，通常我們可以忍受 type I error。


SGDClassifier 的分類方式是建立一個 threshold 的 `decision function` 藉此分出 positive class 或是 negative class。

圖示：
|   8, 7, 3, 9 | 5, 2,    |        5 | 5           |      6 | 5, 5, 5     -|     
| - negative prediction - | - decision threshold - | - positive prediction -|  

+ Decision threshold 中間那條線來區分看右邊 (right side of threadhold) 5 所佔的比例
  + precision = 4/5(80%)
  + recall = 4/6(67%)

+ 如果移動 threshold 到右邊第 6 與 5 那條線，那 5 所佔的比例就會變成
  + precision = 3/3(100%)
  + recall = 3/6(50%)
  
從這邊可以看到 threshold 的提高與降低會讓 precision 與 recall 彼此間消長。
  
在 sickit-learning 無法直接設定 threshold，但可以透過取得 decision score 的 threshold 來進行預測，要取得 score 是呼叫 decision_function() 這個函式：

```python
y_scores = sgd_clf.decision_function([some_digit])
y_scores
array([ 416.56310942])
```

接著就可以設定想要的 threshold 來做判定

```python
threshold = 0
y_some_digit_pred = (y_scores > threshold)
y_some_digit_pred
array([ True], dtype=bool)
threshold = 200000
y_some_digit_pred = (y_scores > threshold)
y_some_digit_pred
array([False], dtype=bool)
```

但衍伸出問題是多少的 threshold 設定值才是正確，可以使用 precision_recall_curve() 這個函式畫出 precision 和 recall tradeoff 交互曲線來參考：

```python
y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3,
                                 method="decision_function")
from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_train_5, y_scores)
```

秀出圖片，並且存到 `/images/classification/` 下。這樣你就可以根據圖顯示的狀況，來選擇 precision/recall tradeoff。

```python
# To plot pretty figures
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "classification"


def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.xlabel("Threshold", fontsize=16)
    plt.legend(loc="upper left", fontsize=16)
    plt.ylim([0, 1])

plt.figure(figsize=(8, 4))
plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.xlim([-700000, 700000])
save_fig("precision_recall_vs_threshold_plot")
plt.show()
```

![#](https://i.imgur.com/sxo08aS.png)


另外一種方式，是將 precisions 和 recall 繪製成 x,y 座標圖關係。

```python
def plot_precision_vs_recall(precisions, recalls):
    plt.plot(recalls, precisions, "b-", linewidth=2)
    plt.xlabel("Recall", fontsize=16)
    plt.ylabel("Precision", fontsize=16)
    plt.axis([0, 1, 0, 1])

plt.figure(figsize=(8, 6))
plot_precision_vs_recall(precisions, recalls)
save_fig("precision_vs_recall_plot")
plt.show()
```

![#](https://i.imgur.com/xneUv8L.png)


關於 precision 與 recall 關係可以舉個例子，如果我們要 90% precision 先比照前前張交互圖，大概需要 70,000 筆資料，接著我們就可以計算出 recall 分數。所以可以很容易的設定出我們想要的精準度(precision)，但這樣其實未必有用，因為伴隨著越高 precision，也帶來 recall 值下降。

```python
>>> y_train_pred_90 = (y_scores > 70000)
>>> precision_score(y_train_5, y_train_pred_90)
0.8842242503259452
>>> recall_score(y_train_5, y_train_pred_90)
0.62553034495480542
```


關於二元分類還有一個不錯的工具：ROC Curve (receiver operating characteristic)，和 precision/recall curve 很類似。繪製出 true positive rate(又稱為 recall) 與 false positive rate 之間的關係。FPR 為不正確分類的比率（預測是但實際不是）。scikit-learn 提供 roc_curve() 函式來實作並且繪圖：


```python
from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_train_5, y_scores)

def plot_roc_curve(fpr, tpr, label=None): 
    plt.plot(fpr, tpr, linewidth=2, label=label) 
    plt.plot([0, 1], [0, 1], 'k--') 
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

plot_roc_curve(fpr, tpr)
save_fig("roc_curve_plot")
plt.show()
```

![#](https://i.imgur.com/953KgNg.png)


同樣可以看到 TPR(recall) 越高，FPR 的分類錯誤也就越多。如果我們想比較分類模型可以比較曲線下面幾 (AUC) 來做模型優劣化指標，越接近 1 越是完美分類。但如果 = 0.5 那模型幾乎沒有價值，< 0.5 比隨機預測還差。同樣 scikit-learn 提供的函式:


```python
>>> from sklearn.metrics import roc_auc_score
>>> roc_auc_score(y_train_5, y_scores)
0.9611350465691233
```

看起來 0.96 很不錯！

然後我們也試著用隨機森林的分類演算法來訓練並且比較，比較特別是隨機森林分類沒有 decision_function() 而有 predict_proba() 回傳一個類別的概率。

```python
>>> from sklearn.ensemble import RandomForestClassifier
>>> forest_clf = RandomForestClassifier(random_state=42)
>>> y_probas_forest = cross_val_predict(forest_clf, X_train, y_train_5, cv=3,
method="predict_proba")
```

```python
>>> y_scores_forest = y_probas_forest[:, 1] # score = proba of positive class 
>>> fpr_forest, tpr_forest, thresholds_forest = roc_curve(y_train_5,y_scores_forest)
>>> plt.plot(fpr, tpr, "b:", label="SGD")
>>> plot_roc_curve(fpr_forest, tpr_forest, "Random Forest")
>>> plt.legend(loc="lower right")
>>> save_fig("roc_curve_comparison_plot")
>>> plt.show()
```

![#](https://i.imgur.com/JJMIxCz.png)

從圖上可以比較用隨機森林繪製出的圖和 ROC curves 很像，接著我們來算算隨機森林的 AUC：

```python
>>> roc_auc_score(y_train_5, y_scores_forest)
0.99224143341969517
```

現在我們知道在挑選二元分類器時，如何使用交差驗證(cross-validation) 評估, 並用 precision/recall tradeoff 來調整你想要的合適度。接者使用 ROC curves, ROC AUC 分數來決定模型是否合適。


