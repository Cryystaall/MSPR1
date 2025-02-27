from fastapi import FastAPI
from .routes import paysData
from .routes import maladiesData

app = FastAPI()

app.include_router(paysData.router, prefix="/api", tags=["PAY CRUD"])
app.include_router(maladiesData.router, prefix="/api", tags=["MALADIES CRUD"])

@app.get("/")
def root():
    return {"message": "Welcome to the API"}
