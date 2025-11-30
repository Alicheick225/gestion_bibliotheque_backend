from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from sqlalchemy import Date


# Schéma pour la création d'une catégorie
class CategorieCreateSchema(BaseModel):
    libelle: str = Field(..., max_length=100, description="Nom de la catégorie")
    description: Optional[str] = Field(None, max_length=200, description="Description de la catégorie")

    
    # Pydantic V2 Configuration: Le correctif essentiel
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True 
    ) 


# Schéma pour la lecture d'une catégorie
class CategorieSchema(CategorieCreateSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

# Schéma pour la mise à jour d'une catégorie
class CategorieUpdateSchema(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True
    )