from sqlalchemy.orm import Session
from ..models.document import Auteur, Editeur
from ..schemas.editeur_schema import EditeurSchema, EditeurCreateSchema as EditeurCreate


def create_editeur(db: Session, editeur: EditeurCreate) -> Auteur:
    """ Crée un nouvel éditeur dans la base de données. """
    db_editeur = Auteur(
        nom=editeur.nom,
        adresse=editeur.adresse,
        telephone=editeur.telephone,
        email=editeur.email
    )
    db.add(db_editeur)
    db.commit()
    db.refresh(db_editeur)
    return db_editeur

def get_editeur_by_id(db: Session, editeur_id: int) -> Auteur | None:
    """ Récupère un éditeur par son ID. """
    return db.query(Auteur).filter(Auteur.id == editeur_id).first()

def get_editeur_by_name(db: Session, nom: str) -> Auteur | None:
    """ Récupère un éditeur par son nom. """
    return db.query(Auteur).filter(Auteur.nom == nom).first()  


def get_all_editeurs(db: Session) -> list[Editeur]:
    """ Récupère tous les éditeurs. """
    return db.query(Editeur).all()


def delete_editeur(db: Session, editeur_id: int) -> Editeur | None:
    """ Supprime un éditeur par son ID. """
    editeur_to_delete = db.query(Auteur).filter(Auteur.id == editeur_id).first()
    if editeur_to_delete is None:
        return None
    db.delete(editeur_to_delete)
    db.commit()
    return editeur_to_delete

