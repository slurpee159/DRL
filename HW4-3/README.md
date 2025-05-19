# HW 4-3 — DQN in **Random‑Mode Gridworld** (Keras)

<sup>Framework migration · training‑stability techniques</sup>

---

## Q & A — Development Notes

**Q1. Why switch from PyTorch to Keras/TensorFlow 2 for this homework?**<br>
A1. Keras offers a concise `Model` / `GradientTape` workflow plus built‑in learning‑rate schedulers and easy mixed‑precision; migrating the baseline shows framework‑agnostic RL skill.

**Q2. What makes *random mode* harder than the previous modes?**<br>
A2. Every episode re‑randomises **Goal / Pit / Wall / Player** positions. The agent must learn a policy that **generalises** across thousands of layouts instead of memorising one map.

**Q3. Which training tips proved most useful?**<br>
A3. *Huber loss* (smooths TD spikes) · *Gradient clipping* (‖g‖≤5) · *Exponential LR decay* (0.5× every 2 000 steps).

---

## Technical Summary

### 1 | Environment

| Component  | Randomised? | Symbol | Reward             |
| ---------- | ----------- | :----: | ------------------ |
| **Goal**   | ✔           |   `+`  | **+10** (terminal) |
| **Pit**    | ✔           |   `-`  | **–10** (terminal) |
| **Wall**   | ✔           |   `W`  | blocks move        |
| **Player** | ✔ (start)   |   `P`  | every step **–1**  |

*Mode*: `Gridworld(size=4, mode="random")`  •  *State*: 4 one‑hot planes → **64‑D** vector

### 2 | Algorithms & Hyper‑parameters

| `--algo`  | Network             | TD target                                   | Tips enabled            |
| --------- | ------------------- | ------------------------------------------- | ----------------------- |
| `double`  | MLP (128)           | **Double TD** (online arg‑max, target eval) | Huber · clip · LR decay |
| `dueling` | **Dueling** (V + A) | Vanilla TD                                  | Huber · clip · LR decay |
| baseline  | MLP (128)           | Vanilla TD                                  | 上述 tips 同樣開啟            |

Common settings (tuned for random mode)

| Item                | Value                        |
| ------------------- | ---------------------------- |
| Episodes            | **3 000**                    |
| Batch / Buffer      | 128 / 50 000                 |
| γ / initial lr      | 0.99 / 1 × 10⁻³              |
| LR schedule         | 0.5× every 2 000 updates     |
| ε‑greedy            | start 1.0 → **0.1**, τ = 800 |
| Target sync         | every **20** episodes        |
| Max steps / episode | 50                           |

### 3 | How to Run

```bash
pip install tensorflow matplotlib
# Double DQN
python hw4_3_keras_dqn.py --algo double  --smooth 100
# Dueling DQN
python hw4_3_keras_dqn.py --algo dueling --smooth 100
```

Each run saves **`random_curves_<algo>.png`** (left = loss, right = reward + MA(100)).

### 4 | Results (example)

*(Insert your generated images below)*

| Algorithm   | Final 100‑ep MA reward | Notes                             |
| ----------- | ---------------------- | --------------------------------- |
| Baseline    | ≈ –30                  | struggles to avoid pits           |
| **Double**  | **≈ –12**              | faster rise, lower variance       |
| **Dueling** | **≈ –15**              | smooth curve, slightly lower mean |

### 5 | Key Takeaways

1. **Double TD** limits Q‑over‑estimation → faster, steadier learning on random layouts.
2. **Dueling head** decouples state value, lowering variance late in training.
3. Huber loss + gradient clipping + LR decay keep the loss bounded and prevent catastrophic spikes.

---

![image](https://github.com/user-attachments/assets/ac87ecdb-3617-40c8-a52e-606475ce9f81)


