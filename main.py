from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.login import router as login_router
from app.routes.receipts import router as receipts_router
from app.routes.cleaning import router as cleaning_router

app = FastAPI(
    title="Room Cleaning Backend",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(login_router)
app.include_router(receipts_router)
app.include_router(cleaning_router)


@app.get("/")
def home():

    return {
        "message": "Backend running"
    }