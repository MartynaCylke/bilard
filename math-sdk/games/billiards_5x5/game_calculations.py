from typing import List, Tuple, Dict
from .game_config import NUM_REELS, NUM_ROWS, PAYTABLE, JACKPOT_TRIGGER_SYMBOL, JACKPOT_MIN_CLUSTER, JACKPOT_MULTIPLIER

def neighbors(r:int,c:int):
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        yield r+dr, c+dc

def find_clusters(board: List[List[str]]) -> List[Tuple[str, List[Tuple[int,int]]]]:
    R, C = len(board), len(board[0])
    seen = [[False]*C for _ in range(R)]
    clusters = []
    for r in range(R):
        for c in range(C):
            if seen[r][c]: continue
            sym = board[r][c]
            stack=[(r,c)]; seen[r][c]=True; group=[(r,c)]
            while stack:
                rr,cc = stack.pop()
                for nr,nc in neighbors(rr,cc):
                    if 0<=nr<R and 0<=nc<C and not seen[nr][nc] and board[nr][nc]==sym:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        group.append((nr,nc))
            clusters.append((sym, group))
    return clusters

def evaluate_board(board: List[List[str]]) -> Dict:
    wins = []
    total = 0
    jackpot_hit = False

    for sym, cells in find_clusters(board):
        size = len(cells)
        for k in (5,4,3):            # płacimy raz na najwyższy próg
            if size >= k and (k, sym) in PAYTABLE:
                win = PAYTABLE[(k, sym)]
                wins.append({"symbol": sym, "kind": k, "win": win,
                             "positions": [{"row": r, "col": c} for r,c in cells]})
                total += win
                break
        if sym == JACKPOT_TRIGGER_SYMBOL and size >= JACKPOT_MIN_CLUSTER:
            jackpot_hit = True

    if jackpot_hit:
        wins.append({"symbol": JACKPOT_TRIGGER_SYMBOL, "kind": JACKPOT_MIN_CLUSTER, "win": JACKPOT_MULTIPLIER, "positions": []})
        total += JACKPOT_MULTIPLIER

    return {"wins": wins, "totalWin": total}
