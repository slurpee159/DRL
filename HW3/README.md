# HW3: Explore and Exploit for Arm-Bandit Problem

## 作業目標
此作業對一系列多臂強盜算法 (多臂強盜, Multi-Armed Bandit, MAB) 進行實作和深入理解。首先對下列四種算法進行分析與比較：

- Epsilon-Greedy
- UCB (Upper Confidence Bound)
- Softmax
- Thompson Sampling

## 各算法項目內容

### 1. Epsilon-Greedy
- **(1) 算法公式 (LaTeX)**:
  \[
  A_t = \begin{cases}
  \text{random action} & \text{with probability } \varepsilon \\
  \arg\max_a Q_t(a) & \text{with probability } 1 - \varepsilon
  \end{cases}
  \]
- **(2) ChatGPT Prompt**:
  > 「請說明 epsilon-greedy 如何在探索與利用之間獲得平衡」
- **(3) 程式碼與圖表**: Python 實作, 每步類動態平均評估
- **(4) 結果解釋**:
  - 空間: $O(K)$
  - 時間: $O(1)$
  - 分析: 簡單效率高, 但設定固定 epsilon 時有賣算問題

### 2. UCB
- **(1) 算法公式 (LaTeX)**:
  \[
  A_t = \arg\max_a \left( Q_t(a) + c \sqrt{\frac{\ln t}{N_t(a)}} \right)
  \]
- **(2) ChatGPT Prompt**:
  > 「請解釋 UCB 如何利用不確定性來探索佳臂」
- **(3) 程式碼與圖表**: 針對已嘗試和未嘗試臂達到探索平衡
- **(4) 結果解釋**:
  - 空間: $O(K)$
  - 時間: $O(K)$
  - 分析: 對累積資訊量使用效率高, 有理論執行效果

### 3. Softmax
- **(1) 算法公式 (LaTeX)**:
  \[
  P(a) = \frac{e^{Q_t(a)/\tau}}{\sum_{b} e^{Q_t(b)/\tau}}, \quad A_t \sim P(a)
  \]
- **(2) ChatGPT Prompt**:
  > 「請解釋 softmax 中溫度參數 tau 如何影響併用與探索」
- **(3) 程式碼與圖表**: 擴光型利用溫度變控探索資訊額
- **(4) 結果解釋**:
  - 空間: $O(K)$
  - 時間: $O(K)$
  - 分析: 效率良好但效果取決於溫度參數

### 4. Thompson Sampling
- **(1) 算法公式 (LaTeX)**:
  \[
  \theta_a \sim \text{Beta}(\alpha_a, \beta_a), \quad A_t = \arg\max_a \theta_a
  \]
- **(2) ChatGPT Prompt**:
  > 「請解釋 Thompson Sampling 如何利用貝葉斯更新調整探索與利用平衡」
- **(3) 程式碼與圖表**: 計算 beta 分佈下的真實取值
- **(4) 結果解釋**:
  - 空間: $O(K)$
  - 時間: $O(K)$
  - 分析: 很有效的探索方法, 常見於推薦系統

---

## 圖表說明
全部算法結果都已經通過 Python 語言實作，針對 Bernoulli Bandit (01 報酬) 進行復練與平均化處理。圖表簡潔顯示了每個算法所獲得的累積報酬。

---

## 結論
所有項目均已充分滿足作業要求：算法公式、Prompt 用語、Python 實作與圖表、空間和時間分析。

可準備上傳 Jupyter Notebook 或 PDF 作為完整作業。

