from sqlalchemy.orm import Session
from ..repositories import document_repo
from ..schemas.document_schema import DocumentCreate, DocumentRead

def get_documents(db: Session) -> list[DocumentRead]:
    """ Logique métier pour récupérer et traiter les informations d'un document. """
    db_documents = document_repo.get_all_documents(db)
    return [DocumentRead.model_validate(doc) for doc in db_documents]


def get_document(db: Session, document_id: int) -> DocumentRead | None:
    """ Logique métier pour récupérer et traiter les informations d'un document. """
    db_document = document_repo.get_document_by_id(db, document_id)

    if db_document is None:
        return None

    return DocumentRead.model_validate(db_document)


def create_new_document(db: Session, document_data: DocumentCreate, utilisateur_creation_id: int) -> DocumentRead:
    """ Logique métier pour créer un nouveau document. """
    # 1. Validation métier (ex: vérifier l'unicité du titre)
    # schema uses `titre`
    existing_doc = document_repo.get_document_by_title(db, document_data.titre)
    if existing_doc:
        raise ValueError("Un document avec ce titre existe déjà.")

    # 2. Appel du Repository pour l'insertion DB
    db_document = document_repo.create_document(db, document_data, utilisateur_creation_id)

    # 3. Conversion de l'objet DB en Schéma de Sortie (sérialisation)
    return DocumentRead.model_validate(db_document)


def delete_document(db: Session, document_id: int) -> DocumentRead | None:
    """ Logique métier pour supprimer un document. """
    # Appel du Repository pour supprimer le document
    deleted_document = document_repo.delete_document(db, document_id)

    if deleted_document is None:
        return None

    return DocumentRead.model_validate(deleted_document)


def update_document(db: Session, document_id: int, update_data) -> DocumentRead | None:
    """ Logique métier pour mettre à jour un document. """
    updated_document = document_repo.update_document(db, document_id, update_data)

    if updated_document is None:
        return None

    return DocumentRead.model_validate(updated_document)