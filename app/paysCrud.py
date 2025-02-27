from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# ---------------------- GET Pays by ID ----------------------
def get_pays(db: Session, id_pays: int):
    pays = db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()
    if not pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    return pays


# ---------------------- GET All Pays ----------------------
def get_pays_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pays).offset(skip).limit(limit).all()


# ---------------------- CREATE Pays ----------------------
def create_pays(db: Session, pays: schemas.PaysCreate):
    # Vérifier si le pays existe déjà
    existing_pays = db.query(models.Pays).filter(models.Pays.nom_pays == pays.nom_pays).first()
    
    if existing_pays:
        raise HTTPException(status_code=422, detail=f"Le pays '{pays.nom_pays}' existe déjà.")
    
    # Créer le pays
    db_pays = models.Pays(nom_pays=pays.nom_pays, region_oms=pays.region_oms)
    
    db.add(db_pays)
    db.commit()
    db.refresh(db_pays)
    
    return db_pays


# ---------------------- UPDATE Pays ----------------------
def update_pays(db: Session, id_pays: int, pays_update: schemas.PaysUpdate):
    pays_to_update = db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()

    if not pays_to_update:
        raise HTTPException(status_code=404, detail="Pays non trouvé")

    # Mise à jour uniquement des champs fournis
    if pays_update.nom_pays is not None:
        pays_to_update.nom_pays = pays_update.nom_pays
    if pays_update.region_oms is not None:
        pays_to_update.region_oms = pays_update.region_oms

    # Commit des changements
    db.commit()
    db.refresh(pays_to_update)
    
    return pays_to_update


# ---------------------- DELETE Pays ----------------------
def delete_pays(db: Session, id_pays: int):
    pays_to_delete = db.query(models.Pays).filter(models.Pays.id_pays == id_pays).first()

    if not pays_to_delete:
        raise HTTPException(status_code=404, detail="Pays non trouvé")

    db.delete(pays_to_delete)
    db.commit()
    
    return {"message": f"Le pays '{pays_to_delete.nom_pays}' a été supprimé avec succès."}
