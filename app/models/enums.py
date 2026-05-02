from enum import Enum


class AssetType(str, Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    CURRENCY = "currency"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    RUB = "RUB"


class UserRole(str, Enum):
    INVESTOR = "investor"
    ADMIN = "admin"


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"