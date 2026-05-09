from authx import AuthXConfig, AuthX
from passlib.context import CryptContext
from app.config import settings


config = AuthXConfig()

config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY

config.JWT_TOKEN_LOCATION = ["headers"]

config.JWT_ACCESS_COOKIE_NAME = "access_token"

config.JWT_ALGORITHM = "HS256"

config.JWT_HEADER_TYPE = "Bearer"

config.JWT_HEADER_NAME = "Authorization"


security = AuthX(config=config)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )