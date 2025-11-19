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

