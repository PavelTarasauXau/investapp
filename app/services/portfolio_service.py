from app.models.portfolio import Portfolio
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.user_repository import UserRepository
from app.schemas.portfolio import PortfolioCreate


class PortfolioService:
    def __init__(
        self,
        portfolio_repo: PortfolioRepository,
        user_repo: UserRepository,
    ):
        self.portfolio_repo = portfolio_repo
        self.user_repo = user_repo

    async def create_portfolio(
        self,
        user_id: int,
        data: PortfolioCreate,
    ) -> Portfolio:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        portfolio = Portfolio(
            user_id=user_id,
            name=data.name,
            currency=data.currency,
            description=data.description,
        )

        return await self.portfolio_repo.create(portfolio)

    async def get_by_id(self, portfolio_id: int) -> Portfolio:
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")
        return portfolio

    async def get_user_portfolios(self, user_id: int) -> list[Portfolio]:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        return await self.portfolio_repo.get_by_user_id(user_id)

    async def get_active_user_portfolios(self, user_id: int) -> list[Portfolio]:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        return await self.portfolio_repo.get_active_by_user_id(user_id)

    async def rename_portfolio(
        self,
        portfolio_id: int,
        new_name: str,
    ) -> Portfolio:
        if not new_name or not new_name.strip():
            raise ValueError("Portfolio name cannot be empty")

        portfolio = await self.portfolio_repo.update(
            portfolio_id,
            {"name": new_name.strip()},
        )

        if portfolio is None:
            raise ValueError("Portfolio not found")

        return portfolio

    async def update_description(
        self,
        portfolio_id: int,
        description: str | None,
    ) -> Portfolio:
        portfolio = await self.portfolio_repo.update(
            portfolio_id,
            {"description": description.strip() if description else None},
        )

        if portfolio is None:
            raise ValueError("Portfolio not found")

        return portfolio

    async def deactivate_portfolio(self, portfolio_id: int) -> Portfolio:
        portfolio = await self.portfolio_repo.update(
            portfolio_id,
            {"is_active": False},
        )

        if portfolio is None:
            raise ValueError("Portfolio not found")

        return portfolio

    async def activate_portfolio(self, portfolio_id: int) -> Portfolio:
        portfolio = await self.portfolio_repo.update(
            portfolio_id,
            {"is_active": True},
        )

        if portfolio is None:
            raise ValueError("Portfolio not found")

        return portfolio

    async def delete_portfolio(self, portfolio_id: int) -> bool:
        deleted = await self.portfolio_repo.delete(portfolio_id)

        if not deleted:
            raise ValueError("Portfolio not found")

        return True