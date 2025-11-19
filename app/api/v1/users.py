from http.client import HTTPException
from fastapi import APIRouter, Depends
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

router = APIRouter()

@router.get("/users/me")
def read_current_user(current_user = Depends(get_current_active_user)):
    """Récupère les informations de l'utilisateur actuellement authentifié."""
    return current_user


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
    


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: oauth2_scheme = Depends(), # Récupère username et password
    db: Session = Depends(get_db)
):
    # 1. AUTHENTIFICATION : Vérification de l'utilisateur et du mot de passe
    user = authenticate_user(db, form_data.username, form_data.password)
    
    # 💥 Échec de l'authentification
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. VÉRIFICATION D'ÉTAT (Ex: utilisateur doit être actif)
    if not user.est_actif:
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