from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.token_schema import Token
from app.core.security import get_current_active_user
from app.schemas.user_schema import UserCreate, UserRead
from app.services import user_service
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import oauth2_scheme # Dépendance pour la récupération des données de connexion
from app.services.user_service import authenticate_user
from datetime import timedelta
from app.core import config
from app.core.security import create_access_token

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

# API pour récupérer les informations de l'utilisateur actuellement authentifié
@router.get("/me")
def read_current_user(current_user = Depends(get_current_active_user)):
    """Récupère les informations de l'utilisateur actuellement authentifié."""
    return current_user


# API pour créer un nouvel utilisateur
@router.post("/register", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """ Crée un nouvel utilisateur. """
    try:
        # Appel du Service
        new_user = user_service.create_new_user(db, user)
        return new_user
    except ValueError as e:
        # Gère l'erreur métier (email déjà utilisé) comme une requête mal formée (400)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

# Authentification et Accès

# API pour s'authentifier et obtenir un token JWT
@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Récupère username et password
    db: Session = Depends(get_db)
):
    # 1. AUTHENTIFICATION : Vérification de l'utilisateur et du mot de passe
    user = authenticate_user(db, form_data.username, form_data.password)
    
    # 💥 Échec de l'authentification
    if not user:
        # Style recommandé de FastAPI (avec arguments nommés)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. VÉRIFICATION D'ÉTAT (Ex: utilisateur doit être actif)
    if not user.est_actif:
        # Style recommandé de FastAPI (avec arguments nommés)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Le compte utilisateur est inactif"
        )

    # 3. GÉNÉRATION DU TOKEN : Création du JWT
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    # 4. RÉPONSE
    return {"access_token": access_token, "token_type": "bearer"}

# Déconnexion de l'utilisateur
@router.post("/auth/logout", status_code=204)
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Point de terminaison pour la déconnexion de l'utilisateur.
    Note : Avec les JWT, la déconnexion côté serveur est complexe car les tokens sont stateless.
    Cette implémentation est un simple placeholder.
    """
    # Ici, on pourrait implémenter une liste de tokens révoqués ou une autre stratégie.
    return


# Rafraîchissement du token d'accès
@router.post("/auth/refresh", response_model=Token)
async def refresh_access_token(
    current_user = Depends(get_current_active_user)
):
    """
    Point de terminaison pour rafraîchir le token d'accès.
    Génère un nouveau token pour l'utilisateur actuellement authentifié.
    """
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    new_access_token = create_access_token(
        data={"sub": current_user.username, "user_id": current_user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": new_access_token, "token_type": "bearer"}


# Réinitialisation du mot de passe
@router.post("/auth/reset-password", status_code=204)
async def reset_password(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Point de terminaison pour réinitialiser le mot de passe d'un utilisateur.
    Envoie un e-mail de réinitialisation (simulation).
    """
    user = user_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur avec cet e-mail non trouvé."
        )
    
    # Ici, on simulerait l'envoi d'un e-mail de réinitialisation
    print(f"Envoi d'un e-mail de réinitialisation à {email} (simulation).")
    
    return

# Envoyer un e-mail de réinitialisation de mot de passe
@router.post("/auth/forgot-password", status_code=204)
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Point de terminaison pour demander une réinitialisation de mot de passe.
    Envoie un e-mail avec un lien de réinitialisation (simulation).
    """
    user = user_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur avec cet e-mail non trouvé."
        )
    
    # Ici, on simulerait l'envoi d'un e-mail avec un lien de réinitialisation
    print(f"Envoi d'un e-mail avec un lien de réinitialisation à {email} (simulation).")
    
    return