"""
Thin wrapper around python-binance's Client, scoped to the
USDT-M Futures Testnet. This is the only module that talks to
the network — everything else in the app depends on this
abstraction, not on python-binance directly, so the underlying
HTTP library could be swapped out without touching CLI/order logic.
"""
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

logger = logging.getLogger("trading_bot")


class BinanceFuturesTestnetClient:
    """Wraps python-binance's Client, forced onto the Futures Testnet."""

    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError(
                "Missing API credentials. Set BINANCE_API_KEY and "
                "BINANCE_API_SECRET (e.g. in a .env file)."
            )

        # testnet=True points python-binance at the testnet base URLs.
        self.client = Client(api_key, api_secret, testnet=True)
        # Belt-and-suspenders: explicitly pin the futures URL too, since
        # this has moved around across python-binance versions.
        self.client.FUTURES_URL = self.BASE_URL + "/fapi"

        logger.info("Initialized Binance Futures Testnet client (base_url=%s)", self.BASE_URL)

    def place_order(self, **kwargs):
        """
        Place a futures order. kwargs are forwarded to python-binance's
        futures_create_order, e.g.:
            symbol, side, type, quantity, price, timeInForce, stopPrice
        """
        logger.info("API REQUEST -> futures_create_order params=%s", kwargs)
        try:
            response = self.client.futures_create_order(**kwargs)
            logger.info("API RESPONSE <- %s", response)
            return response
        except BinanceAPIException as e:
            logger.error("Binance API error (code=%s): %s", e.code, e.message)
            raise
        except BinanceOrderException as e:
            logger.error("Binance order error: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected/network error while placing order: %s", e)
            raise

    def get_account_balance(self):
        """Convenience helper — useful for sanity-checking connectivity/credentials."""
        try:
            balances = self.client.futures_account_balance()
            logger.info("API RESPONSE <- futures_account_balance: %s", balances)
            return balances
        except BinanceAPIException as e:
            logger.error("Binance API error while fetching balance: %s", e.message)
            raise
