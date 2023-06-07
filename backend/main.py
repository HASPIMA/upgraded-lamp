from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.prisma import prisma

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
def read_root():
    return {"version": "0.0.0"}
