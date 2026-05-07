from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router

from app.core.security import security


app = FastAPI(title="InvestApp")


app.include_router(users_router)
app.include_router(auth_router)

security.handle_errors(app)