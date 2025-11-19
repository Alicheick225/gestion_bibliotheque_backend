from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field

# 1. Schéma d'entrée (Création) : Ce que le client envoie
class MembreCreate(BaseModel):
    nom: str = Field(..., max_length=100)
    prenoms: str = Field(..., max_length=100)
    adresse: str = Field(default = "", max_length=100)
    email: EmailStr
    telephone: str = Field(None, max_length=20)
    type_membre_id: int = Field(..., description="ID du type d'adhérent")
    
    # Configuration Pydantic pour autoriser la validation depuis l'ORM
    class Config:
        from_attributes = True

# 2. Schéma de sortie (Lecture) : Ce que l'API retourne au client
class MembreRead(MembreCreate):
    id: int
    est_actif: bool
    date_adhesion: datetime
    type_membre_libelle: str
    

# 3. Schéma de mise à jour (Optionnel)
class MembreUpdate(BaseModel):
    adresse: str | None = None
    telephone: str | None = None
    est_actif: bool | None = None
    email: str | None = None
    nom: str | None = None
    prenoms: str | None = None
    type_membre_id: int | None = None

    # Pydantic v2 config to forbid extra fields
    model_config = {
        "extra": "forbid"
    }