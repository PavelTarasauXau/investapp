from fastapi import FastAPI
import uvicorn
from app.database.init_db import init_db

app = FastAPI(title="InvestApp")

@app.on_event("startup")
async def startup():
    await init_db()  # создаёт таблицы при старте если их нет

@app.get("/")
def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)