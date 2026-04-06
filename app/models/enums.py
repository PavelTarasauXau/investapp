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