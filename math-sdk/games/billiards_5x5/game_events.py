from typing import List, Dict
from .game_config import NUM_ROWS, NUM_REELS
from .game_calculations import evaluate_board

def make_reveal_event(board: List[List[str]]) -> Dict:
    flat = [board[r][c] for c in range(NUM_REELS) for r in range(NUM_ROWS[0])]
    return {"index": 0,"type": "reveal","board": flat,"gameType": "basegame","paddingPositions": [],"anticipation": []}

def build_book(board: List[List[str]], sim_id: int) -> Dict:
    winInfo = evaluate_board(board)
    return {
        "id": sim_id,
        "events": [
            make_reveal_event(board),
            {"index": 1, "type": "winInfo", **winInfo},
            {"index": 2, "type": "setWin", "amount": winInfo["totalWin"], "winLevel": 1},
            {"index": 3, "type": "setTotalWin", "amount": winInfo["totalWin"]},
        ],
        "payoutMultiplier": int(winInfo["totalWin"]),
        "criteria": "basegame",
        "baseGameWins": float(winInfo["totalWin"]),
        "freeGameWins": 0.0
    }
