from sqlalchemy.orm import Session
from app.models.utilisateur import UtilisateurSys
from ..schemas.user_schema import UserCreate

def create_user(db: Session, user_data: UserCreate) -> UtilisateurSys:
    """ Crée un nouvel utilisateur dans la base de données. """
    db_user = UtilisateurSys(
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
        nom=user_data.nom,
        prenoms=user_data.prenoms,
        adresse =user_data.adresse,
        telephone=user_data.telephone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> UtilisateurSys | None:
    """ Récupère un utilisateur par son nom d'utilisateur. """
    return db.query(UtilisateurSys).filter(UtilisateurSys.username == username).first()

def get_user_by_email(db: Session, email: str) -> UtilisateurSys | None:
    """ Récupère un utilisateur par son adresse e-mail. """
    return db.query(UtilisateurSys).filter(UtilisateurSys.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> UtilisateurSys | None:
    """ Récupère un utilisateur par son ID. """
    return db.query(UtilisateurSys).filter(UtilisateurSys.id == user_id).first()