from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init_grid', methods=['POST'])
def init_grid():
    n = int(request.json['size'])
    return jsonify({"grid": [["" for _ in range(n)] for _ in range(n)]})

@app.route('/run_value_iteration', methods=['POST'])
def run_value_iteration():
    data = request.json
    n = data['size']
    start = tuple(data['start'])
    goal = tuple(data['goal'])
    obstacles = [tuple(ob) for ob in data['obstacles']]

    V, policy = value_iteration(n, start, goal, obstacles)
    return jsonify({"V": V, "policy": policy})

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

if __name__ == '__main__':
    app.run(debug=True)