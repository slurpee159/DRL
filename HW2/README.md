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


---

## File Structure
```
.
├── app.py           # Flask backend with value iteration logic
└── templates/
    └── index.html   # Frontend UI and JavaScript
```

---

## Programming-Focused Q&A with Code Examples

### 1. **How to generate a dynamic grid on the webpage?**
You can create an n x n grid dynamically using JavaScript by appending `div` elements to a container and using CSS Grid layout. Here's how it's done:

**JavaScript Code (from `index.html`)**:
```javascript
function createGrid() {
    gridSize = parseInt(document.getElementById('gridSize').value);
    gridData = [];
    document.getElementById('gridContainer').style.gridTemplateColumns = `repeat(${gridSize}, 50px)`;
    document.getElementById('gridContainer').innerHTML = '';

    for (let i = 0; i < gridSize; i++) {
        gridData[i] = [];
        for (let j = 0; j < gridSize; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.onclick = () => handleCellClick(i, j, cell);
            gridData[i][j] = '';
            document.getElementById('gridContainer').appendChild(cell);
        }
    }
}
```
This function creates a grid and allows each cell to respond to click events.

---

### 2. **How to let users select start, goal, and obstacles?**
Clicking on the grid sequentially marks the start, goal, and obstacles. The logic is:
- First click → start (green)
- Second click → goal (red)
- Next (n-2) clicks → obstacles (gray)

**JavaScript Code:**
```javascript
function handleCellClick(i, j, cell) {
    if (!start) {
        start = [i, j];
        cell.classList.add('start');
    } else if (!goal) {
        goal = [i, j];
        cell.classList.add('goal');
    } else if (obstacles.length < gridSize - 2) {
        const key = `${i},${j}`;
        if (!obstacles.some(o => o[0] === i && o[1] === j)) {
            obstacles.push([i, j]);
            cell.classList.add('obstacle');
        }
    }
}
```

---

### 3. **How to send the grid data to the Flask backend?**
When the user clicks the **"Run Value Iteration"** button, an HTTP POST request is made to the server with grid configuration.

**JavaScript Code:**
```javascript
fetch('/run_value_iteration', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: gridSize, start, goal, obstacles })
});
```

---

### 4. **How to write the Value Iteration algorithm in Python?**
The core logic is implemented in Python and uses dynamic programming. Here's the core implementation:

**Python Code (from `app.py`)**:
```python
def value_iteration(n, start, goal, obstacles, gamma=0.9, theta=1e-4):
    V = [[0 for _ in range(n)] for _ in range(n)]
    policy = [["" for _ in range(n)] for _ in range(n)]
    actions = ['U', 'D', 'L', 'R']
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and (x, y) not in obstacles

    while True:
        delta = 0
        for i in range(n):
            for j in range(n):
                if (i, j) in obstacles or (i, j) == goal:
                    continue
                v = V[i][j]
                max_value = float('-inf')
                best_action = ''
                for a in actions:
                    dx, dy = directions[a]
                    ni, nj = i + dx, j + dy
                    if not is_valid(ni, nj):
                        ni, nj = i, j
                    reward = 1 if (ni, nj) == goal else 0
                    val = reward + gamma * V[ni][nj]
                    if val > max_value:
                        max_value = val
                        best_action = a
                V[i][j] = max_value
                policy[i][j] = best_action
                delta = max(delta, abs(v - V[i][j]))
        if delta < theta:
            break

    return V, policy
```

---

### 5. **How to return and display the results?**
The backend sends JSON with the policy and value matrix. The frontend renders arrows and values for each cell using this logic:

**JavaScript Code Snippet:**
```javascript
valueCell.innerHTML = `<div class='value'>${V[i][j].toFixed(2)}</div>`;
policyCell.innerHTML = `<div class='policy'>${arrow(policy[i][j])}</div>`;
```

Function `arrow()` converts policy letters to arrows:
```javascript
function arrow(action) {
    return { 'U': '↓', 'D': '↑', 'L': '→', 'R': '←' }[action] || '';
}
```

---


