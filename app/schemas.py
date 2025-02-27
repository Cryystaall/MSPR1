from pydantic import BaseModel

class PaysBase(BaseModel):
    nom_pays: str
    region_oms: str

# Schéma pour créer un pays
class PaysCreate(PaysBase):
    pass

# Schema for updating Pays
class PaysUpdate(PaysBase):
    # Here you can modify the attributes if needed, like making them optional
    nom_pays: str = None
    region_oms: str = None

# Schéma pour lire un pays
class Pays(PaysBase):
    id_pays: int

    class Config:
        from_attributes = True  # Convertit les objets ORM en modèles Pydantic
