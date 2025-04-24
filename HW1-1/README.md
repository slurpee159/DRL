## HW1-1 Flask Grid Map Selection Web App

### 1. Prompt: Create an Interactive n x n Grid Map (n from 5 to 9)

#### Question:
How can I build a dynamic grid-based web app using Flask that allows users to select a start cell, end cell, and obstacles?

#### Solution:
We use Flask to render an interactive HTML grid where users can select cells via mouse clicks. The grid is generated using Jinja2 templating, and JavaScript handles user interactions to mark start (green), end (red), and obstacles (gray).

#### Code Implementation:
**app.py**
```python
from flask import Flask, render_template, request
import webbrowser, threading, time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        return render_template('index.html', n=n)
    return render_template('index.html', n=None)

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
```

---

### 2. Prompt: Render Grid and Handle Click Events

#### Question:
How can I dynamically render a grid with numbers 1 to n² and handle clicks to mark start, end, and obstacles?

#### Solution:
Use Jinja2 in the HTML template to number cells from 1 to n². JavaScript is used to control the number of allowed start (1), end (1), and obstacles (n-2). A reset button clears the selection.

#### Code Implementation:
**templates/index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Grid Map</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        table { border-collapse: collapse; margin-top: 20px; }
        td {
            width: 50px; height: 50px;
            border: 1px solid #999;
            text-align: center;
            vertical-align: middle;
            cursor: pointer;
            font-size: 12px;
        }
        .start { background-color: green; color: white; }
        .end { background-color: red; color: white; }
        .obstacle { background-color: gray; color: white; }
        #reset-btn {
            margin-top: 10px;
            padding: 6px 12px;
        }
    </style>
</head>
<body>
    <h2>Select Grid Size (5 to 9)</h2>
    <form method="post">
        <input type="number" name="n" min="5" max="9" required>
        <button type="submit">Create Grid</button>
    </form>

    {% if n %}
    <h3>{{ n }} x {{ n }} Grid</h3>
    <button id="reset-btn">Reset Grid</button>
    <table id="grid">
        {% for i in range(n) %}
        <tr>
            {% for j in range(n) %}
            <td data-row="{{ i }}" data-col="{{ j }}">
                {{ loop.index0 + i * n + 1 }}
            </td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>

    <script>
        let startSet = false;
        let endSet = false;
        let obstacleCount = 0;
        const maxObstacles = {{ n }} - 2;

        const resetBtn = document.getElementById('reset-btn');
        const cells = document.querySelectorAll('#grid td');

        function resetGrid() {
            startSet = false;
            endSet = false;
            obstacleCount = 0;
            cells.forEach(cell => cell.classList.remove('start', 'end', 'obstacle'));
        }

        resetBtn.addEventListener('click', resetGrid);

        cells.forEach(cell => {
            cell.addEventListener('click', () => {
                if (!startSet) {
                    cell.classList.add('start');
                    startSet = true;
                } else if (!endSet && !cell.classList.contains('start')) {
                    cell.classList.add('end');
                    endSet = true;
                } else if (
                    obstacleCount < maxObstacles &&
                    !cell.classList.contains('start') &&
                    !cell.classList.contains('end') &&
                    !cell.classList.contains('obstacle')
                ) {
                    cell.classList.add('obstacle');
                    obstacleCount++;
                }
            });
        });
    </script>
    {% endif %}
</body>
</html>
```

---

### 3. Prompt: Auto-launch Browser

#### Question:
How can I make the Flask app automatically launch in a browser upon execution?

#### Solution:
Use Python's `webbrowser` module inside a `threading.Thread()` to open the app URL shortly after the server starts.

#### Code Snippet:
```python
def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
```

![image](https://github.com/user-attachments/assets/87a4ea39-6133-4a41-bb84-2ac35c3b863f)



