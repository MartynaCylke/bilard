# ~/billiards-project/rgs-mock/mock_rgs.py
import os
import random
from typing import List

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# === ustawienia UI ===
CURRENCY = "USD"
DEFAULT_LANG = "en"

# skąd wolno łączyć frontowi w dev
ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://10.0.0.22:3001",
]

app = FastAPI(title="RGS Mock (billiards)")

# Uwaga: bez allow_private_network (ta wersja Starlette go nie zna)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Preflight / PNA (Chrome)
@app.options("/{path:path}")
def options_pna(path: str, request: Request):
    origin = request.headers.get("origin", "")
    headers = {
        "Access-Control-Allow-Origin": origin if origin in ALLOWED_ORIGINS else "",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "*"),
        "Access-Control-Max-Age": "600",
        # Chrome Private Network Access hint
        "Access-Control-Allow-Private-Network": "true",
    }
    return Response(status_code=204, headers=headers)

# ===== modele =====
class AuthReq(BaseModel):
    sessionID: str

class PlayReq(BaseModel):
    sessionID: str
    amount: int = 100
    mode: str = "BASE"

class EndReq(BaseModel):
    sessionID: str

# ===== logika rundy =====
SYMBOLS: List[str] = ["W", "L4", "L1", "H3", "S", "H4", "L2", "H1", "H2", "L3"]

def random_board(rows: int = 5, cols: int = 5) -> List[List[str]]:
    return [[random.choice(SYMBOLS) for _ in range(cols)] for __ in range(rows)]

# deterministyczna plansza dla pierwszego spina (do debugowania)
FIXED_BOARD_ENABLED = os.environ.get("MOCK_TEST_BOARD") == "1"
_FIXED_USED = False
TEST_BOARD = [
    ["H1","H2","H3","H4","L1"],
    ["L1","L2","L3","L4","W"],
    ["H1","H2","S","H4","L1"],
    ["L1","W","L3","L4","H2"],
    ["H1","H2","H3","H4","L1"],
]

# ===== endpointy =====
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/wallet/authenticate")
def authenticate(_: AuthReq):
    return {"balance": {"amount": 10_000_000_000, "currency": CURRENCY}, "lang": DEFAULT_LANG}

@app.post("/wallet/play")
def wallet_play(req: PlayReq):
    global _FIXED_USED
    board = TEST_BOARD if (FIXED_BOARD_ENABLED and not _FIXED_USED) else random_board(5, 5)
    if FIXED_BOARD_ENABLED and not _FIXED_USED:
        _FIXED_USED = True
    events = [
        {"type": "setBoard", "board": board},
        {"type": "setTotalWin", "amount": 0},
    ]
    return {
        "balance": {"amount": 10_000_000_000 - int(req.amount), "currency": CURRENCY},
        "round": {"events": events},
    }

# alias, gdy frontend strzela w /play zamiast /wallet/play
@app.post("/play")
def play_alias(req: PlayReq):
    return wallet_play(req)

@app.post("/wallet/end-round")
def end_round(_: EndReq):
    return {"balance": {"amount": 10_000_000_000, "currency": CURRENCY}}
