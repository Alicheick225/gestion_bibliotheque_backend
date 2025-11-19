from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.repositories import auteur_repo
from app.models.document import Document, DocumentAuteur
from app.schemas.document_schema import DocumentCreate, DocumentUpdate


def get_document_by_id(db: Session, document_id: int) -> Document | None:
    """ Récupère un document par son ID. """
    return db.query(Document).filter(Document.id == document_id).first()

def get_all_documents(db: Session) -> list[Document]:
    """ Récupère tous les documents. """
    return db.query(Document).all()


def get_document_by_title(db: Session, title: str) -> Document | None:
    """ Récupère un document par son titre. """
    # le modèle utilise `titre` (fr) plutôt que `title`
    return db.query(Document).filter(Document.titre == title).first()

def create_document(db: Session, document_data: DocumentCreate, utilisateur_creation_id: int) -> Document:
    """ Crée un nouveau document et associe un ou plusieurs auteurs.

    - `auteur_ids` dans `document_data` peut être None ou une liste d'entiers.
    - `utilisateur_creation_id` doit provenir du contexte d'authentification (fourni par l'appelant).
    """
    # Valider que tous les auteurs existent
    auteur_ids: List[int] = document_data.auteur_ids or []
    for aid in auteur_ids:
        if not auteur_repo.get_auteur_by_id(db, aid):
            raise ValueError(f"Auteur non trouvé avec l'ID {aid}.")

    db_document = Document(
        titre=document_data.titre,
        editeur_id=document_data.editeur_id,
        categorie_id=document_data.categorie_id,
        utilisateur_creation_id=utilisateur_creation_id,
        annee_publication=document_data.annee_publication,
        resume=document_data.resume,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Créer les lignes d'association document_auteur si des auteurs sont fournis
    for aid in auteur_ids:
        new_assoc = DocumentAuteur(document_id=db_document.id, auteur_id=aid, date_creation=datetime.now())
        db.add(new_assoc)
    if auteur_ids:
        db.commit()

    return db_document

def delete_document(db: Session, document_id: int) -> Document | None:
    """ Supprime un document par son ID et retourne l'objet supprimé. """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        db.delete(document)
        db.commit()
    return document

def update_document(db: Session, document_id: int, update_data: DocumentUpdate) -> Document | None:
    """ Met à jour les informations d'un document et retourne l'objet mis à jour. """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)
    return document


def associate_auteur_to_document(db: Session, document_id: int, auteur_id: int):
    """Associe un auteur à un document dans la table d'association document_auteur"""

    new_document_auteur = DocumentAuteur(document_id=document_id, auteur_id=auteur_id)
    db.add(new_document_auteur)
    db.commit()