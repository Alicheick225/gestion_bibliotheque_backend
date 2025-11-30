from sqlalchemy.orm import Session
from ..models.document import Categorie
from ..schemas.categorie_schema import CategorieSchema, CategorieCreateSchema as CategorieCreate

def create_categorie(db: Session, categorie: CategorieCreate) -> Categorie:
    """ Crée une nouvelle catégorie dans la base de données. """
    db_categorie = Categorie(
        nom=categorie.nom,
        description=categorie.description
    )
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie

def get_categorie_by_id(db: Session, categorie_id: int) -> Categorie | None:
    """ Récupère une catégorie par son ID. """
    return db.query(Categorie).filter(Categorie.id == categorie_id).first()

def get_categorie_by_name(db: Session, nom: str) -> Categorie | None:
    """ Récupère une catégorie par son nom. """
    return db.query(Categorie).filter(Categorie.nom == nom).first()

def get_all_categories(db: Session) -> list[Categorie]:
    """ Récupère toutes les catégories. """
    return db.query(Categorie).all()

def delete_categorie(db: Session, categorie_id: int) -> Categorie | None:
    """ Supprime une catégorie par son ID. """
    categorie_to_delete = db.query(Categorie).filter(Categorie.id == categorie_id).first()
    if categorie_to_delete is None:
        return None
    db.delete(categorie_to_delete)
    db.commit()
    return categorie_to_delete

