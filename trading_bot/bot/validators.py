"""
Validation for CLI-provided order parameters.
Every function raises ValueError with a clear, user-facing message on
invalid input, and returns the cleaned/normalized value on success.
"""
import re

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT", "STOP"}  # STOP = Stop-Limit (bonus)
VALID_TIME_IN_FORCE = {"GTC", "IOC", "FOK"}

# Binance futures symbols are uppercase alphanumeric, e.g. BTCUSDT, ETHUSDT
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValueError("Symbol is required, e.g. BTCUSDT.")
    symbol = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValueError(f"Invalid symbol format: '{symbol}'. Expected e.g. BTCUSDT.")
    return symbol


def validate_side(side: str) -> str:
    if not side:
        raise ValueError("Side is required (BUY or SELL).")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side: '{side}'. Must be one of {sorted(VALID_SIDES)}.")
    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValueError("Order type is required (MARKET, LIMIT or STOP).")
    order_type = order_type.strip().upper()
    if order_type not in VALID_TYPES:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be one of {sorted(VALID_TYPES)}.")
    return order_type


def validate_quantity(quantity) -> float:
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity must be a number, got '{quantity}'.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity


def validate_price(price, order_type: str):
    """Price is required for LIMIT and STOP orders, ignored for MARKET."""
    if order_type in ("LIMIT", "STOP"):
        if price is None:
            raise ValueError(f"--price is required for {order_type} orders.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Price must be a number, got '{price}'.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        return price
    return None


def validate_stop_price(stop_price, order_type: str):
    """Stop price is required only for STOP (stop-limit) orders."""
    if order_type == "STOP":
        if stop_price is None:
            raise ValueError("--stop-price is required for STOP orders.")
        try:
            stop_price = float(stop_price)
        except (TypeError, ValueError):
            raise ValueError(f"stop_price must be a number, got '{stop_price}'.")
        if stop_price <= 0:
            raise ValueError("stop_price must be greater than 0.")
        return stop_price
    return None


def validate_time_in_force(tif: str) -> str:
    tif = (tif or "GTC").strip().upper()
    if tif not in VALID_TIME_IN_FORCE:
        raise ValueError(f"Invalid time-in-force: '{tif}'. Must be one of {sorted(VALID_TIME_IN_FORCE)}.")
    return tif
