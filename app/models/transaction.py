from datetime import datetime, timezone
from enum import Enum
from decimal import Decimal #для денег лучше decimal

class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value


class Transaction:

    def __init__(
            self, 
            portfolio_id : int,
            asset_id: int,
            transaction_type: TransactionType,
            quantity: Decimal,
            price: Decimal,
            id: int | None = None,
            comission: Decimal = Decimal("0"),
            transaction_date: datetime | None = None,
        ):

        self.portfolio_id = portfolio_id
        self.asset_id = asset_id

        if not isinstance(transaction_type, TransactionType):
            raise ValueError("Transaction must be a TransactionType enum value")
        self.transaction_type = transaction_type

        if quantity <= 0:
            raise ValueError ("Quantity must be positive number")
        self.quantity = quantity

        if price <= 0:
            raise ValueError ("Price must be positive number")
        self.price = price

        if comission < 0:
            raise ValueError ("Comission cant be negative number")
        self.comission = comission

        self.transaction_date = transaction_date or datetime.now(timezone.utc)

    @property
    def total_amount(self) -> Decimal:
        return self.quantity * self.price

    @property
    def total_with_comission(self) -> Decimal:
        return self.total_amount + self.comission   
    
    def is_buy(self) -> bool:
        return self.transaction_type == TransactionType.BUY
    
    def is_sell(self) -> bool:
        return self.transaction_type == TransactionType.SELL
    
    @classmethod
    def create_buy(
        cls,
        portfolio_id: int,
        asset_id: int,
        quantity: Decimal,
        price: Decimal,
        **kwargs #что за kwargs 
        ) -> Transaction:
        
            return cls(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                transaction_type=TransactionType.BUY,
                quantity=quantity,
                price=price,
                **kwargs
            )
    
    @classmethod
    def create_sell(
        cls,
        portfolio_id: int,
        asset_id: int,
        quantity: Decimal,
        price: Decimal,
        **kwargs
    ) -> "Transaction":
        
            return cls(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                transaction_type=TransactionType.SELL,
                quantity=quantity,
                price=price,
                **kwargs
            )

    def __repr__(self):
         type_str = "BUY" if self.is_buy() else "SELL"
         return f"<Transaction {type_str} {self.quantity} of asset {self.asset_id}>"        