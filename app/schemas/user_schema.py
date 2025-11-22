from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    nom: str
    prenoms : str
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    
    class Config:
        # Permet de convertir les données Pydantic en format ORM (dictionnaire) si nécessaire
        from_attributes = True


class UserRead(UserCreate):
    id: int

    class Config:
        from_attributes = True    