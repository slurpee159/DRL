from flask import Flask, render_template, request
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        return render_template('index.html', n=n)
    return render_template('index.html', n=None)

def open_browser():
    time.sleep(1)  # 等待伺服器啟動
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
