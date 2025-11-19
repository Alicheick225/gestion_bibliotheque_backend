from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Any
from passlib.context import CryptContext
from app.repositories import user_repo  # adapte le chemin / fonction
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt # Bibliothèque pour JWT
from app.core import config # Pour accéder à la clé secrète
from app.schemas.token_schema import TokenData


from app.core.database import get_db # Fonction existante pour obtenir la session DB
from app.repositories import user_repo # Repository à créer
from app.models.utilisateur import UtilisateurSys # Modèle DB


from fastapi.security import OAuth2PasswordRequestForm

# Définit le contexte de hachage (utiliser bcrypt car il est lent et sécurisé)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe simple correspond au mot de passe haché."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hache et sale le mot de passe."""
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordRequestForm


# ----------------------------------------------------------------------
# 2. Fonction de Création du Token
# ----------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un JSON Web Token (JWT) pour l'authentification.

    Args:
        data (dict): Les 'claims' à inclure dans le token (ex: {'sub': username, 'user_id': id}).
        expires_delta (timedelta, optional): Durée de validité du token. Par défaut, 15 minutes.

    Returns:
        str: Le token JWT encodé.
    """
    # Copie des données pour l'ajout des claims spécifiques au token
    to_encode = data.copy()

    # Définition de l'expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Valeur par défaut si non spécifiée (souvent 15 minutes)
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) 
    
    # Ajout du claim 'exp' (expiration) et 'iat' (issued at)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    # Encodage du token en utilisant la clé secrète et l'algorithme
    encoded_jwt = jwt.encode(
        to_encode, 
        config.settings.SECRET_KEY, 
        algorithm=config.settings.ALGORITHM # Ex: "HS256"
    )
    
    return encoded_jwt



def decode_access_token(token: str) -> TokenData:
    """
    Décode un token JWT et renvoie les données qu'il contient.
    Lève une HTTPException si le token est invalide ou expiré.
    """
    try:
        # 1. Décodage du token en utilisant la clé secrète
        payload = jwt.decode(
            token, 
            config.settings.SECRET_KEY, 
            algorithms=[config.settings.ALGORITHM]
        )
        
        # 2. Extraction des données (claims)
        username: str = payload.get("sub") # 'sub' contient le username
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide : Données utilisateur manquantes.",
            )
        
        # 3. Renvoie les données décodées
        return TokenData(username=username, user_id=user_id)

    except JWTError:
        # Gère les erreurs de signature, d'expiration, ou de format
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 1. Définit le schéma OAuth2 et le point de terminaison de token (pour la documentation)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/users")

async def get_current_active_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme) # ⬅️ Récupère le token de l'en-tête
) -> UtilisateurSys:
    
    # 2. Décodage du token pour obtenir les claims
    token_data = decode_access_token(token)
    
    # 3. Récupération de l'utilisateur par son ID
    user = user_repo.get_user_by_id(db, user_id=token_data.user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable.",
        )
    
    # 4. Vérification si l'utilisateur est actif
    if not user.est_actif:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Le compte utilisateur est inactif"
        )
        
    return user