from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import create_db_and_tables
from .routes import products, users, orders, checkout

app = FastAPI()

# Configure CORS policy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://baecommerce.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

# Register API routers.
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(checkout.router)