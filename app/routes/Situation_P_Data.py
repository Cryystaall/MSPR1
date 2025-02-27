from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import Situation_P_Crud, schemas

router = APIRouter()

# Créer une situation pandémique
@router.post("/situations/", response_model=schemas.SituationPandemique)
def create_situation(situation: schemas.SituationPandemiqueCreate, db: Session = Depends(get_db)):
    return Situation_P_Crud.create_situation_pandemique(db=db, situation_data=situation)

# Obtenir toutes les situations pandémiques
@router.get("/situations/", response_model=list[schemas.SituationPandemique])
def get_all_situations(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return Situation_P_Crud.get_situations_pandemiques(db=db, skip=skip, limit=limit)

# Obtenir une situation par ID
@router.get("/situations/{id_situation}", response_model=schemas.SituationPandemique)
def get_situation(id_situation: int, db: Session = Depends(get_db)):
    return Situation_P_Crud.get_situation_pandemique(db=db, id_situation=id_situation)

# Mettre à jour une situation
@router.put("/situations/{id_situation}", response_model=schemas.SituationPandemique)
def update_situation(id_situation: int, situation: schemas.SituationPandemiqueUpdate, db: Session = Depends(get_db)):
    return Situation_P_Crud.update_situation_pandemique(db=db, id_situation=id_situation, situation_update=situation)

# Supprimer une situation
@router.delete("/situations/{id_situation}")
def delete_situation(id_situation: int, db: Session = Depends(get_db)):
    return Situation_P_Crud.delete_situation_pandemique(db=db, id_situation=id_situation)
