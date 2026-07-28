from contextlib import asynccontextmanager

from app.api.laws import router as laws_router
from app.database import create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="耳学 PWA Backend API", lifespan=lifespan)

# CORSの設定（フロントエンドからの通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発中なのでとりあえず全て許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(laws_router)


@app.get("/")
def read_root():
    return {"message": "耳学 API サーバーは正常に稼働しています"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
