# Afficher tous les documents

from app.core.database import get_db
from app.services import document_service
from app.core.security import get_current_active_user

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentCreate, DocumentRead, DocumentUpdate
from typing import List, Any


router = APIRouter()

# --- 1. GET / : Récupère tous les documents (PROTÉGÉ) ---
@router.get("/", response_model=List[DocumentRead], summary="Récupère tous les documents (Protégé)")
def read_documents(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),  # ⬅️ Correction: Syntaxe standard
):
    """Récupère tous les documents (accessible uniquement aux utilisateurs connectés)"""

    return document_service.get_documents(db)


# --- 2. GET /{document_id} : Récupère les détails d'un document (PROTÉGÉ) ---
@router.get("/{document_id}", response_model=DocumentRead, summary="Récupère les détails d'un document (Protégé)")
def read_document(
    document_id: int, 
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),  # ⬅️ Correction: Syntaxe standard
):
    """ Récupère les détails d'un document. """
    
    document = document_service.get_document(db, document_id)
    
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")
        
    return document


# --- 3. POST / : Crée un nouveau document (CORRIGÉ) ---
@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED, summary="Crée un nouveau document (Protégé)")
def create_document(
    document: DocumentCreate, 
    db: Session = Depends(get_db), 
    current_user: Any = Depends(get_current_active_user),  # ⬅️ Correction: Syntaxe standard
):
    """ Crée un nouveau document. """
    try:
        # L'ID de l'utilisateur est utilisé pour lier l'auteur du document
        new_document = document_service.create_new_document(db, document, current_user.id)
        return new_document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
# --- 4. DELETE /{document_id} : Supprime un document (PROTÉGÉ) ---
@router.delete("/{document_id}", response_model=DocumentRead, summary="Supprime un document (Protégé)")
def delete_document(
    document_id: int, 
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),  # ⬅️ Correction: Syntaxe standard
):   
    """
    Supprime un document par son ID. 
    (Idéalement, le service vérifie que current_user a les droits de suppression.)
    """
    
    # Passer l'utilisateur au service pour la vérification des droits
    document = document_service.delete_document(db, document_id, current_user) 

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")

    return document


# --- 5. PATCH /{document_id} : Met à jour partiellement un document (PROTÉGÉ) ---
@router.patch("/{document_id}", response_model=DocumentRead, summary="Met à jour partiellement un document (Protégé)")
def patch_document(
    document_id: int, 
    updates: DocumentUpdate, 
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user), # ⬅️ Correction: Syntaxe standard
):
    """
    Met à jour partiellement un document. 
    (Idéalement, le service vérifie que current_user a les droits de modification.)
    """
    try:
        # Passer l'utilisateur au service pour vérifier les permissions
        updated_document = document_service.update_document(db, document_id, updates, current_user)
        
        if updated_document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé")
        
        return updated_document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))