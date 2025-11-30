from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from sqlalchemy import Date


# Schéma pour la création d'un éditeur
class EditeurCreateSchema(BaseModel):
    nom: str = Field(..., max_length=100, description="Nom de l'éditeur")
    adresse: Optional[str] = Field(None, max_length=200, description="Adresse de l'éditeur")
    telephone: Optional[str] = Field(None, max_length=20, description="Numéro de téléphone de l'éditeur")
    email: Optional[str] = Field(None, max_length=100, description="Email de l'éditeur")

    
    # Pydantic V2 Configuration: Le correctif essentiel
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True 
    )

# Schéma pour la lecture d'un éditeur
class EditeurSchema(EditeurCreateSchema):
    id: int

    class Config:
        from_attributes = True  

# Schéma pour la mise à jour d'un éditeur
class EditeurUpdateSchema(BaseModel):
    nom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True
    )

