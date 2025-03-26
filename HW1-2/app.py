from flask import Flask, render_template, request
import webbrowser
import threading
import time
import numpy as np

app = Flask(__name__)

# 定義動作對應的箭頭符號
action_symbols = {
    0: '\u2190',  # 左
    1: '\u2192',  # 右
    2: '\u2191',  # 上
    3: '\u2193'   # 下
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        # 隨機生成策略與初始化值矩陣
        policy = np.random.choice([0, 1, 2, 3], size=(n, n))
        value = np.round(np.random.uniform(-4, 1.5, size=(n, n)), 2)

        # 隨機選定起點、終點與障礙
        start = (0, 0)
        end = (n-1, n-1)
        obstacles = []
        for _ in range(n - 2):
            while True:
                r, c = np.random.randint(0, n, size=2)
                if (r, c) != start and (r, c) != end and (r, c) not in obstacles:
                    obstacles.append((r, c))
                    break

        return render_template('index.html', n=n, policy=policy, value=value,
                               action_symbols=action_symbols,
                               start=start, end=end, obstacles=obstacles)
    return render_template('index.html', n=None)

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
