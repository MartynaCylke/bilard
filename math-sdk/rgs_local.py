
from flask import Flask, request, jsonify
from games.billiards_5x5.gamestate import run_spin
app = Flask(__name__)
balances = {}
@app.post("/play")
def play():
    data = request.get_json(force=True) or {}
    session = data.get("sessionID","local")
    amount = int(data.get("amount", 100000))
    balances[session] = balances.get(session, 1_000_000) - amount
    book = run_spin(1)
    win = 0
    for e in book["events"]:
        if e["type"] == "setTotalWin":
            win = int(e["amount"])
    balances[session] += win
    return jsonify({"round": book, "balance": {"amount": balances[session]}})
@app.post("/wallet/end-round")
def end_round():
    data = request.get_json(force=True) or {}
    session = data.get("sessionID","local")
    return jsonify({"balance": {"amount": balances.get(session, 1_000_000)}})
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
