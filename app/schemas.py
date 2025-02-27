from pydantic import BaseModel

# Schéma pour pays

# Schéma pour lire un pays
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





# Schéma pour maladies

class MaladieBase(BaseModel):
    nom_maladie: str
    type_maladie: str
    description: str


# Schéma pour créer une maladie
class MaladieCreate(MaladieBase):
    pass

# Schéma pour mettre à jour une maladie
class MaladieUpdate(MaladieBase):
    # Here you can modify the attributes if needed, like making them optional
    nom_maladie: str = None
    type_maladie: str = None
    description: str = None

# Schéma pour lire une maladie
class Maladie(MaladieBase):
    id_maladie: int

    class Config:
        from_attributes = True  # Convertit les objets ORM en modèles Pydantic