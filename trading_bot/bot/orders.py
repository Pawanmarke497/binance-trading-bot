"""
Order placement logic. Builds well-formed order payloads for MARKET,
LIMIT, and STOP (Stop-Limit, bonus) orders, prints a clean summary of
the request and response, and delegates the actual network call to
the client wrapper.
"""
import logging

from .client import BinanceFuturesTestnetClient

logger = logging.getLogger("trading_bot")


class OrderManager:
    def __init__(self, client: BinanceFuturesTestnetClient):
        self.client = client

    def build_order_params(
        self, symbol, side, order_type, quantity, price=None,
        stop_price=None, time_in_force="GTC",
    ):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "STOP" if order_type.upper() == "STOP" else order_type.upper(),
            "quantity": quantity,
        }

        order_type = order_type.upper()
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force
        elif order_type == "STOP":
            # Binance Futures stop-limit order: needs both price and stopPrice
            params["price"] = price
            params["stopPrice"] = stop_price
            params["timeInForce"] = time_in_force
        elif order_type == "MARKET":
            pass  # no extra params required
        else:
            raise ValueError(f"Unsupported order type: {order_type}")

        return params

    def place_market_order(self, symbol, side, quantity):
        params = self.build_order_params(symbol, side, "MARKET", quantity)
        return self._execute(params)

    def place_limit_order(self, symbol, side, quantity, price, time_in_force="GTC"):
        params = self.build_order_params(
            symbol, side, "LIMIT", quantity, price=price, time_in_force=time_in_force
        )
        return self._execute(params)

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price, time_in_force="GTC"):
        params = self.build_order_params(
            symbol, side, "STOP", quantity, price=price,
            stop_price=stop_price, time_in_force=time_in_force,
        )
        return self._execute(params)

    def _execute(self, params):
        logger.info("Order request summary: %s", params)
        print("\n--- Order Request ---")
        for k, v in params.items():
            print(f"{k:<12}: {v}")

        response = self.client.place_order(**params)

        print("\n--- Order Response ---")
        print(f"{'orderId':<12}: {response.get('orderId')}")
        print(f"{'status':<12}: {response.get('status')}")
        print(f"{'executedQty':<12}: {response.get('executedQty')}")
        print(f"{'avgPrice':<12}: {response.get('avgPrice', 'N/A')}")
        print("Result      : SUCCESS\n")

        logger.info(
            "Order placed successfully: orderId=%s status=%s executedQty=%s avgPrice=%s",
            response.get("orderId"), response.get("status"),
            response.get("executedQty"), response.get("avgPrice", "N/A"),
        )

        return response
