from sqlalchemy.orm import Session
from ..models.document import Auteur
from ..schemas.auteur_schema import AuteurCreateSchema as AuteurCreate


def create_auteur(db: Session, auteur: AuteurCreate) -> Auteur:
    """ Crée un nouvel auteur dans la base de données. """
    db_auteur = Auteur(
        nom=auteur.nom,
        prenoms=auteur.prenoms,
        nationalite=auteur.nationalite,
        date_naissance=auteur.date_naissance,
        date_deces=auteur.date_deces
    )
    db.add(db_auteur)
    db.commit()
    db.refresh(db_auteur)
    return db_auteur

def get_auteur_by_id(db: Session, auteur_id: int) -> Auteur | None:
    """ Récupère un auteur par son ID. """
    return db.query(Auteur).filter(Auteur.id == auteur_id).first()

def get_auteur_by_name(db: Session, nom: str) -> Auteur | None:
    """ Récupère un auteur par son nom. """
    return db.query(Auteur).filter(Auteur.nom == nom).first()

def get_all_auteurs(db: Session) -> list[Auteur]:
    """ Récupère tous les auteurs. """
    return db.query(Auteur).all()


def delete_auteur(db: Session, auteur_id: int) -> Auteur | None:
    """ Supprime un auteur par son ID. """
    auteur_to_delete = db.query(Auteur).filter(Auteur.id == auteur_id).first()
    if auteur_to_delete is None:
        return None
    db.delete(auteur_to_delete)
    db.commit()
    return auteur_to_delete