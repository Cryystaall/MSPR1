from fastapi import FastAPI
from .routes import data

app = FastAPI()

app.include_router(data.router, prefix="/api", tags=["Data"])

@app.get("/")
def root():
    return {"message": "Welcome to the API"}
