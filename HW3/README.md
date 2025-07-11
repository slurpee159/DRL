# HW3: Explore and Exploit for Arm-Bandit Problem

---

### 1. Epsilon-Greedy

#### Prompt:

How does the epsilon-greedy strategy balance exploration and exploitation in the multi-armed bandit problem?

#### Additional Question:

How does epsilon-greedy compare to other methods like UCB or Thompson Sampling in terms of convergence speed and simplicity?
How does the epsilon-greedy strategy balance exploration and exploitation in the multi-armed bandit problem?

#### Question:

What happens if epsilon is set too high or too low in the epsilon-greedy algorithm?

#### Formula (LaTeX):

$$
A_t = \begin{cases}
\text{random action} & \text{with probability } \varepsilon \\
\arg\max_a Q_t(a) & \text{with probability } 1 - \varepsilon
\end{cases}
$$

#### Python Code: Included in full MAB implementation

#### Result Explanation:

* 空間複雜度：\$O(K)\$（每個臂一個計數器與平均值）
* 時間複雜度：\$O(1)\$ 每一步
* 結果分析：

  * 高 epsilon：過度探索，難以收斂至最佳臂。
  * 低 epsilon：過度利用，可能卡在局部最優。
  * 合理 epsilon（如 0.1）可在長期找到高報酬策略。

---

### 2. Upper Confidence Bound (UCB)

#### Prompt:

How does UCB use uncertainty estimates to guide exploration in bandit algorithms?

#### Additional Question:

What happens to UCB performance if the confidence level parameter $c$ is set too high or too low?
How does UCB use uncertainty estimates to guide exploration in bandit algorithms?

#### Question:

Why does UCB tend to explore under-sampled arms early on?

#### Formula (LaTeX):

$$
A_t = \arg\max_a \left( Q_t(a) + c \sqrt{\frac{\ln t}{N_t(a)}} \right)
$$

#### Python Code: Included in full MAB implementation

#### Result Explanation:

* 空間複雜度：\$O(K)\$（平均值與計數）
* 時間複雜度：\$O(K)\$ 每一步需遍歷所有臂
* 結果分析：

  * 理論上證明擁有次線性後悔值。
  * 初期能快速探索未嘗試臂。
  * 參數 \$c\$ 調整探索強度。

---

### 3. Softmax

#### Prompt:

How does temperature $\tau$ affect the exploration-exploitation trade-off in the softmax action selection algorithm?

#### Additional Question:

How does softmax differ from epsilon-greedy in terms of probability-based decision-making?
How does temperature $\tau$ affect the exploration-exploitation trade-off in the softmax action selection algorithm?

#### Question:

What are the consequences of setting $\tau$ too high or too low in softmax?

#### Formula (LaTeX):

$$
P(a) = \frac{e^{Q_t(a)/\tau}}{\sum_{b} e^{Q_t(b)/\tau}}, \quad A_t \sim P(a)
$$

#### Python Code: Included in full MAB implementation

#### Result Explanation:

* 空間複雜度：\$O(K)\$
* 時間複雜度：\$O(K)\$ 每一步計算 softmax 機率
* 結果分析：

  * $\tau \rightarrow 0$：接近 greedy
  * $\tau \rightarrow \infty$：幾乎均勻隨機選臂
  * 需精心選取 $\tau$，使策略穩定且探索充分

---

### 4. Thompson Sampling

#### Prompt:

How does Thompson Sampling leverage Bayesian inference to balance exploration and exploitation?

#### Additional Question:

Why is Thompson Sampling often more sample-efficient compared to frequentist approaches?
How does Thompson Sampling leverage Bayesian inference to balance exploration and exploitation?

#### Question:

What are the advantages of using Thompson Sampling in a non-stationary bandit setting?

#### Formula (LaTeX):

$$
\theta_a \sim \text{Beta}(\alpha_a, \beta_a), \quad A_t = \arg\max_a \theta_a
$$

#### Python Code: Included in full MAB implementation

#### Result Explanation:

* 空間複雜度：\$O(K)\$（每個臂的 alpha/beta）
* 時間複雜度：\$O(K)\$ 每步須取樣所有臂
* 結果分析：

  * 本質上具備探索與利用的平衡。
  * 在早期有良好的探索機會，並可快速收斂於最佳策略。
  * 不需參數設定，實務上表現穩定。

---

## Python 實作與圖表

已使用 Python 完整實作上述四種策略，並透過 `matplotlib` 繪製其在 1000 步模擬下的累積報酬：

* Epsilon-Greedy (`ε = 0.1`)
* UCB (`c = 2`)
* Softmax (`τ = 0.1`)
* Thompson Sampling（無需參數）

每個策略的學習曲線顯示其探索與利用的效率。

---

## 主程式流程與繪圖說明

本次模擬設定如下：

* 臂數 (`n_arms`)：10
* 總步數 (`n_steps`)：1000
* 隨機種子：42（使用 `np.random.seed(42)` 確保可重現性）

主程式會依序執行四種策略並繪圖：

```python
plot_results([cr_eps], [f"Epsilon-Greedy (ε={eps})"], "Epsilon-Greedy Performance")
plot_results([cr_ucb], [f"UCB (c={c})"], "UCB Performance")
plot_results([cr_soft], [f"Softmax (τ={tau})"], "Softmax Performance")
plot_results([cr_ts], ["Thompson Sampling"], "Thompson Sampling Performance")

plot_results(
    [cr_eps, cr_ucb, cr_soft, cr_ts],
    ["Epsilon-Greedy", "UCB", "Softmax", "Thompson Sampling"],
    "Algorithm Comparison"
)
```

---

## 總結

| 策略                | 空間複雜度    | 時間複雜度    | 優勢           | 限制        |
| ----------------- | -------- | -------- | ------------ | --------- |
| Epsilon-Greedy    | \$O(K)\$ | \$O(1)\$ | 簡單易實作        | 無動態調整探索比率 |
| UCB               | \$O(K)\$ | \$O(K)\$ | 有理論保證        | 初期偏貪婪時可能慢 |
| Softmax           | \$O(K)\$ | \$O(K)\$ | 平滑機率式選擇      | 溫度參數調整需謹慎 |
| Thompson Sampling | \$O(K)\$ | \$O(K)\$ | 貝葉斯方法，自動探索平衡 | 對初學者較難理解  |

---

## 實驗圖表示意

下圖顯示四種策略在 1000 步內的學習效率與報酬表現：

![image](https://github.com/user-attachments/assets/45a8f952-c276-4f66-ba61-3df3676a8b0d)

![image](https://github.com/user-attachments/assets/06c4658f-aa04-4b6a-8d49-44e34e5cce21)

![image](https://github.com/user-attachments/assets/714c63aa-9829-4d82-9b5b-f46b49fdba1f)

![image](https://github.com/user-attachments/assets/89d199cf-8124-4210-be02-f91462443f78)

![image](https://github.com/user-attachments/assets/c72be726-c56a-4209-be61-df68d41643f2)




