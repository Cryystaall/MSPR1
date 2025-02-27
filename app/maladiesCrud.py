from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# Get all maladies 
def get_maladies_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Maladie).offset(skip).limit(limit).all()


# Get one maladie by ID
def get_maladie(db: Session, id_maladie: int):
    maladie = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    if not maladie:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")
    return maladie


# Add a new maladie
def create_maladie(db: Session, maladie: schemas.MaladieCreate):
    existing_maladie = db.query(models.Maladie).filter(models.Maladie.nom_maladie == maladie.nom_maladie).first()
    if existing_maladie:
        raise HTTPException(status_code=422, detail=f"Maladie {maladie.nom_maladie} already exists.")

    # Create new Maladie instance
    db_maladie = models.Maladie(
        nom_maladie=maladie.nom_maladie,
        type_maladie=maladie.type_maladie,  # Ensure this is included if required
        description=maladie.description
    )
    
    # Add and commit changes
    db.add(db_maladie)
    db.commit()
    db.refresh(db_maladie)
    return db_maladie


# Update a maladie
def update_maladie(db: Session, id_maladie: int, maladie_update: schemas.MaladieUpdate):
    maladie_to_update = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    if not maladie_to_update:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")

    # Update fields
    maladie_to_update.nom_maladie = maladie_update.nom_maladie
    maladie_to_update.type_maladie = maladie_update.type_maladie  # Include if required
    maladie_to_update.description = maladie_update.description

    # Commit changes
    db.commit()
    db.refresh(maladie_to_update)
    return maladie_to_update


# Delete a maladie
def delete_maladie(db: Session, id_maladie: int):
    maladie_to_delete = db.query(models.Maladie).filter(models.Maladie.id_maladie == id_maladie).first()
    if not maladie_to_delete:
        raise HTTPException(status_code=404, detail=f"Maladie with ID {id_maladie} not found.")

    db.delete(maladie_to_delete)
    db.commit()
    return maladie_to_delete
