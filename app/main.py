from fastapi import FastAPI
import uvicorn
from app.database.init_db import init_db
from app.api.users import router as users_router

app = FastAPI(title="InvestApp")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(users_router)

@app.get("/")
def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)