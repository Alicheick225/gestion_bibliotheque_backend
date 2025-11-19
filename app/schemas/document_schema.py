from pydantic import BaseModel
from typing import Optional
from datetime import date

# Schéma de base pour Document
class DocumentBase(BaseModel):
    titre: str
    editeur_id: int
    annee_publication: Optional[int] = None
    categorie_id: int
    # allow multiple authors when creating a document
    auteur_ids: Optional[list[int]] = None
    # resume/description text
    resume: Optional[str] = None

# Schéma pour la création d'un document
class DocumentCreate(DocumentBase):
    # correspond au modèle Document : on laisse les mêmes champs que DocumentBase
    # et on autorise explicitement le champ `disponible` (par défaut True)
    disponible: Optional[bool] = True

    class Config:
        from_attributes = True

# Schéma pour la lecture d'un document
class DocumentRead(DocumentBase):
    id: int
    disponible: bool = True

    class Config:
        from_attributes = True

# Schéma pour la modification d'un document
class DocumentUpdate(BaseModel):
    titre: Optional[str] = None
    auteur: Optional[str] = None
    editeur: Optional[str] = None
    date_publication: Optional[date] = None
    categorie: Optional[str] = None
    description: Optional[str] = None
    disponible: Optional[bool] = None