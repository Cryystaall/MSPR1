from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import paysCrud, schemas

router = APIRouter()

# Create a new Pays
@router.post("/pays/", response_model=schemas.Pays)
def create_pays(pays: schemas.PaysCreate, db: Session = Depends(get_db)):
    return paysCrud.create_pays(db=db, pays=pays)

@router.get("/pays/{id_pays}")
def read_pays(id_pays: int, db: Session = Depends(get_db)):
    pays = paysCrud.get_pays(db, id_pays)
    if pays is None:
        raise HTTPException(status_code=404, detail="Pays not found")
    return pays

# Get all Pays
@router.get("/pays/", response_model=list[schemas.Pays])
def read_pays_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pays_list = paysCrud.get_pays_list(db, skip=skip, limit=limit)
    return pays_list

# Update a Pays

@router.put("/pays/{id_pays}", response_model=schemas.Pays)
def update_pays(id_pays: int, pays_update: schemas.PaysUpdate, db: Session = Depends(get_db)):
    # Check if the pays exists
    pays = paysCrud.get_pays(db, id_pays)
    if pays is None:
        raise HTTPException(status_code=404, detail="Pays not found")
    
    # Call the function to update the pays in the database
    updated_pays = paysCrud.update_pays(db, id_pays, pays_update)
    if updated_pays is None:
        raise HTTPException(status_code=400, detail="Error updating pays")
    
    return updated_pays

# delete pay
@router.delete("/pays/{id_pays}", response_model=schemas.Pays)
def delete_pays(id_pays: int, db: Session = Depends(get_db)):
    # Check if the pays exists
    pays = paysCrud.get_pays(db, id_pays)
    if pays is None:
        raise HTTPException(status_code=404, detail="Pays not found")
    
    # Call the function to delete the pays in the database
    deleted_pays = paysCrud.delete_pays(db, id_pays)
    if deleted_pays is None:
        raise HTTPException(status_code=400, detail="Error deleting pays")
    
    # Return success message and deleted pays object as response
    # Just return the deleted pays as the response, FastAPI will handle serialization
    return deleted_pays