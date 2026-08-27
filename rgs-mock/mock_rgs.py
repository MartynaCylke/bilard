# mock_rgs.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
import os
import random

app = FastAPI(title="RGS Mock", version="1.0")

# CORS: pozwól na dev z localhost:3001 itd.
DEFAULT_ORIGINS = ["http://localhost:3001", "http://127.0.0.1:3001"]
allowed_origins = [
    origin.strip()
    for origin in os.getenv("MOCK_ALLOWED_ORIGINS", ",".join(DEFAULT_ORIGINS)).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============
# MODELE
# ============
class AuthenticateReq(BaseModel):
    sessionID: str

class PlayReq(BaseModel):
    sessionID: str
    amount: int = Field(gt=0)
    mode: Literal["BASE", "BONUS"]
    force_result: Optional[dict] = Field(default=None, alias="__forceResult")

# ============
# POMOCNICZE
# ============
SYMBOLS_SAFE = ["H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4"]  # bez W/S

def board_5x5_safe() -> List[List[str]]:
    """Plansza 5×5 bez W/S, żeby UI nie szukało multiplierów."""
    b: List[List[str]] = []
    for _ in range(5):
        row = [random.choice(SYMBOLS_SAFE) for _ in range(5)]
        b.append(row)
    return b

# Deterministyczna plansza przy testach (łatwiej debugować)
TEST_BOARD = [
    ["H1","H2","H3","H4","L1"],
    ["L1","L2","L3","L4","L1"],
    ["H1","H2","H3","H4","L2"],
    ["L2","L3","L4","H1","H2"],
    ["H3","H4","L1","L2","L3"],
]

def make_board() -> List[List[str]]:
    if os.getenv("MOCK_TEST_BOARD") == "1":
        return TEST_BOARD
    return board_5x5_safe()

# prosta "baza" sald
BALANCES = {}

def get_balance(session: str) -> int:
    return BALANCES.get(session, 10_000_000_000)

def set_balance(session: str, amount: int) -> None:
    BALANCES[session] = amount

# ============
# ENDPOINTY
# ============
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/wallet/authenticate")
def wallet_auth(req: AuthenticateReq):
    # nie zmieniamy stanu, tylko zwracamy saldo + lang
    return {
        "balance": {"amount": get_balance(req.sessionID), "currency": "USD"},
        "lang": "en",
    }

@app.post("/wallet/play")
def wallet_play(req: PlayReq):
    # proste pomniejszenie salda
    current = get_balance(req.sessionID)
    new_balance = max(0, current - req.amount)
    set_balance(req.sessionID, new_balance)

    # stan rundy — UWAGA: "state", nie "events"
    state = [
        {"type": "setBoard", "board": make_board()},
        # można dorzucić inne (np. setWinLines / setExplosions), ale nie są wymagane
        {"type": "setTotalWin", "amount": 0},
    ]

    return {
        "balance": {"amount": new_balance, "currency": "USD"},
        "round": {"state": state},
    }

@app.post("/wallet/end-round")
def wallet_end_round(req: AuthenticateReq):
    # nic nie robi – zgodnie z web-sdk
    return {"ok": True}
