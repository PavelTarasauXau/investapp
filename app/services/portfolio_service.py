from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import PortfolioCreate
from app.models.portfolio import Currency

class PortfolioService:
    def __init__(self, repo: PortfolioRepository):
        self.repo = repo

    async def create(self, user_id: int, data: PortfolioCreate):
        return await self.repo.create(user_id, data)

    async def create_default(self, user_id: int, currency: Currency = Currency.USD):
        data = PortfolioCreate(name="Main", currency=currency)
        return await self.repo.create(user_id, data)

    async def get_user_portfolios(self, user_id: int):
        return await self.repo.get_by_user_id(user_id)

    async def deactivate(self, portfolio_id: int, user_id: int):
        # проверяем что портфель принадлежит пользователю — важно
        portfolio = await self.repo.get_by_id(portfolio_id)
        if not portfolio or portfolio.user_id != user_id:
            raise ValueError("Portfolio not found or access denied")
        return await self.repo.update(portfolio_id, {"is_active": False})

    async def rename(self, portfolio_id: int, user_id: int, new_name: str):
        if not new_name.strip():
            raise ValueError("Name cannot be empty")
        portfolio = await self.repo.get_by_id(portfolio_id)
        if not portfolio or portfolio.user_id != user_id:
            raise ValueError("Portfolio not found or access denied")
        return await self.repo.update(portfolio_id, {"name": new_name.strip()})