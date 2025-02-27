from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class Pays(Base):
    __tablename__ = "pays"

    id_pays = Column(Integer, primary_key=True, index=True)
    nom_pays = Column(String(100), unique=True, nullable=False)
    region_oms = Column(String(50), nullable=False)

class Maladie(Base):
    __tablename__ = "maladie"

    id_maladie = Column(Integer, primary_key=True, index=True)
    nom_maladie = Column(String(50), unique=True, nullable=False)
    type_maladie = Column(String(50), nullable=False)
    description = Column(String, nullable=True)

class SituationPandemique(Base):
    __tablename__ = "situation_pandemique"

    id_pays = Column(Integer, ForeignKey("pays.id_pays"), primary_key=True)
    id_maladie = Column(Integer, ForeignKey("maladie.id_maladie"), primary_key=True)
    date_observation = Column(Date, primary_key=True)
    cas_confirmes = Column(Integer, default=0)
    deces = Column(Integer, default=0)
    guerisons = Column(Integer, default=0)
