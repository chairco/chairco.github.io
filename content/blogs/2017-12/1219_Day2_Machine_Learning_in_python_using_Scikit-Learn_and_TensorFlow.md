---
Title: Day2 一天一篇機器學習 in python using Scikit-Learn and TensorFlow 系列 
Slug: day2_machine_learning_in_python_using_scikit-learn_and_tensorflow
Date: 2017-12-19 09:25:26
Modified: 2017-12-19 09:25:26
Tags: Python, Classification, Scikit-learn
Category: Machine Learning
---

前一天我們提到二元分類器、並且透過交叉驗證 (cross-validation) 得到準確度並使用 precision/recall tradeoff 調整配適，最後透過 ROC curves, ROC AUC 分數來評估模型。

但如果前面的例子，我們想拓展成能夠分類 0~9 的任一數字呢？接下來就來討論有哪些作法：

+ `Randon Forest classifier`(隨機森林)或是 `navie Bayes` classifiers 可以直接處理多元分類
+ `Support Vector Machine` classifiers 或是 `Linear` classifiers 就是嚴格的二元分類，策略是將他做多個二元分類，看起來就像是多元分類。舉個例，你可以去訓練 0~9 每一個數字 `是與否`，你就可以訓練出 10 個分類器(0-detector, 1-detector, 2-detector, 3-detector 等等)，然後再做判斷時你只要取得十種二元分類器判斷的最高分。這個又被稱為 one-versus-all(OvA)。林軒田老師的機器學習課程稱： One-Vs-All 策略。另外在這種嚴格二元分類底下還有一種策略是兩兩成對(every pair of digits)，就是將所有數字進行排列組合：(0,1), (0,2), (0,3) ... 所以你需要訓練出 `n*(n-1)/2` 種分類，這種策略被稱為 one-versus-one(OvO) 以本例 MNIST 你就會需要訓練出 45 種二元分類。好像有點太多了。但他的優點就是訓練時你只要挑兩類(以本例為數字)來做訓練。

兩種演算法個適合在不同的使用情境，例如 Support Vector Machine 會隨著訓練的規模縮小而效能較好，因此如果你的訓練資料是比較小的，那會比較建議用 OvO，但多數時候的二元分類演算法會偏好使用 OvA。

使用 sickit-learn 做多元分類時預設是使用 OvA 策略。除了 SVM 分類器會使用 OVO 策略，接著我們就來試試 SGDClassifier:

```python
>>> sgd_clf.fit(X_train, y_train) # y_train, not y_train_5
>>> sgd_clf.predict([some_digit])
array([ 5.])
```


上面我們的訓練資料就不能放 y_train_5 而要放 y_train，非常簡單，sickit-learn 就會根據我們給的訓練資料開始訓練 10 個二元分類器。然後根據不同的圖片計算 decision score。可以呼叫 decision_function() 這是會回傳 10 組實例的分數。


```python
>>> some_digit_scores = sgd_clf.decision_function([some_digit]) 
>>> some_digit_scores
array([[-311402.62954431, -363517.28355739, -446449.5306454 ,
        -183226.61023518, -414337.15339485,  161855.74572176,
        -452576.39616343, -471957.14962573, -518542.33997148,
        -536774.63961222]])
```

接著我們可以看看最高分數位於哪個位置。

```python
>>> np.argmax(some_digit_scores)
5
>>> sgd_clf.classes_
array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.])
>>> sgd_clf.classes_[5]
5.0
```

可以很清楚看見答案是 5，在這個例子當中只是剛好 5 位於陣列 5 的位置。

用 OvO 的策略來訓練，可以選 OneVsOneClassifier or OneVsRestClassifier classes 然後根據 SGDClassifier：

```python
>>> from sklearn.multiclass import OneVsOneClassifier
>>> ovo_clf = OneVsOneClassifier(SGDClassifier(random_state=42))
>>> ovo_clf.fit(X_train, y_train)
>>> ovo_clf.predict([some_digit])
array([ 5.])
>>> len(ovo_clf.estimators_)
45
```

用 RandomForestClassifier 演算法，注意是用 RandomForest 就不需要選用 OvO 或是 OvA，因為 RandomForest 可以直接處理多元分類。

```python
>>> forest_clf.fit(X_train, y_train)
>>> forest_clf.predict([some_digit])
array([ 5.])
>>> forest_clf.predict_proba([some_digit])
array([[ 0.1,  0. ,  0. ,  0.1,  0. ,  0.8,  0. ,  0. ,  0. ,  0. ]])
```

用 Predict_proba 印出每個訓練資料是 5 的概率。index 5 有 80% 機率為 5，也可發現在 0 或是 3 某些機率下也會被判斷成 5，接著用交叉驗證(cross-validation) 確認 SGDClassifier 的 accurancy:

```python
>>> cross_val_score(sgd_clf, X_train, y_train, cv=3, scoring="accuracy")
array([ 0.87767447,  0.84059203,  0.85477822])
```


拆解成 k-folds 測試得到 84% 準確度，如果使用隨機分類會得到 10% 準確度，看起來不錯。但我們可以讓他更好一些：

```python
>>> from sklearn.preprocessing import StandardScaler
>>> scaler = StandardScaler()
>>> X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))
>>> cross_val_score(sgd_clf, X_train_scaled, y_train, cv=3, scoring="accuracy")
array([ 0.91376725,  0.90954548,  0.90718608])
```

