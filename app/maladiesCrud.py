from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# ---------------------- GET All Maladies ----------------------
def get_maladies_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Maladie).offset(skip).limit(limit).all()

# ---------------------- GET Maladie by ID ----------------------
def get_maladie(db: Session, id_maladie: int):
    maladie = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    if not maladie:
        raise HTTPException(status_code=404, detail=f"Maladie avec l'ID {id_maladie} introuvable.")
    return maladie

# ---------------------- CREATE Maladie ----------------------
def create_maladie(db: Session, maladie: schemas.MaladieCreate):
    # Vérifier si la maladie existe déjà
    existing_maladie = db.query(models.Maladie).filter(models.Maladie.nom_maladie == maladie.nom_maladie).first()
    
    if existing_maladie:
        raise HTTPException(status_code=422, detail=f"La maladie '{maladie.nom_maladie}' existe déjà.")

    # Créer une nouvelle maladie
    db_maladie = models.Maladie(
        nom_maladie=maladie.nom_maladie,
        type_maladie=maladie.type_maladie,
        description=maladie.description
    )

    db.add(db_maladie)
    db.commit()
    db.refresh(db_maladie)
    
    return db_maladie


# ---------------------- UPDATE Maladie ----------------------
def update_maladie(db: Session, id_maladie: int, maladie_update: schemas.MaladieUpdate):
    maladie_to_update = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    
    if not maladie_to_update:
        raise HTTPException(status_code=404, detail=f"Maladie avec l'ID {id_maladie} introuvable.")

    # Mise à jour uniquement des champs fournis
    if maladie_update.nom_maladie is not None:
        maladie_to_update.nom_maladie = maladie_update.nom_maladie
    if maladie_update.type_maladie is not None:
        maladie_to_update.type_maladie = maladie_update.type_maladie
    if maladie_update.description is not None:
        maladie_to_update.description = maladie_update.description

    db.commit()
    db.refresh(maladie_to_update)
    
    return maladie_to_update

# ---------------------- DELETE Maladie ----------------------
def delete_maladie(db: Session, id_maladie: int):
    maladie_to_delete = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    
    if not maladie_to_delete:
        raise HTTPException(status_code=404, detail=f"Maladie avec l'ID {id_maladie} introuvable.")

    db.delete(maladie_to_delete)
    db.commit()
    
    return {"message": f"La maladie '{maladie_to_delete.nom_maladie}' a été supprimée avec succès."}
