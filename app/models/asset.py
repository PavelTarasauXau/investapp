from enum import Enum
import re

class AssetType(Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    CURRENCY = "currency" 

class Asset:

    def __init__(
        self,
        ticker: str,
        name: str,
        asset_type: AssetType,
        id: int | None = None,
        isin: str | None = None
    ):
        
        if not ticker or not ticker.strip():
            raise ValueError("Ticker cannot be empty")
        if len(ticker) > 20:
            raise ValueError("Ticker too long (max 20 chars)")
        self.ticker = ticker.upper().strip()
        
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        self.name = name.strip()
        
        if not isinstance(asset_type, AssetType):
            raise ValueError("Asset type must be an AssetType enum value")
        self.asset_type = asset_type
        
        if isin and not self._validate_isin(isin):
            raise ValueError(f"Invalid ISIN format: {isin}")
        self.isin = isin.upper().strip() if isin else None
        
        self.id = id

    @staticmethod
    def _validate_isin(isin: str) -> bool:
        """Проверяет базовый формат ISIN"""
        if not isin:
            return True
        
        # ISIN: 2 буквы + 9 букв/цифр + 1 цифра
        pattern = r'^[A-Z]{2}[A-Z0-9]{9}[0-9]$'
        return bool(re.match(pattern, isin))


    @property
    def is_stock(self) -> bool:
        return self.asset_type == AssetType.STOCK
    

    @property
    def is_bond(self) -> bool:
        return self.asset_type == AssetType.BOND
    

    @property
    def is_etf(self) -> bool:
        return self.asset_type == AssetType.ETF
    

    @property
    def is_currency(self) -> bool:
        return self.asset_type == AssetType.CURRENCY
    

    @classmethod
    def create_stock(cls, ticker: str,name: str,isin: str | None = None) -> "Asset":
        return cls(
            ticker = ticker,
            name = name,
            asset_type = AssetType.STOCK,
            isin = isin
        )
    
    @classmethod
    def create_bond(cls, ticker: str, name: str, isin: str | None = None) -> "Asset":
        return cls(
            ticker=ticker,
            name=name,
            asset_type=AssetType.BOND,
            isin=isin
        )
    
    @classmethod
    def create_etf(cls, ticker: str, name: str, isin: str | None = None) -> "Asset":
        return cls(
            ticker=ticker,
            name=name,
            asset_type=AssetType.ETF,
            isin=isin
        )

    @classmethod
    def create_currency(cls, ticker: str, name: str) -> "Asset":
        return cls(
            ticker=ticker,
            name=name,
            asset_type=AssetType.CURRENCY,
            isin=None  # у валют нет ISIN
        )
    
    def __repr__(self):
        return f"<Asset {self.ticker} ({self.asset_type.value})>"



