import numpy as np
import matplotlib.pyplot as plt

# 設定亂數種子，保證實驗可重現
np.random.seed(42)

# 模擬參數設定
n_arms = 10         # 臂數
n_steps = 1000      # 每次實驗的步數
n_runs = 200        # 總共模擬次數
true_reward_means = np.random.rand(n_arms)  # 真實機率

# Epsilon-Greedy 策略
def epsilon_greedy(epsilon):
    rewards = np.zeros(n_steps)
    for _ in range(n_runs):
        Q = np.zeros(n_arms)
        N = np.zeros(n_arms)
        for t in range(n_steps):
            if np.random.rand() < epsilon:
                a = np.random.choice(n_arms)
            else:
                a = np.argmax(Q)
            r = np.random.binomial(1, true_reward_means[a])
            N[a] += 1
            Q[a] += (r - Q[a]) / N[a]
            rewards[t] += r
    return rewards / n_runs

# UCB 策略
def ucb(c):
    rewards = np.zeros(n_steps)
    for _ in range(n_runs):
        Q = np.zeros(n_arms)
        N = np.zeros(n_arms)
        for t in range(n_steps):
            for i in range(n_arms):
                if N[i] == 0:
                    a = i
                    break
            else:
                UCB = Q + c * np.sqrt(np.log(t + 1) / (N + 1e-5))
                a = np.argmax(UCB)
            r = np.random.binomial(1, true_reward_means[a])
            N[a] += 1
            Q[a] += (r - Q[a]) / N[a]
            rewards[t] += r
    return rewards / n_runs

# Softmax 策略
def softmax(tau):
    rewards = np.zeros(n_steps)
    for _ in range(n_runs):
        Q = np.zeros(n_arms)
        N = np.zeros(n_arms)
        for t in range(n_steps):
            exp_Q = np.exp(Q / tau)
            probs = exp_Q / np.sum(exp_Q)
            a = np.random.choice(n_arms, p=probs)
            r = np.random.binomial(1, true_reward_means[a])
            N[a] += 1
            Q[a] += (r - Q[a]) / N[a]
            rewards[t] += r
    return rewards / n_runs

# Thompson Sampling 策略
def thompson_sampling():
    rewards = np.zeros(n_steps)
    for _ in range(n_runs):
        alpha = np.ones(n_arms)
        beta = np.ones(n_arms)
        for t in range(n_steps):
            theta = np.random.beta(alpha, beta)
            a = np.argmax(theta)
            r = np.random.binomial(1, true_reward_means[a])
            if r == 1:
                alpha[a] += 1
            else:
                beta[a] += 1
            rewards[t] += r
    return rewards / n_runs

# 執行各策略
eps_rewards = epsilon_greedy(0.1)
ucb_rewards = ucb(2)
softmax_rewards = softmax(0.1)
ts_rewards = thompson_sampling()

# 繪製圖表
plt.figure(figsize=(12, 6))
plt.plot(np.cumsum(eps_rewards), label="Epsilon-Greedy")
plt.plot(np.cumsum(ucb_rewards), label="UCB")
plt.plot(np.cumsum(softmax_rewards), label="Softmax")
plt.plot(np.cumsum(ts_rewards), label="Thompson Sampling")
plt.xlabel("Steps")
plt.ylabel("Cumulative Reward")
plt.title("Cumulative Reward over Time for MAB Algorithms")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
