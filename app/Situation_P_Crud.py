from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# ---------------------- GET ALL Situations Pandémiques ----------------------
def get_situations_pandemiques(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SituationPandemique).offset(skip).limit(limit).all()


# ---------------------- GET Situation Pandémique BY ID ----------------------
def get_situation_pandemique(db: Session, id_situation: int):
    situation = db.query(models.SituationPandemique).filter(models.SituationPandemique.id_situation == id_situation).first()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")
    return situation


# ---------------------- CREATE a Situation Pandémique ----------------------
def create_situation_pandemique(db: Session, situation_data: schemas.SituationPandemiqueCreate):
    # Vérifier si la maladie et le pays existent avant d'ajouter la situation
    maladie = db.query(models.Maladie).filter(models.Maladie.id_maladie == situation_data.id_maladie).first()
    pays = db.query(models.Pays).filter(models.Pays.id_pays == situation_data.id_pays).first()

    if not maladie:
        raise HTTPException(status_code=404, detail="Maladie non trouvée")
    if not pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")

    new_situation = models.SituationPandemique(
        id_pays=situation_data.id_pays,
        id_maladie=situation_data.id_maladie,
        date_observation=situation_data.date_observation,
        cas_confirmes=situation_data.cas_confirmes,
        deces=situation_data.deces,
        guerisons=situation_data.guerisons
    )
    db.add(new_situation)
    db.commit()
    db.refresh(new_situation)
    return new_situation


# ---------------------- UPDATE a Situation Pandémique ----------------------
def update_situation_pandemique(db: Session, id_situation: int, situation_update: schemas.SituationPandemiqueUpdate):
    situation = db.query(models.SituationPandemique).filter(models.SituationPandemique.id_situation == id_situation).first()

    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    # Mise à jour des champs uniquement si des valeurs sont fournies
    if situation_update.id_pays is not None:
        situation.id_pays = situation_update.id_pays
    if situation_update.id_maladie is not None:
        situation.id_maladie = situation_update.id_maladie
    if situation_update.date_observation is not None:
        situation.date_observation = situation_update.date_observation
    if situation_update.cas_confirmes is not None:
        situation.cas_confirmes = situation_update.cas_confirmes
    if situation_update.deces is not None:
        situation.deces = situation_update.deces
    if situation_update.guerisons is not None:
        situation.guerisons = situation_update.guerisons

    db.commit()
    db.refresh(situation)
    return situation


# ---------------------- DELETE a Situation Pandémique ----------------------
def delete_situation_pandemique(db: Session, id_situation: int):
    situation = db.query(models.SituationPandemique).filter(models.SituationPandemique.id_situation == id_situation).first()

    if not situation:
        raise HTTPException(status_code=404, detail="Situation pandémique non trouvée")

    db.delete(situation)
    db.commit()
    return {"message": "Situation pandémique supprimée avec succès"}
