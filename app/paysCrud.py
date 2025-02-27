from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def get_pays(db: Session, id_pays: int):
    return db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()

# Get all Pays
def get_pays_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pays).offset(skip).limit(limit).all()

# Create a new Pays
def create_pays(db: Session, pays: schemas.PaysCreate):
    # Check if the country already exists
    existing_pays = db.query(models.Pays).filter(models.Pays.nom_pays == pays.nom_pays).first()
    
    if existing_pays:
        raise HTTPException(status_code=422, detail=f"Country {pays.nom_pays} already exists.")
    
    # Create new pays
    db_pays = models.Pays(nom_pays=pays.nom_pays, region_oms=pays.region_oms)
    
    db.add(db_pays)
    db.commit()
    db.refresh(db_pays)
    
    return db_pays


# Update an existing Pays
def update_pays(db: Session, id_pays: int, pays: schemas.PaysUpdate):
    pays_to_update = db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()
    if pays_to_update:
        # Update fields from the pays_update schema
        pays_to_update.nom_pays = pays.nom_pays
        pays_to_update.region_oms = pays.region_oms  # Assuming this is also part of the update schema
        
        # Commit the changes
        db.commit()
        db.refresh(pays_to_update)
        return pays_to_update
    else:
        return None

# Delete an existing Pays
def delete_pays(db: Session, id_pays: int):
    pays_to_delete = db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()
    if pays_to_delete:
        db.delete(pays_to_delete)
        db.commit()
        return pays_to_delete
    else:
        return None
