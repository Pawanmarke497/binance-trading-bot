# Trading Bot — Binance Futures Testnet (USDT-M)

A small, structured Python CLI application that places MARKET, LIMIT, and
Stop-Limit orders on the Binance Futures Testnet, with input validation,
structured logging, and clean error handling.

## Project structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper (network layer)
│   ├── orders.py          # Order-building & placement logic
│   ├── validators.py      # CLI input validation
│   └── logging_config.py  # Logging setup (console + rotating file)
├── cli.py                 # CLI entry point (argparse)
├── logs/
│   └── trading_bot.log    # Generated at runtime
├── requirements.txt
├── .env.example
└── README.md
```

## Setup steps

### 1. Create a Binance Futures Testnet account and API keys

1. Go to https://testnet.binancefuture.com
2. Log in with a GitHub account (this is how the testnet authenticates).
3. Once logged in, go to **API Key** (usually under your profile / API
   management section) and generate a new API key + secret.
4. Copy both values — the secret is only shown once.
5. Your testnet account starts with fake USDT funds you can trade with.

### 2. Install dependencies

```bash
cd trading_bot
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your testnet key/secret:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

The app loads these via `python-dotenv`; they are never hardcoded or logged.

## How to run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

### Bonus: Stop-Limit order

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.01 --price 64000 --stop-price 64500
```

Every run prints:
- An **order request summary** (the exact parameters sent)
- The **order response** (`orderId`, `status`, `executedQty`, `avgPrice`)
- A clear **success/failure** message

All of this — plus the raw API request/response payloads and any errors —
is also written to `logs/trading_bot.log`.

### Generating the required deliverable logs

Run one MARKET order and one LIMIT order command above (with small
quantities, e.g. `0.01` BTCUSDT, so as not to run out of testnet funds), then
attach the resulting `logs/trading_bot.log` file — it will contain a
timestamped entry for both.

## Assumptions

- The bot targets **USDT-M Futures** only (not Coin-M or Spot).
- Only one order is placed per CLI invocation (no batch/queue support) —
  this matches the "simplified" scope of the task.
- `quantity` and `price` precision/step-size rules (Binance's `LOT_SIZE` /
  `PRICE_FILTER` symbol filters) are enforced by the exchange itself; the
  app does not pre-round values to the symbol's tick size. If an order is
  rejected for precision reasons, the Binance error message is surfaced
  and logged as-is.
- Default `timeInForce` for LIMIT/STOP orders is `GTC` (Good-Till-Cancelled),
  overridable via `--time-in-force`.
- Credentials are read only from environment variables / `.env` — never
  passed as CLI arguments, to avoid them leaking into shell history or logs.
- The Stop-Limit order type was chosen as the bonus feature (over OCO/TWAP/Grid)
  since it maps directly onto the existing LIMIT code path with one extra
  parameter (`stopPrice`), keeping the codebase small and consistent.

## Error handling

- **Invalid input** (bad symbol format, invalid side/type, missing price
  for LIMIT/STOP, non-numeric quantity, etc.) is caught by `validators.py`
  before any network call is made, and reported with a clear message.
- **API errors** (e.g. insufficient balance, invalid symbol, bad signature)
  raise `BinanceAPIException` / `BinanceOrderException`, which are caught,
  logged with the Binance error code/message, and re-raised so the CLI can
  exit with a clear failure message.
- **Network failures** (timeouts, connection errors) are caught by a
  general exception handler in `client.py` and logged before failing
  gracefully.

## Notes

- This tool is for **testnet use only**. Do not point it at production
  Binance API endpoints with real funds without a thorough security review.
