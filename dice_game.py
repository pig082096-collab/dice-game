# dice_game.py
from flask import Flask, jsonify, render_template_string, session
import random

app = Flask(__name__)
app.secret_key = "dice-game-secret-key"  # 一定要有

HTML = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>骰子遊戲</title>
<style>
body {
    font-family: Arial;
    background: #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.game {
    background: white;
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    width: 300px;
}
button {
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    color: white;
}
.roll { background: #4CAF50; }
.reset { background: #f44336; margin-top: 10px; }
.dice { font-size: 60px; margin: 20px; }
</style>
</head>

<body>
<div class="game">
<h2>🎲 骰子遊戲</h2>
<div id="dice" class="dice">-</div>
<button class="roll" onclick="rollDice()">擲骰子</button><br>
<button class="reset" onclick="resetGame()">重新開始</button>
<p>總分：<span id="score">0</span></p>
<p>規則：擲到 1 分數歸零</p>
</div>

<script>
function rollDice() {
    fetch('/roll')
    .then(r => r.json())
    .then(data => {
        document.getElementById("dice").innerText = data.dice;
        document.getElementById("score").innerText = data.score;
    });
}

function resetGame() {
    fetch('/reset')
    .then(r => r.json())
    .then(data => {
        document.getElementById("dice").innerText = "-";
        document.getElementById("score").innerText = data.score;
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    session.setdefault("score", 0)
    return render_template_string(HTML)

@app.route("/roll")
def roll():
    dice = random.randint(1, 6)
    score = session.get("score", 0)

    if dice == 1:
        score = 0
    else:
        score += dice

    session["score"] = score
    return jsonify(dice=dice, score=score)

@app.route("/reset")
def reset():
    session["score"] = 0
    return jsonify(score=0)

