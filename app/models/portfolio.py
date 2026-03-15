from enum import Enum
from datetime import datetime, timezone


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    
    def __str__(self):
        return self.value


class Portfolio:
    def __init__(self, user_id, name, currency: Currency, id=None, 
                 description=None, created_at=None, is_active=True):

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
    def display_name(self):
        return f"{self.name} ({self.currency.value})"

    def deactivate(self):
        self.is_active = False
    
    def activate(self):
        self.is_active = True
    
    def belongs_to(self, user_id):
        return self.user_id == user_id
    
    @classmethod
    def create_default(cls, user_id, currency=Currency.USD):
        return cls(
            user_id=user_id,
            name="Main",
            currency=currency
        )
    
    def __repr__(self):
        return f"<Portfolio {self.display_name}>"

"""
    if __name__ == "__main__":
        # Создаем портфель
        p1 = Portfolio(
            user_id=1,
            name="  Пенсионный  ",
            currency=Currency.USD,
            description="Для старости"
        )
        
        print(p1)  # <Portfolio Пенсионный (USD)>
        print(p1.display_name)  # Пенсионный (USD)
        print(f"Принадлежит пользователю 1? {p1.belongs_to(1)}")  # True
        print(f"Принадлежит пользователю 2? {p1.belongs_to(2)}")  # False
        
        # Создаем портфель по умолчанию
        p2 = Portfolio.create_default(user_id=1, currency=Currency.EUR)
        print(p2)  # <Portfolio Основной (EUR)>
        
        p2.deactivate()
        print(f"Активен? {p2.is_active}")  # False
"""