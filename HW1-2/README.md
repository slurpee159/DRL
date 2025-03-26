# HW1-2: Policy Display and Value Evaluation

## Project Overview
This project is a simple Flask-based web app that simulates policy display and value evaluation on an n x n grid.
The user can choose the grid size (5 to 9), and the system will randomly generate the corresponding policy (arrows) and state values (V(s)), then display them in table format.

## 1. Prompt: Create a Flask web interface to input grid size and display random policy and value matrix
**Q: How can I build a Flask web app where users input the grid size (n) and the backend generates random policy and value matrices?**

**A:**
We use Flask to handle GET and POST requests at the root route. When the form is submitted, the backend uses NumPy to generate a random policy matrix (`np.random.choice([0,1,2,3], size=(n,n))`) and a value matrix (`np.random.uniform(-4, 1.5, size=(n,n))`), and renders them via `index.html`.

---

## 2. Prompt: How to render policy and value matrices in HTML
**Q: How do I display both matrices clearly on the web page?**

**A:**
In `index.html`, we use Jinja2 templating to loop through the matrices. The `value` matrix shows floating-point numbers, while the `policy` matrix uses a symbol dictionary to convert directions (0-3) into arrows (←, →, ↑, ↓).

---

## 3. Prompt: How to mark obstacles, start and end points
**Q: How do I randomly assign obstacles while preserving the start and end cells?**

**A:**
The start is always (0,0), and the end is (n-1,n-1). We place (n-2) obstacles in random cells, excluding the start, end, and any previously selected obstacle cells.

---

## 4. Prompt: Auto-launch browser when Flask server starts
**Q: Can the browser open automatically after I start the Flask server?**

**A:**
Yes, use Python’s `webbrowser` module inside a separate thread with a delay:
```python
threading.Thread(target=open_browser).start()
def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')
```

---

## 5. Prompt: Display direction symbols instead of numeric actions
**Q: How can I show ← ↑ → ↓ instead of 0 1 2 3 in the policy matrix?**

**A:**
Define a mapping in `app.py`:
```python
action_symbols = {
    0: '←',
    1: '→',
    2: '↑',
    3: '↓'
}
```
Then access it in Jinja2 with `action_symbols[policy[i][j]]`.

---

## Features
- Grid size selectable between 5 and 9
- Random start and end points
- (n-2) random gray obstacles
- Value matrix: each cell shows a random float between -4 and 1.5
- Policy matrix: each cell shows an arrow indicating action





---


![image](https://github.com/user-attachments/assets/dc03baa5-6db5-4350-a475-5028beb7713c)


