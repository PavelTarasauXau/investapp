from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.portfolios import router as portfolios_router
from app.api.assets import router as assets_router
from app.api.transactions import router as transactions_router
from app.api.dividends import router as dividends_router
from app.api.coupons import router as coupons_router
from app.api.analytics import router as analytics_router
from fastapi.openapi.utils import get_openapi

from app.core.security import security


app = FastAPI(title="InvestApp")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(portfolios_router)
app.include_router(assets_router)
app.include_router(transactions_router)
app.include_router(dividends_router)
app.include_router(coupons_router)
app.include_router(analytics_router)

security.handle_errors(app)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="InvestApp",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [
        {"BearerAuth": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/portfolio/{portfolio_id}")
async def portfolio_page(request: Request, portfolio_id: int):
    return templates.TemplateResponse(
        "portfolio.html",
        {
            "request": request,
            "portfolio_id": portfolio_id,
        }
    )


@app.get("/analytics/{portfolio_id}")
async def analytics_page(request: Request, portfolio_id: int):
    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "portfolio_id": portfolio_id,
        }
    )