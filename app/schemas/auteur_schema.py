from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from sqlalchemy import Date


# Schéma pour la création d'un auteur
class AuteurCreateSchema(BaseModel):
    nom: str = Field(..., max_length=100, description="Nom de l'auteur")
    prenoms: str = Field(..., max_length=100, description="Prénoms de l'auteur")
    nationalite: Optional[str] = Field(None, max_length=100, description="Nationalité de l'auteur")
    date_naissance: Optional[Date] = Field(None, description="Date de naissance de l'auteur")
    date_deces: Optional[Date] = Field(None, description="Date de décès de l'auteur")

    
    # Pydantic V2 Configuration: Le correctif essentiel
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True 
    )


# Schéma pour la lecture d'un auteur
class AuteurSchema(AuteurCreateSchema):
    id: int

    class Config:
        from_attributes = True


# Schéma pour la mise à jour d'un auteur
class AuteurUpdateSchema(BaseModel):
    nom: Optional[str] = None
    prenoms: Optional[str] = None
    date_deces : Optional[Date] = None
    date_naissance: Optional[Date] = None

    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True
    )