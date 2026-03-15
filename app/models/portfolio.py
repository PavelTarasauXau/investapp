from enum import Enum
from datetime import datetime, timezone


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    
    def __str__(self):
        return self.value


class Portfolio:
    def __init__(        
            self,
            user_id: int,
            name: str,
            currency: Currency,
            id: int | None = None,
            description: str | None = None,
            created_at: datetime | None = None,
            is_active: bool = True
        ):

        if not name or not name.strip():
            raise ValueError("Portfolio name cannot be empty")
        self.name = name.strip()
        
        if not isinstance(currency, Currency):
            raise ValueError("Currency must be a Currency enum value")
        
        self.id = id
        self.user_id = user_id
        self.currency = currency
        self.description = description.strip() if description else None
        self.created_at = created_at or datetime.now(timezone.utc)
        self.is_active = is_active

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.currency.value})"

    def deactivate(self):
        self.is_active = False
    
    def activate(self):
        self.is_active = True
    
    def belongs_to(self, user_id: int) -> bool:
        return self.user_id == user_id
    
    @classmethod
    def create_default(cls, user_id: int, currency: Currency = Currency.USD) -> "Portfolio":
        return cls(
            user_id=user_id,
            name="Main",
            currency=currency
        )
    
    def __repr__(self):
        return f"<Portfolio {self.display_name}>"
    
    #добавить потом
    def rename(self, new_name):
        pass

    #это тоже    
    def change_currency(self, new_currency):
        pass