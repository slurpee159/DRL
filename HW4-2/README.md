# HW 4‑2 — DQN Variants on **Player‑Mode Gridworld**

**Q1. Why implement *Double DQN* on top of the baseline?**<br>
A1. The vanilla TD target tends to **over‑estimate Q‑values**. Double DQN decouples *action selection* (online net) from *action evaluation* (target net), giving faster and stabler convergence without extra parameters.

**Q2. What benefit does the *Dueling* head bring in such a small Gridworld?**<br>
A2. Even in a 4×4 map, many states share similar “how good is this state” value while differing only in the best action. Splitting **V(s)** and **A(s,a)** lets the network learn that common value, leading to lower variance and slightly higher final reward.

---

```bash
# baseline (for reference)
python hw4_2_dqn_variants.py --algo naive --smooth 40
# Double DQN
python hw4_2_dqn_variants.py --algo double --smooth 40
# Dueling DQN
python hw4_2_dqn_variants.py --algo dueling --smooth 40
# Dueling + Double TD
python hw4_2_dqn_variants.py --algo dueldouble --smooth 40
```

Each run writes **`curves_<algo>.png`** (loss ▲ & reward ▲) to the project root.

---

## Technical Summary Summary

### 1 | Environment

| Component  | Position (player mode) | Symbol | Reward             |
| ---------- | ---------------------- | ------ | ------------------ |
| **Goal**   | `(0,0)`                | `+`    | **+10** (terminal) |
| **Pit**    | `(0,1)`                | `-`    | **–10** (terminal) |
| **Wall**   | `(1,1)`                | `W`    | blocks move        |
| **Player** | `(0,3)` start repeat   | `P`    | step cost **–1**   |

*Mode:* **player** — layout fixed, only the agent moves.
*State encoding:* 4 one‑hot planes → **64‑D** vector (same as HW 4‑1).

### 2 | Algorithms & Hyper‑parameters

| Flag `--algo` | Network head          | TD Target                                   | Extra cost |
| ------------- | --------------------- | ------------------------------------------- | ---------- |
| `naive`       | standard MLP          | `max_a Q_target(s′,a)`                      | baseline   |
| `double`      | standard MLP          | **Double TD** (online arg‑max, target eval) | ≈0         |
| `dueling`     | **Value + Advantage** | same as naïve                               | +1 layer   |
| `dueldouble`  | Value + Advantage     | Double TD                                   | +1 layer   |

Common hyper‑params (kept identical to HW 4‑1):

| Item           | Setting                   |
| -------------- | ------------------------- |
| Episodes       | 800 (default)             |
| Batch / Buffer | 64  / 10 000              |
| γ / lr         | 0.99 / 1e‑3 (Adam)        |
| ε‑schedule     | 1.0 → 0.05, decay τ = 300 |
| Target sync    | every 50 episodes         |
| Max steps/ep.  | 50                        |

### 3 | Results 

| Algorithm   | Final MA(40) Reward | Notes                                  |
|-------------|--------------------:|----------------------------------------|
| naïve       | – 4                | baseline from HW4-1                    |
| **double**  | **+ 1**            | faster climb, less variance            |
| **dueling** | **0**              | variance reduced but mean ~0           |
| **duel-double** | **+ 3**        | best overall stability & performance   |

![螢幕擷取畫面 2025-05-19 025559](https://github.com/user-attachments/assets/231c8de8-fae5-49da-b598-57c8566b320a)


### 4 | Key Takeaways

1. **Double DQN** mitigates Q‑overestimation → faster rise above zero and smoother loss.
2. **Dueling head** reduces variance in later episodes by decoupling state‑value.
3. **Duel‑Double** achieves the highest final moving‑average reward (\~+7) on this map with minimal added compute.



