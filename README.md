# Billiards game prototype

Development workspace for a 5×5 billiards-themed game. It combines:

- `math-sdk/` — the local game-math implementation;
- `web-sdk/` — the Engine web SDK, pinned as a Git submodule;
- `rgs-mock/` — a small FastAPI wallet/RGS mock for local development.

The SDK directories originate from the Engine/Stake Engine projects. Review
their upstream licensing and contribution terms before redistributing derived
code.

## Clone

The frontend is a submodule, so clone recursively:

```bash
git clone --recurse-submodules https://github.com/MartynaCylke/bilard.git
cd bilard
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## Run the mock RGS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r rgs-mock/requirements.txt
cd rgs-mock
uvicorn mock_rgs:app --host 127.0.0.1 --port 8787
```

The default allowed browser origins are `http://localhost:3001` and
`http://127.0.0.1:3001`. Override them with a comma-separated
`MOCK_ALLOWED_ORIGINS` environment variable.

Set `MOCK_TEST_BOARD=1` to return a deterministic board during local testing.

Run the mock API tests with:

```bash
python -m pip install -r rgs-mock/requirements-dev.txt
cd rgs-mock
python -m pytest -q
```

## Math SDK tests

```bash
cd math-sdk
make setup
make test
```
