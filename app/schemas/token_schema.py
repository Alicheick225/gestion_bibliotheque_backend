from pydantic import BaseModel
from typing import Optional

# Schéma d'entrée pour la connexion
class TokenRequest(BaseModel):
    # Nous utiliserons le 'username' pour l'identification
    username: str
    password: str

# Schéma de sortie pour le token (standard JWT)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
# Schéma pour le JWT décodé (utilisé en interne par le système)
class TokenData(BaseModel):
    username: Optional[str] = None

