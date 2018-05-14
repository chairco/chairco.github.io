---
Title: 增強式學習導論
Date: 2017-05-21 21:54:51
Tags: Reinforcement Learning, Machine Learning
Category: Machine Learning
Slug: Reinforcement Learning introduction
---

這篇主要整理了今天一堂 Reinforcement Learning 課程的整天課程紀錄。所有的實作主要會在 [Google Cloud Platform](https://console.cloud.google.com/compute) 上完成，按照網站上說法是需要信用卡申請才能使用原因是避免機器人自動申請。

課程大綱可以參考[網站](https://sites.google.com/view/caigame/%E9%A6%96%E9%A0%81?authuser=0)，接下來會以我今天有限的腦力紀錄。



### 雲端機器與 Docker 環境設置

今天上半場主要講解如何在 GCP 上啟用一個 instance，並且安裝 docker [^1]，接著 pull 一個已經預先做好的 docker image，接著設定防火牆讓 jupyter notebook 可以透過外網連入 jupyter notebook 操作。要注意是一開始 demo 是不開啟 GPU 版本，因此可以不需要安裝 nvdia 的 driver



### OpenAI Gym

接著開始介紹 OpenAI Gym 這個套件 [^2]。這個套件出現的目的是用來建立一個增強式學習的平台。簡單來說就是讓環境(environment)和機器人(agent)之間相互作用的溝通平台。同時也內建了許多已經事先安裝好的環境，就是透過一些 api 讓你的機器人可以用簡單方式與環境活動進而可以簡單的進行增強式學習。



### 增強式學習(Reinforcement Learning)

接著是增強式學習的介紹。講師以一篇 2015 年的增強式學習投影片來說明 [^3]增強式學習有一個很重要特徵:

+ 機器導向式的學習(Agent-oriented learning)
+ 透過嘗試與錯誤，且只傳遞評估的回饋（獎勵, reward）
	- 某些機器學習就像是自然學習(Natural Learning)
	- 學習可以告訴自己是正確或錯誤
+ 開始這樣的自我思考科學既不是自然科學也不是應用科技


所以我們可以說增強式學習（Reinforcement Learning）結合幾種集合：

+ Machine Learning
+ Reward System
+ Classical/Operant Conditioning
+ Bounded Rationality
+ Operations Research
+ Optimal Control


同時增強式學習的介面會像是：

1. Environment (Reward, Gain, Payoff, Cost)--->  Agent
2. Agent (Action, Response, Control)---> Environment 
3. Environment (state, Stimulus, Situation)---> Agent

1 > 2 > 3 > 1 .... 不斷循環的過程


而在增強式學習過程中，統計學和機率是不可或缺的數學要素，因此馬可夫決策過程（Markov Decision Processesm, MDPs）被視為一個在增強式學習過程中處理部分隨機部份決策者控制下的一個數學模型。（其實講到這裡思考一下人類就是這樣做學習的啊，在部分隨機的外界控制和自己的決策中逐漸累積一種智慧）


舉個馬可夫決策過程的，假設 A, B 路徑兩點路徑會有幾個限制

1. 離散時間 t=1,2,3....
2. 有限的狀態(states)
3. 有限的行動(actions)
4. 有限的獎勵(rewards)
5. 所以會有 s(t), a(t), r(t+1), a(t+1)....等
6. 所以我們可以透過這樣馬可夫的動態推導機率


接著談到報酬要怎麼做，提到了 Q-Learning，定義為 Q 值。所以透過馬可夫的動態決策過程我們不斷去累積報酬的折現（Q 值）簡單講其實就是統計上的一種期望值啦，不斷的重複某種行為到最後當然就會逐漸出現一種好的結果。在做這樣的訓練過程講師認為不是要達到目標與獲得正報酬，而是要避開風險。


### 深度學習(Deep Learning)

接著課題回到了神經網路，增強式學習與類神經網路結合的效果很不錯，因此來談談類神經網路 [^4]。要談類神經網路之前就要先從邏輯迴歸(Logistic Regression
)說起。邏輯迴歸Logistic Regression)簡單來講就是在平面上透過一條線去評定兩端，因此經常用在統計學、經濟學等範疇。但通常在實務上遇到問題是我們並不知道那條線的方程式，但有很多那條線方程式所產生的資料(如果對這個有興趣可以去聽林軒田老師的機器學習基石提到的 Perception Learning Algorithm, PLA)那我們要怎麼找到這個方程式？

簡單來說我們可以寫一個演算法，然後用資料不斷去帶入，假設 a 類帶入方程式希望是正的，b 類帶入方程式希望是負的，所以我們不斷去測試直到找到一個可以測試正確的。然後在測試過程我們要給他反饋就是所謂的 Cost Function 或是稱 Lost Function。簡而言之就是說你找到對的花費小，找到錯的花費大。而最小化 Cost Function 的演算法就是 SGD(Stochastic Gtadient Descent)。然後這樣複雜的事情 Keras 這個 Python 套件讓這件事變得美好。



### Q-Learning

回過頭來談談 Q-Learning 到底在 RL 中要如何優化 policy? 畢竟 RL 報酬很稀疏又延遲實在不知道怎樣做才會得到好的報酬。方法就是都去嘗試，然後求一個期望值類似於統計學的中央極限定理(CLT)。因為我們認為所有的行為在經過多數之後就會趨於一個常態分配（normal distribution）所以很合理的 Q-Learning 的 Q 值其實就是一個期望值。

如何求得這個期望值呢？先了解從 finite Markov decision process (MDP) 上對於 Q-learning 的公式來看：

```
Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
```

這公式裡面需要搭配每個點的路徑，路徑我們可以給訂一個 Reward 值然後計算出 R 矩陣與 Q 矩陣 

+ s(state): 狀態
+ a(action): 行為
+ Q: Q 值，代表每一次學習後的智慧
+ R: R 值，代表當前狀態 R 矩陣的值
+ Max[Q]: 下一個狀態在 Q 矩陣的值 

**[詳細可參考這篇文章](http://mnemstudio.org/path-finding-q-learning-tutorial.htm)**


然後經過每一次路徑結果就可以不斷產生新的平均值。這個大概就是 Q-learning 概念。




[^1]:[環境申請與安裝教學](https://sites.google.com/view/caigame/%E9%A6%96%E9%A0%81/%E5%BB%BA%E7%BD%AE?authuser=0)

[^2]:[OpenAI Gym 介紹](https://docs.google.com/presentation/d/1EP9c8YUZUSFkoH-vcyeogLFTxJybJ3x7DM1Dcr1IZ9o/edit#slide=id.g21cc553694_0_128)

[^3]:[ShuttonIntroRL](http://media.nips.cc/Conferences/2015/tutorialslides/SuttonIntroRL-nips-2015-tutorial.pdf)

[^4]:[類神經網路介紹](https://docs.google.com/presentation/d/1Yw5BfhfQp0mxPvvXyJ2HC4Z80dkTg-pLXasLVdo8wGs/edit#slide=id.g21bd18b122_25_0)

