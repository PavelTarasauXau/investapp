from authx import AuthXConfig, AuthX
from passlib.context import CryptContext


config = AuthXConfig()

config.JWT_SECRET_KEY = "super-secret-key-change-this"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_ALGORITHM = "HS256"


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