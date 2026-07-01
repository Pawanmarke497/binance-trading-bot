# Binance Trading Bot 🚀

A Python-based Binance Futures Testnet Trading Bot that allows users to place BUY and SELL orders from the command line using the Binance API.

## 📌 Features

- Place Market Orders
- Place Limit Orders
- Place Stop Orders
- Binance Futures Testnet Support
- Secure API Key Configuration using `.env`
- Command Line Interface (CLI)
- Error Handling for API Requests

## 🛠️ Tech Stack

- Python 3
- python-binance
- python-dotenv
- Requests
- Binance Futures Testnet API

## 📂 Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── order.py
│   └── ...
│
├── cli.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Pawanmarke497/binance-trading-bot.git
```

Go to the project folder

```bash
cd binance-trading-bot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file.

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

## ▶️ Usage

### Market Buy

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Market Sell

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 100000 --time-in-force GTC
```

## 📷 Screenshots

Add screenshots of the project here.

## 📈 Future Improvements

- Live Price Monitoring
- Technical Indicators
- Stop Loss & Take Profit
- Trading Strategies
- Web Dashboard
- Telegram Notifications
- Docker Support

## ⚠️ Disclaimer

This project is intended for educational purposes only. Always test using the Binance Futures Testnet before using any real funds.

## 👨‍💻 Author

**Pawan Marke**

GitHub: https://github.com/Pawanmarke497
