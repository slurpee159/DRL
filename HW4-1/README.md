# HW 4‑1 — Naive DQN on **Static Gridworld**

**Q1:** I executed `!python hw4_1_naive_dqn.py` in Colab and immediately saw `error: unrecognized arguments: -f …kernel‑xxxx.json`.
**A1:** That flag comes from Jupyter itself. I switched to *tolerant* parsing:

```python
args, _ = parser.parse_known_args()  # ignores unknown notebook flags
```

Pull the updated script and the error disappears.

**Q2:** The next run crashed with `AttributeError: 'Gridworld' object has no attribute 'observation'`.
**A2:** The original Gridworld isn’t Gym‑style, so I wrapped it:

```python
class GridEnvWrapper:
    def reset(self):
        self.raw.initGridStatic()
        return self._flatten_board()
    def step(self, a_idx):
        self.raw.makeMove({0:'u',1:'d',2:'l',3:'r'}[a_idx])
        r = self.raw.reward()
        done = r in {10,-10}
        return self._flatten_board(), r, done
```

This adds `reset()`, `step()`, `render()` and a 64‑dim one‑hot observation, solving the attribute error.

**Q3:** Training starts but early returns plunge to –50. Is that normal?
**A3:** Yes. With ε≈1.0 the agent moves randomly, often falling into the pit (–10) many times per episode. As ε decays (*exponential with τ = 300*):

```python
eps = eps_end + (eps_start - eps_end) * math.exp(-steps / 300)
```

returns climb towards 0 … +4. Occasional negative spikes remain due to residual exploration and vanilla DQN instability.

\---|---|
\| **I ran `!python hw4_1_naive_dqn.py` in Colab and got**<br>`error: unrecognized arguments: -f …kernel‑xxxx.json`. | That flag is injected by Jupyter. I swapped `parse_args()` for `parse_known_args()` so unknown flags are ignored. Please pull the new script and rerun. |
\| **Now it stops at**<br>`AttributeError: 'Gridworld' object has no attribute 'observation'`. | The legacy environment lacked a Gym‑like API. I wrapped it with `GridEnvWrapper`, adding `reset()`, `step()`, `render()`, and a flattened one‑hot observation. Updated script uploaded. |
\| **The code trains, but rewards plunge to –50 early on. Normal?** | Yes. At high ε (≈1) the agent explores randomly, often falling into the pit (–10). As ε decays it learns and returns rise toward 0 … +4. Occasional dips remain due to exploration plus vanilla DQN instability. |
\| **Greedy evaluation shows 7 steps with total +4. Is that optimal?** | Exactly. Shortest safe path: 6 moves × (–1) + terminal +10 = **+4**. Seven moves from `(0,3)` to `(0,0)` avoids the pit `(0,1)` and wall `(1,1)`. |
\| **So training is successful?** | Yes—the Naive DQN baseline now works and can serve as a reference for Double/Dueling variants in later tasks. |

---

##Technical Summary

### 1 | Environment

| Component  | Position      | Symbol | Reward             |
| ---------- | ------------- | ------ | ------------------ |
| **Goal**   | `(0,0)`       | `+`    | **+10** (terminal) |
| **Pit**    | `(0,1)`       | `-`    | **–10** (terminal) |
| **Wall**   | `(1,1)`       | `W`    | blocks move        |
| **Player** | `(0,3)` start | `P`    | step cost **–1**   |

*Board size:* 4 × 4 (static).
*State encoding:* 4 one‑hot planes (Player/Goal/Pit/Wall) flattened → **64‑D** vector.

### 2 | Agent & Hyper‑parameters

| Item            | Setting                                 |
| --------------- | --------------------------------------- |
| Network         | `Linear(64→128) → ReLU → Linear(128→4)` |
| Replay Buffer   | capacity 10 000, batch 64               |
| Target Net      | sync every 50 episodes                  |
| Exploration     | ε‑greedy, 1.0 → 0.05, decay τ = 300     |
| Discount γ      | 0.99                                    |
| Optimizer       | Adam, lr 1e‑3                           |
| Max steps / ep. | 50                                      |

### 3 | Results

* **Learning curve:** after \~200 episodes returns stabilise around 0 – +4 with sporadic spikes below –20.
* **Greedy test:** agent reliably reaches the goal in **7 moves**, total reward **+4** (optimal).
* **Artifact:** `training_curve.png` shows the convergence trend (see Colab output).

### 4 | Key Takeaways

1. **Replay Buffer + Target Network** are indispensable—removing either caused divergence in early trials.
2. Proper ε‑decay balances exploration (discovering the path) and exploitation (refining Q‑values).
3. A single hidden layer of 128 units already suffices for this tiny task; larger models did not help.
4. Negative outliers stem from residual exploration and Q‑over/under‑estimation typical of vanilla DQN.

![image](https://github.com/user-attachments/assets/c100301b-3b36-4d1e-994d-4689220a5f6a)

