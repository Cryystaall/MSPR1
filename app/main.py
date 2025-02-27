from fastapi import FastAPI
from .routes import paysData
from .routes import maladiesData
from .routes import Situation_P_Data

app = FastAPI()

app.include_router(paysData.router, prefix="/api", tags=["PAY CRUD"])
app.include_router(maladiesData.router, prefix="/api", tags=["MALADIES CRUD"])
app.include_router(Situation_P_Data.router, prefix="/api", tags=["SITUATION PANDEMIQUE CRUD"])

@app.get("/")
def root():
    return {"message": "Welcome to the API"}
