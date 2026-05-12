import asyncio
from uuid import uuid4

from app.database.session import AsyncSessionLocal

import app.models

from app.models.user import User
from app.models.enums import Currency 

from app.repositories.user_repository import UserRepository
from app.repositories.portfolio_repository import PortfolioRepository

from app.services.portfolio_service import PortfolioService

from app.schemas.portfolio import PortfolioCreate


async def main():
    suffix = uuid4().hex[:6].upper()

    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        portfolio_repo = PortfolioRepository(session)

        service = PortfolioService(
            portfolio_repo=portfolio_repo,
            user_repo=user_repo,
        )

        user = await user_repo.create(
            User(
                email=f"portfolio_test_{suffix}@example.com",
                full_name="Portfolio Test User",
                password_hash="fake_hash",
            )
        )

        portfolio = await service.create_portfolio(
            user_id=user.id,
            data=PortfolioCreate(
                name=" Main Portfolio ",
                currency=Currency.USD,
                description=" Test description ",
            ),
        )

        print("Portfolio created:", portfolio.id, portfolio.name, portfolio.currency)

        portfolios = await service.get_user_portfolios(user.id)
        print("User portfolios count:", len(portfolios))

        active_portfolios = await service.get_active_user_portfolios(user.id)
        print("Active portfolios count:", len(active_portfolios))

        renamed = await service.rename_portfolio(
            portfolio_id=portfolio.id,
            new_name="Renamed Portfolio",
        )
        print("Portfolio renamed:", renamed.name)

        updated = await service.update_description(
            portfolio_id=portfolio.id,
            description="Updated description",
        )
        print("Description updated:", updated.description)

        deactivated = await service.deactivate_portfolio(portfolio.id)
        print("Portfolio active after deactivate:", deactivated.is_active)

        active_after_deactivate = await service.get_active_user_portfolios(user.id)
        print("Active portfolios after deactivate:", len(active_after_deactivate))

        activated = await service.activate_portfolio(portfolio.id)
        print("Portfolio active after activate:", activated.is_active)

        try:
            await service.create_portfolio(
                user_id=999999,
                data=PortfolioCreate(
                    name="Broken Portfolio",
                    currency=Currency.USD,
                    description=None,
                ),
            )
        except ValueError as e:
            print("Invalid user caught correctly:", e)

        deleted = await service.delete_portfolio(portfolio.id)
        print("Portfolio deleted:", deleted)


if __name__ == "__main__":
    asyncio.run(main())