import io, os, json, random
from typing import List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from zstandard import ZstdDecompressor

# --- USTAWIENIA ---
CURRENCY = "USD"        # <— waluta do frontu
DEFAULT_LANG = "en"     # <— język

# ---- wczytanie math files ----
PUBLISH_DIR = os.path.expanduser("~/math-sdk/games/billiards_5x5/library/publish_files")
BOOKS = os.path.join(PUBLISH_DIR, "books_base.jsonl.zst")

books: Dict[int, Dict] = {}
try:
    if os.path.isfile(BOOKS):
        with open(BOOKS, "rb") as f:
            dctx = ZstdDecompressor()
            with dctx.stream_reader(f) as reader:
                for i, line in enumerate(io.TextIOWrapper(reader, "utf-8")):
                    try:
                        obj = json.loads(line)
                        sid = int(obj.get("sim_id", i+1))
                        books[sid] = obj
                    except Exception:
                        pass
    else:
        print(f"[mock_rgs] Brak pliku: {BOOKS} — użyję fallbacku.")
except Exception as e:
    print(f"[mock_rgs] UWAGA: problem przy wczytywaniu publish_files: {e}. Używam fallbacku.")

sim_ids: List[int] = list(books.keys()) if books else list(range(1, 2001))

# ---- API ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthReq(BaseModel):
    sessionID: str

class PlayReq(BaseModel):
    sessionID: str
    amount: int
    mode: str = "BASE"

class EndReq(BaseModel):
    sessionID: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/wallet/authenticate")
def authenticate(req: AuthReq):
    # kluczowe: currency i opcjonalnie lang
    return {"balance": {"amount": 10_000_000_000, "currency": CURRENCY}, "lang": DEFAULT_LANG}

@app.post("/play")
def play(req: PlayReq):
    sid = random.choice(sim_ids)
    rec = books.get(sid, {"board": [], "win": 0})
    events = [
        {"type": "setBoard", "board": rec.get("board", [])},
        {"type": "setTotalWin", "amount": int(rec.get("win", 0))}
    ]
    return {
        "balance": {"amount": 10_000_000_000 - int(req.amount), "currency": CURRENCY},
        "round": {"events": events}
    }

@app.post("/wallet/end-round")
def end_round(req: EndReq):
    return {"balance": {"amount": 10_000_000_000, "currency": CURRENCY}}
