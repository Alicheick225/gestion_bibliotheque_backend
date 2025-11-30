from sqlalchemy.orm import Session
from ..repositories import auteur_repo
from ..schemas.auteur_schema import AuteurSchema

def get_auteur(db: Session, auteur_id: int) -> AuteurSchema | None:
    """ Logique métier pour récupérer et traiter les informations d'un auteur. """
    db_auteur = auteur_repo.get_auteur_by_id(db, auteur_id)

    if db_auteur is None:
        return None

    return AuteurSchema.model_validate(db_auteur)


def get_auteurs(db: Session) -> list[AuteurSchema]:
    """ Logique métier pour récupérer et traiter les informations d'un auteur. """
    db_auteurs = auteur_repo.get_all_auteurs(db)
    return [AuteurSchema.model_validate(auteur) for auteur in db_auteurs]


def delete_auteur(db: Session, auteur_id: int) -> AuteurSchema | None:
    """ Logique métier pour supprimer un auteur. """
    # Appel du Repository pour supprimer l'auteur
    deleted_auteur = auteur_repo.delete_auteur(db, auteur_id)

    if deleted_auteur is None:
        return None

    return AuteurSchema.model_validate(deleted_auteur)

def create_new_auteur(db: Session, auteur_data) -> AuteurSchema:
    """ Logique métier pour créer un nouvel auteur. """
    # 1. Validation métier (ex: vérifier l'unicité du nom)
    existing_auteur = auteur_repo.get_auteur_by_name(db, auteur_data.nom)
    if existing_auteur:
        raise ValueError("Un auteur avec ce nom existe déjà.")

    # 2. Appel du Repository pour l'insertion DB
    db_auteur = auteur_repo.create_auteur(db, auteur_data)

    # 3. Conversion de l'objet DB en Schéma de Sortie (sérialisation)
    return AuteurSchema.model_validate(db_auteur)