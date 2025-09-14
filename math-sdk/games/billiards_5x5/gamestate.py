import random
from typing import List
from .game_config import NUM_REELS, NUM_ROWS, REELSTRIPS
from .game_events import build_book

def random_board() -> List[List[str]]:
    rows = NUM_ROWS[0]; cols = NUM_REELS
    board = [[None for _ in range(cols)] for _ in range(rows)]
    for c in range(cols):
        col_syms = REELSTRIPS[c]
        for r in range(rows):
            board[r][c] = random.choice(col_syms)
    return board

def run_spin(sim_id:int):
    board = random_board()
    return build_book(board, sim_id)
