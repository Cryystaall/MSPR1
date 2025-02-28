from fastapi import FastAPI
from .routes import paysData, maladiesData, Situation_P_Data

# Initialize the FastAPI app
app = FastAPI()

# Include routers for different resources with specific prefixes and tags
app.include_router(paysData.router, prefix="/api", tags=["PAY"])
app.include_router(maladiesData.router, prefix="/api", tags=["MALADIE"])
app.include_router(Situation_P_Data.router, prefix="/api", tags=["SITUATION PANDEMIQUE"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the API"}
