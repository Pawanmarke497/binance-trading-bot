#!/usr/bin/env python3
"""
CLI entry point for the Binance Futures Testnet trading bot.

Examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

    python cli.py --symbol BTCUSDT --side SELL --type LIMIT \\
        --quantity 0.01 --price 65000

    # Bonus order type: Stop-Limit
    python cli.py --symbol BTCUSDT --side BUY --type STOP \\
        --quantity 0.01 --price 64000 --stop-price 64500
"""
import argparse
import os
import sys

from dotenv import load_dotenv

from bot import validators
from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import OrderManager


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures Testnet trading bot."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--type", required=True, dest="order_type",
        help="MARKET, LIMIT, or STOP (stop-limit, bonus)",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Price (required for LIMIT/STOP)")
    parser.add_argument(
        "--stop-price", dest="stop_price",
        help="Stop trigger price (required for STOP orders)",
    )
    parser.add_argument(
        "--time-in-force", dest="time_in_force", default="GTC",
        help="GTC / IOC / FOK (default: GTC, used for LIMIT/STOP)",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    logger = setup_logging()

    args = parse_args()
    logger.debug("Raw CLI args: %s", vars(args))

    # ---- Validate input ----
    try:
        symbol = validators.validate_symbol(args.symbol)
        side = validators.validate_side(args.side)
        order_type = validators.validate_order_type(args.order_type)
        quantity = validators.validate_quantity(args.quantity)
        price = validators.validate_price(args.price, order_type)
        stop_price = validators.validate_stop_price(args.stop_price, order_type)
        time_in_force = validators.validate_time_in_force(args.time_in_force)
    except ValueError as e:
        logger.error("Input validation failed: %s", e)
        print(f"Input error: {e}")
        sys.exit(1)

    # ---- Load credentials ----
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # ---- Place order ----
    try:
        client = BinanceFuturesTestnetClient(api_key, api_secret)
        manager = OrderManager(client)

        if order_type == "MARKET":
            manager.place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            manager.place_limit_order(symbol, side, quantity, price, time_in_force)
        elif order_type == "STOP":
            manager.place_stop_limit_order(symbol, side, quantity, price, stop_price, time_in_force)

    except ValueError as e:
        # Config errors, e.g. missing credentials
        logger.error("Configuration error: %s", e)
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        # Network failures / Binance API errors already logged inside client.py
        print(f"Order failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
