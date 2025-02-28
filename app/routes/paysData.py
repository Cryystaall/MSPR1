from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import paysCrud, schemas

router = APIRouter()

# ---------------------- Create a new Pays (Single) ----------------------
@router.post("/pays/", response_model=schemas.Pays)
def create_pays(pays: schemas.PaysCreate, db: Session = Depends(get_db)):
    return paysCrud.create_pays(db=db, pays=pays)

# ---------------------- Insert Multiple Pays Data ----------------------
@router.post("/pays/bulk", response_model=List[schemas.Pays])
def create_pays_bulk(pays_list: List[schemas.PaysCreate], db: Session = Depends(get_db)):
    created_pays = []
    for pays in pays_list:
        created_pays.append(paysCrud.create_pays(db=db, pays=pays))
    return created_pays

# ---------------------- Get All Pays ----------------------
@router.get("/pays/", response_model=List[schemas.Pays])
def read_pays_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paysCrud.get_pays_list(db, skip=skip, limit=limit)

# ---------------------- Update a Pays ----------------------
@router.put("/pays/{id_pays}", response_model=schemas.Pays)
def update_pays(id_pays: int, pays_update: schemas.PaysUpdate, db: Session = Depends(get_db)):
    # Check if the pays exists
    pays = paysCrud.get_pays(db, id_pays)
    if not pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")

    # Update pays
    updated_pays = paysCrud.update_pays(db, id_pays, pays_update)
    if not updated_pays:
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour du pays")

    return updated_pays

# ---------------------- Delete Pays ----------------------
@router.delete("/pays/{id_pays}", response_model=schemas.Pays)
def delete_pays(id_pays: int, db: Session = Depends(get_db)):
    # Check if the pays exists
    pays = paysCrud.get_pays(db, id_pays)
    if not pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    
    # Delete pays
    deleted_pays = paysCrud.delete_pays(db, id_pays)
    if not deleted_pays:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression du pays")

    return deleted_pays
