from pydantic import BaseModel
from typing import Optional

# ---------------------- Schémas pour Pays ----------------------

class PaysBase(BaseModel):
    nom_pays: str
    region_oms: str


class PaysCreate(PaysBase):
    pass


class PaysUpdate(BaseModel):
    nom_pays: Optional[str] = None
    region_oms: Optional[str] = None


class Pays(PaysBase):
    id_pays: int

    class Config:
        from_attributes = True  # Convertit les objets ORM en modèles Pydantic





# ---------------------- Schémas pour Maladies ----------------------

class MaladieBase(BaseModel):
    nom_maladie: str
    type_maladie: str
    description: str


class MaladieCreate(MaladieBase):
    pass


class MaladieUpdate(BaseModel):
    nom_maladie: Optional[str] = None
    type_maladie: Optional[str] = None
    description: Optional[str] = None


class Maladie(MaladieBase):
    id_maladie: int

    class Config:
        from_attributes = True  # Convertit les objets ORM en modèles Pydantic





# ---------------------- Schémas pour Situation Pandémique ----------------------

class SituationPandemiqueBase(BaseModel):
    id_pays: int
    id_maladie: int
    date_observation: str
    cas_confirmes: int
    deces: int
    guerisons: int


class SituationPandemiqueCreate(SituationPandemiqueBase):
    pass


class SituationPandemiqueUpdate(BaseModel):
    id_pays: Optional[int] = None
    id_maladie: Optional[int] = None
    date_observation: Optional[str] = None
    cas_confirmes: Optional[int] = None
    deces: Optional[int] = None
    guerisons: Optional[int] = None


class SituationPandemique(SituationPandemiqueBase):
    maladie: Maladie
    pays: Pays

    class Config:
        from_attributes = True  # Convertit les objets ORM en modèles Pydantic
