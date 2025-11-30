from sqlalchemy.orm import Session
from ..repositories import categorie_repo
from ..schemas.categorie_schema import CategorieSchema

def get_categorie(db: Session, categorie_id: int) -> CategorieSchema | None:
    """ Logique métier pour récupérer et traiter les informations d'une catégorie. """
    db_categorie = categorie_repo.get_categorie_by_id(db, categorie_id)

    if db_categorie is None:
        return None

    return CategorieSchema.model_validate(db_categorie)


def get_categories(db: Session) -> list[CategorieSchema]:
    """ Logique métier pour récupérer et traiter les informations d'une catégorie. """
    db_categories = categorie_repo.get_all_categories(db)
    return [CategorieSchema.model_validate(categorie) for categorie in db_categories]


def delete_categorie(db: Session, categorie_id: int) -> CategorieSchema | None:
    """ Logique métier pour supprimer une catégorie. """
    # Appel du Repository pour supprimer la catégorie
    deleted_categorie = categorie_repo.delete_categorie(db, categorie_id)

    if deleted_categorie is None:
        return None

    return CategorieSchema.model_validate(deleted_categorie)


def create_new_categorie(db: Session, categorie_data) -> CategorieSchema:
    """ Logique métier pour créer une nouvelle catégorie. """
    # 1. Validation métier (ex: vérifier l'unicité du nom)
    existing_categorie = categorie_repo.get_categorie_by_name(db, categorie_data.nom)
    if existing_categorie:
        raise ValueError("Une catégorie avec ce nom existe déjà.")

    # 2. Appel du Repository pour l'insertion DB
    db_categorie = categorie_repo.create_categorie(db, categorie_data)

    # 3. Conversion de l'objet DB en Schéma de Sortie (sérialisation)
    return CategorieSchema.model_validate(db_categorie)