分析錯誤一樣用到混淆矩陣 (Confuion Matrix) 
```python
>>> y_train_pred = cross_val_predict(sgd_clf, X_train_scaled, y_train, cv=3)
>>> conf_mx = confusion_matrix(y_train, y_train_pred)
>> conf_mx
array([[5729,    2,   22,    8,   10,   50,   48,    9,   41,    4],
       [   2, 6487,   44,   25,    6,   42,    5,    9,  110,   12],
       [  50,   40, 5347,   95,   85,   28,   87,   53,  159,   14],
       [  48,   38,  135, 5331,    1,  253,   32,   54,  144,   95],
       [  17,   25,   41,   10, 5350,   10,   55,   30,   87,  217],
       [  69,   38,   35,  189,   75, 4614,   97,   25,  183,   96],
       [  33,   24,   50,    2,   39,  102, 5609,    5,   53,    1],
       [  24,   19,   77,   26,   60,   12,    4, 5798,   18,  227],
       [  42,  148,   70,  146,   11,  161,   57,   18, 5062,  136],
       [  40,   34,   28,   85,  161,   32,    2,  203,   81, 5283]])
```

但都是數字不是很明顯，將它轉成以顏色為主的方格來看，

```python
>>> plt.matshow(conf_mx, cmap=plt.cm.gray)
>>> save_fig("confusion_matrix_plot", tight_layout=False)
>>> plt.show()
```

![#](https://i.imgur.com/jUksCQT.png)

主對角線上的值代表圖片正確的預測，所以呈現一個對角線，唔，看起來非常的不錯！

但我們也關注錯誤的分類。首先我們將混淆矩陣內錯誤數量除以圖片的的數量得到一個比例，這樣可以協助我們繪製圖表：

```python
>>> row_sums = conf_mx.sum(axis=1, keepdims=True)
>>> norm_conf_mx = conf_mx / row_sums

>>> np.fill_diagonal(norm_conf_mx, 0)
>>> plt.matshow(norm_conf_mx, cmap=plt.cm.gray)
>>> save_fig("confusion_matrix_errors_plot", tight_layout=False)
>>> plt.show()
```

![#](https://i.imgur.com/th0ZFtg.png)

這張圖 row（行）是指實際的值，column（列）是指預測得值。從圖上的顏色可以發現 column 上的 8, 9 兩個數字底色接近白色的數量遠多於其他數字，代表很多數字被錯誤分類到 8, 9 相反的像是數字 1 的底色多數為黑，這代表多數情況下 1 都可以被正確分類（雖然部分與 8 混淆）。注意是錯誤不一定都是對稱的。

分析混淆矩陣有助於你了解與改善分類器，以這個例子為例，你就可以花費較多的心力來改善對於數字 8, 9 的改善。或是撰寫演算法來計算 closed loop 的數量，或是使用 scikit-image, Pillow, OpenCV 來改善。

雖然分析這些個別的錯誤可以有助了解分類器錯誤原因，但卻是耗時的。我們嘗試畫 3, 5 兩個數字來看看：

```python
def plot_digits(instances, images_per_row=10, **options):
    size = 28
    images_per_row = min(len(instances), images_per_row)
    images = [instance.reshape(size,size) for instance in instances]
    n_rows = (len(instances) - 1) // images_per_row + 1
    row_images = []
    n_empty = n_rows * images_per_row - len(instances)
    images.append(np.zeros((size, size * n_empty)))
    for row in range(n_rows):
        rimages = images[row * images_per_row : (row + 1) * images_per_row]
        row_images.append(np.concatenate(rimages, axis=1))
    image = np.concatenate(row_images, axis=0)
    plt.imshow(image, cmap = matplotlib.cm.binary, **options)
    plt.axis("off")
```

```python
cl_a, cl_b = 3, 5
X_aa = X_train[(y_train == cl_a) & (y_train_pred == cl_a)]
X_ab = X_train[(y_train == cl_a) & (y_train_pred == cl_b)]
X_ba = X_train[(y_train == cl_b) & (y_train_pred == cl_a)]
X_bb = X_train[(y_train == cl_b) & (y_train_pred == cl_b)]

plt.figure(figsize=(8,8))
plt.subplot(221); plot_digits(X_aa[:25], images_per_row=5)
plt.subplot(222); plot_digits(X_ab[:25], images_per_row=5)
plt.subplot(223); plot_digits(X_ba[:25], images_per_row=5)
plt.subplot(224); plot_digits(X_bb[:25], images_per_row=5)
save_fig("error_analysis_digits_plot")
plt.show()
```

![#](https://i.imgur.com/cpUtaJ8.png)

其實用肉眼可以看出像是第八行的 5 看起來就很像 3。我們也可以解釋為什麼 SGDClassifier 再進行一些分類時會出現錯誤，分類器只是一個簡單的線性模型，對於分辨方式是給予每個像素一個權重，因此當分類器看到一個新圖像就會根據權重給予像素強度並且計算分數總和。3s 與 5s 只有幾個像素不同，因此很容易就造成混淆。


最後是分類的另一種方式：`Multilabel classification` 某些時候對於一種 instance 我們希望輸出多種類別，例如照片的分辨：Alice, Mary, Tome 三人在一張照片裡面我們可能會希望輸出這樣結果 [1, 0, 1], Alice:Yes, Mary:No, Tom:Yes。這種輸出多個 label 的二元分類就是稱為 `multilabel classification system` 

