# Grid World Value Iteration Web App

An interactive Flask web application to visualize and compute optimal policies using the **Value Iteration** algorithm on a customizable grid world.

---

## Overview
This project allows users to:
- Select grid size (3x3 to 10x10)
- Mark start, goal, and obstacle positions by clicking the grid
- Execute Value Iteration to compute and visualize:
  - Optimal policy (direction arrows)
  - State value function `V(s)`

---

## How to Run
```bash
pip install flask
python app.py
```
Then open your browser at `http://127.0.0.1:5000`

---

## File Structure
```
.
├── app.py           # Flask backend with value iteration logic
└── templates/
    └── index.html   # Frontend UI and JavaScript
```

---

## Programming-Focused Q&A

### 1. **How is the grid generated in the frontend?**
The grid is created dynamically in JavaScript using `createGrid()`:
```javascript
document.getElementById('gridContainer').style.gridTemplateColumns = `repeat(${gridSize}, 50px)`;
```
It appends `<div>` elements for each cell, sets data attributes for coordinates, and assigns a click handler.

---

### 2. **How are start, goal, and obstacles assigned?**
Using `handleCellClick(i, j, cell)` in JavaScript:
- First click → start (green)
- Second click → goal (red)
- Next (n-2) clicks → obstacles (gray)
All clicks modify `gridData` state.

---

### 3. **How is data sent to the backend?**
On "Run Value Iteration" click:
```javascript
fetch('/run_value_iteration', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ size, start, goal, obstacles })
});
```
The Flask backend parses the JSON and starts value iteration.

---

### 4. **How is Value Iteration implemented in Python?**
In `app.py`, the `value_iteration()` function:
```python
while True:
    for each state s:
        for each action a:
            compute reward + gamma * V(s')
        update V[s] = max over actions
    if max change < theta: break
```
Obstacles are skipped; the goal has reward 1.

---

### 5. **How are policy and value results returned?**
After computing `V` and `policy`, the Flask app returns:
```python
return jsonify({"V": V, "policy": policy})
```
Frontend parses and updates two grid views:
- `policyGrid`: shows arrows for actions
- `valueGrid`: shows numerical values

---

## Example Enhancements to Try
- Add stochastic transitions (e.g. slip left/right)
- Customize reward function
- Switch between Value Iteration and Policy Iteration
- Export policy/value as CSV

---

## Educational Use
This project is perfect for understanding:
- Markov Decision Processes (MDPs)
- Reinforcement Learning fundamentals
- Dynamic Programming

Feel free to explore, extend, and tweak it!

