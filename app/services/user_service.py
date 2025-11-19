# Fichier: app/services/user_service.py (Extrait)

from app.core.security import get_password_hash, verify_password
from app.repositories import user_repo # A créer
from app.schemas.user_schema import UserCreate, UserRead
from sqlalchemy.orm import Session

def create_new_user(db: Session, user_data: UserCreate) -> UserRead:
    # 1. Vérification métier (email unique, etc.)

    # 2. Hachage du mot de passe AVANT de l'envoyer au Repository
    hashed_password = get_password_hash(user_data.password)
    
    # Créer un dictionnaire pour le Repo, en remplaçant le mot de passe par la version hachée
    user_db_data = user_data.model_dump(exclude={"password"})
    user_db_data["password"] = hashed_password 
    
    db_user = user_repo.create_user(db, user_db_data)
    
    return UserRead.model_validate(db_user)


def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)
    if not user:
        return None
        
    # Vérification du mot de passe haché
    if not verify_password(password, user.password):
        return None
        
    return user