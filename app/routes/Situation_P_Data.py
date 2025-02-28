from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import Situation_P_Crud, schemas
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# ---------------------- Create a new Situation Pandémique (Single) ----------------------
@router.post("/situations/", response_model=schemas.SituationPandemique)
def create_situation(situation: schemas.SituationPandemiqueCreate, db: Session = Depends(get_db)):
    return Situation_P_Crud.create_situation_pandemique(db=db, situation_data=situation)

# ---------------------- Insert Multiple Situation Pandémique Data ----------------------
@router.post("/situations/bulk", response_model=List[schemas.SituationPandemique])
def create_situations_bulk(situations_list: List[schemas.SituationPandemiqueCreate], db: Session = Depends(get_db)):
    created_situations = []
    for situation in situations_list:
        created_situations.append(Situation_P_Crud.create_situation_pandemique(db=db, situation_data=situation))
    return created_situations

# ---------------------- Get All Situations Pandémiques ----------------------
@router.get("/situations/", response_model=List[schemas.SituationPandemique])
def read_situations_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        # Get list of situations with pagination
        return Situation_P_Crud.get_situations_pandemiques(db, skip=skip, limit=limit)
    except SQLAlchemyError as e:
        # Catch database-related exceptions and provide more specific error message
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    except Exception as e:
        # Catch any other exception that is not database-related
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    

# ---------------------- Update a Situation Pandémique ----------------------
@router.put("/situations/{id_pays}/{id_maladie}/{date_observation}", response_model=schemas.SituationPandemique)
def update_situation(id_pays: int, id_maladie: int, date_observation: str,
                     situation_update: schemas.SituationPandemiqueUpdate, db: Session = Depends(get_db)):
    # Check if the situation exists
    situation = Situation_P_Crud.get_situation_pandemique(
        db=db, id_pays=id_pays, id_maladie=id_maladie, date_observation=date_observation
    )
    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    # Update the situation
    updated_situation = Situation_P_Crud.update_situation_pandemique(
        db=db, id_pays=id_pays, id_maladie=id_maladie, date_observation=date_observation, situation_update=situation_update
    )
    if not updated_situation:
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour de la situation")

    return updated_situation

# ---------------------- Delete Situation Pandémique ----------------------
@router.delete("/situations/{id_pays}/{id_maladie}/{date_observation}", response_model=schemas.SituationPandemique)
def delete_situation(id_pays: int, id_maladie: int, date_observation: str, db: Session = Depends(get_db)):
    # Check if the situation exists
    situation = Situation_P_Crud.get_situation_pandemique(
        db=db, id_pays=id_pays, id_maladie=id_maladie, date_observation=date_observation
    )
    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")
    
    # Delete the situation
    deleted_situation = Situation_P_Crud.delete_situation_pandemique(db=db, id_pays=id_pays, id_maladie=id_maladie, date_observation=date_observation)
    if not deleted_situation:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression de la situation")

    return deleted_situation
