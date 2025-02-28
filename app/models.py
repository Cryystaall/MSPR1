from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from .database import Base

class Pays(Base):
    __tablename__ = "pays"

    id_pays = Column(Integer, primary_key=True, index=True)
    nom_pays = Column(String(100), unique=True, nullable=False)
    region_oms = Column(String(50), nullable=False)

    # Relationship: One country has many pandemic situations
    situations = relationship("SituationPandemique", back_populates="pays")

class Maladie(Base):
    __tablename__ = "maladie"

    id_maladie = Column(Integer, primary_key=True, index=True)
    nom_maladie = Column(String(50), unique=True, nullable=False)
    type_maladie = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)  # Use Text for longer descriptions

    # Relationship: One disease has many pandemic situations
    situations = relationship("SituationPandemique", back_populates="maladie")

class SituationPandemique(Base):
    __tablename__ = "situation_pandemique"

    id_pays = Column(Integer, ForeignKey("pays.id_pays", ondelete="CASCADE"), primary_key=True, index=True)
    id_maladie = Column(Integer, ForeignKey("maladie.id_maladie", ondelete="CASCADE"), primary_key=True, index=True)
    date_observation = Column(Date, primary_key=True, index=True)

    cas_confirmes = Column(Integer, default=0, nullable=False)
    deces = Column(Integer, default=0, nullable=False)
    guerisons = Column(Integer, default=0, nullable=False)
    cas_actifs = Column(Integer, default=0, nullable=False)
    nouveaux_cas = Column(Integer, default=0, nullable=False)
    nouveaux_deces = Column(Integer, default=0, nullable=False)
    nouvelles_guerisons = Column(Integer, default=0, nullable=False)

    # Relationships
    pays = relationship("Pays", back_populates="situations")
    maladie = relationship("Maladie", back_populates="situations")
