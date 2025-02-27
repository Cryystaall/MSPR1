from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import maladiesCrud, schemas

router = APIRouter()


# Create a new Maladie
@router.post("/maladies/", response_model=schemas.Maladie)
def create_maladie(maladie: schemas.MaladieCreate, db: Session = Depends(get_db)):
    return maladiesCrud.create_maladie(db=db, maladie=maladie)


# Get all Maladies
@router.get("/maladies/", response_model=list[schemas.Maladie])
def get_maladies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return maladiesCrud.get_maladies_list(db=db, skip=skip, limit=limit)


# Get a single Maladie by ID
@router.get("/maladies/{id_maladie}", response_model=schemas.Maladie)
def get_maladie(id_maladie: int, db: Session = Depends(get_db)):
    maladie = maladiesCrud.get_maladie(db=db, id_maladie=id_maladie)
    if not maladie:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")
    return maladie


# Update a Maladie by ID
@router.put("/maladies/{id_maladie}", response_model=schemas.Maladie)
def update_maladie(id_maladie: int, maladie_update: schemas.MaladieUpdate, db: Session = Depends(get_db)):
    updated_maladie = maladiesCrud.update_maladie(db=db, id_maladie=id_maladie, maladie_update=maladie_update)
    if not updated_maladie:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")
    return updated_maladie


# Delete a Maladie by ID
@router.delete("/maladies/{id_maladie}", response_model=schemas.Maladie)
def delete_maladie(id_maladie: int, db: Session = Depends(get_db)):
    deleted_maladie = maladiesCrud.delete_maladie(db=db, id_maladie=id_maladie)
    if not deleted_maladie:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")
    return deleted_maladie
