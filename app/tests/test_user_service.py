import asyncio
from uuid import uuid4

import app.models

from app.database.session import AsyncSessionLocal

from app.repositories.user_repository import UserRepository

from app.services.user_service import UserService

from app.schemas.user import UserCreate


async def main():
    suffix = uuid4().hex[:6]

    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)

        service = UserService(user_repo)

        email = f"user_test_{suffix}@example.com"

        user = await service.register_user(
            UserCreate(
                email=email,
                full_name="Test User",
                password="123456",
            )
        )

        print("User created:")
        print(user.id, user.email, user.user_role)

        try:
            await service.register_user(
                UserCreate(
                    email=email,
                    full_name="Duplicate User",
                    password="123456",
                )
            )
        except ValueError as e:
            print("Duplicate email caught correctly:")
            print(e)

        authenticated_user = await service.authenticate_user(
            email=email,
            password="123456",
        )

        print("Authentication success:")
        print(authenticated_user.email if authenticated_user else None)

        failed_auth = await service.authenticate_user(
            email=email,
            password="wrong_password",
        )

        print("Authentication with wrong password:")
        print(failed_auth)

        updated_user = await service.change_password(
            user_id=user.id,
            old_password="123456",
            new_password="654321",
        )

        print("Password changed:")
        print(updated_user.email)

        auth_with_old_password = await service.authenticate_user(
            email=email,
            password="123456",
        )

        print("Auth with old password:")
        print(auth_with_old_password)

        auth_with_new_password = await service.authenticate_user(
            email=email,
            password="654321",
        )

        print("Auth with new password:")
        print(auth_with_new_password.email if auth_with_new_password else None)

        all_users = await service.list_all()

        print("Users count:")
        print(len(all_users))


if __name__ == "__main__":
    asyncio.run(main())