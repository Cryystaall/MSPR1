from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from typing import List
from . import models
from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError


# ---------------------- Get All Situations Pandémiques ----------------------
def get_situations_pandemiques(db: Session, skip: int = 0, limit: int = 100):
    try:
        # Query the database for situations with pagination
        return db.query(models.SituationPandemique).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        # Log or handle SQL errors if necessary
        raise e  # Re-raise the error to be caught by the route handler


# ---------------------- GET Situation Pandémique BY PRIMARY KEYS ----------------------
def get_situation_pandemique(db: Session, id_pays: int, id_maladie: int, date_observation: str):
    situation = db.query(models.SituationPandemique).filter(
        models.SituationPandemique.id_pays == id_pays,
        models.SituationPandemique.id_maladie == id_maladie,
        models.SituationPandemique.date_observation == date_observation
    ).first()

    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    return situation


# ---------------------- CREATE a Single Situation Pandémique ----------------------
def create_situation_pandemique(db: Session, situation_data: schemas.SituationPandemiqueCreate):
    # Vérifier l'existence de la maladie et du pays
    if not db.query(models.Maladie).filter(models.Maladie.id_maladie == situation_data.id_maladie).first():
        raise HTTPException(status_code=404, detail="Maladie non trouvée")

    if not db.query(models.Pays).filter(models.Pays.id_pays == situation_data.id_pays).first():
        raise HTTPException(status_code=404, detail="Pays non trouvé")

    new_situation = models.SituationPandemique(**situation_data.dict())

    db.add(new_situation)
    db.commit()
    db.refresh(new_situation)

    return new_situation


# Bulk Insert Function with Chunking and SQLAlchemy's bulk_save_objects
def create_situations_bulk(db: Session, situations_data: List[schemas.SituationPandemiqueCreate], chunk_size: int = 1000):
    total_inserted = 0
    new_situations = []
    
    # Loop through data and chunk it
    for i, situation_data in enumerate(situations_data):
        # Validate country and disease existence
        if not db.query(models.Maladie).filter(models.Maladie.id_maladie == situation_data.id_maladie).first():
            raise HTTPException(status_code=404, detail=f"Maladie with ID {situation_data.id_maladie} not found")
        if not db.query(models.Pays).filter(models.Pays.id_pays == situation_data.id_pays).first():
            raise HTTPException(status_code=404, detail=f"Pays with ID {situation_data.id_pays} not found")

        new_situations.append(models.SituationPandemique(**situation_data.dict()))
        
        # Insert in chunks
        if len(new_situations) >= chunk_size:
            try:
                db.bulk_save_objects(new_situations)
                db.commit()  # Commit chunk to DB
                total_inserted += len(new_situations)
                new_situations = []  # Reset for next batch
            except exc.SQLAlchemyError as e:
                db.rollback()  # Rollback in case of error
                raise HTTPException(status_code=500, detail="Error during bulk insert.")
    
    # Insert any remaining situations
    if new_situations:
        try:
            db.bulk_save_objects(new_situations)
            db.commit()
            total_inserted += len(new_situations)
        except exc.SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error during bulk insert.")

    return {"message": f"{total_inserted} situations successfully added."}
# ---------------------- UPDATE a Situation Pandémique ----------------------
def update_situation_pandemique(db: Session, id_pays: int, id_maladie: int, date_observation: str,
                                situation_update: schemas.SituationPandemiqueUpdate):
    situation = db.query(models.SituationPandemique).filter(
        models.SituationPandemique.id_pays == id_pays,
        models.SituationPandemique.id_maladie == id_maladie,
        models.SituationPandemique.date_observation == date_observation
    ).first()

    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    for field, value in situation_update.dict(exclude_unset=True).items():
        setattr(situation, field, value)

    db.commit()
    db.refresh(situation)

    return situation



# ---------------------- DELETE a Situation Pandémique ----------------------
def delete_situation_pandemique(db: Session, id_pays: int, id_maladie: int, date_observation: str):
    situation = db.query(models.SituationPandemique).filter(
        models.SituationPandemique.id_pays == id_pays,
        models.SituationPandemique.id_maladie == id_maladie,
        models.SituationPandemique.date_observation == date_observation
    ).first()

    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    db.delete(situation)
    db.commit()

    return {"message": "Situation pandémique supprimée avec succès"}
