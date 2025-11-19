# Afficher tous les documents

from app.core.database import get_db
from app.services import document_service
from app.core.security import get_current_active_user

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentCreate, DocumentRead, DocumentUpdate


router = APIRouter()

@router.get("/", response_model=list[DocumentRead])
def read_documents(db: Session = Depends(get_db)):
    """Récupère tous les documents"""

    # Retourne la liste des documents (vide si aucun document)
    return document_service.get_documents(db)

@router.get("/{document_id}", response_model=DocumentRead)
def read_document(document_id: int, db: Session = Depends(get_db)):
    """ Récupère les détails d'un document. """
    
    # Appel du Service
    document = document_service.get_document(db, document_id)
    
    if document is None:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")
        
    return document

@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    """ Crée un nouveau document. """
    try:
        # Appel du Service
        new_document = document_service.create_new_document(db, document, current_user.id)
        return new_document
    except ValueError as e:
        # Gère l'erreur métier comme une requête mal formée (400)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{document_id}", response_model=DocumentRead)
def delete_document(document_id: int, db: Session = Depends(get_db)):   
    """Supprime un document par son ID"""
    # Appel du Service pour récupérer le document
    document = document_service.delete_document(db, document_id)

    if document is None:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")

    return document


@router.patch("/{document_id}", response_model=DocumentRead)
def patch_document(document_id: int, updates: DocumentUpdate, db: Session = Depends(get_db)):
    """Met à jour partiellement un document"""
    try:
        updated_document = document_service.update_document(db, document_id, updates)
        if updated_document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")
        return updated_document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))