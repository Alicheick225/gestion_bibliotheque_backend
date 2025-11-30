from sqlalchemy.orm import Session
from ..repositories import editeur_repo
from ..schemas.editeur_schema import EditeurSchema

def get_editeur(db: Session, editeur_id: int) -> EditeurSchema | None:
    """ Logique métier pour récupérer et traiter les informations d'un éditeur. """
    db_editeur = editeur_repo.get_editeur_by_id(db, editeur_id)

    if db_editeur is None:
        return None

    return EditeurSchema.model_validate(db_editeur)

def get_editeurs(db: Session) -> list[EditeurSchema]:
    """ Logique métier pour récupérer et traiter les informations d'un éditeur. """
    db_editeurs = editeur_repo.get_all_editeurs(db)
    return [EditeurSchema.model_validate(editeur) for editeur in db_editeurs]


def delete_editeur(db: Session, editeur_id: int) -> EditeurSchema | None:
    """ Logique métier pour supprimer un éditeur. """
    # Appel du Repository pour supprimer l'éditeur
    deleted_editeur = editeur_repo.delete_editeur(db, editeur_id)

    if deleted_editeur is None:
        return None

    return EditeurSchema.model_validate(deleted_editeur)

def create_new_editeur(db: Session, editeur_data) -> EditeurSchema:
    """ Logique métier pour créer un nouvel éditeur. """
    # 1. Validation métier (ex: vérifier l'unicité du nom)
    existing_editeur = editeur_repo.get_editeur_by_name(db, editeur_data.nom)
    if existing_editeur:
        raise ValueError("Un éditeur avec ce nom existe déjà.")

    # 2. Appel du Repository pour l'insertion DB
    db_editeur = editeur_repo.create_editeur(db, editeur_data)

    # 3. Conversion de l'objet DB en Schéma de Sortie (sérialisation)
    return EditeurSchema.model_validate(db_editeur)