from ...core.database import get_db
from ...services import editeur_service
from ...schemas.editeur_schema import EditeurCreateSchema, EditeurSchema

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Création du routeur. Le prefixe est défini dans main.py
router = APIRouter()


# Route GET : Lecture d'un Auteur par ID
@router.get("/{editeur_id}", response_model=EditeurSchema)
def read_editeur(editeur_id: int, db: Session = Depends(get_db)):
    """ Récupère les détails d'un éditeur. """
    
    # Appel du Service
    editeur = editeur_service.get_editeur(db, editeur_id)
    
    if not editeur:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Éditeur non trouvé")
        
    return editeur

# Route GET: Lecture de tous les éditeurs
@router.get("/", response_model=list[EditeurSchema])
def read_editeurs(db:Session = Depends(get_db)):
    """Récupère tous les éditeurs"""

    # Retourne la liste des éditeurs (vide si aucun éditeur)
    return editeur_service.get_editeurs(db)

# Route DELETE: Suppression d'un éditeur
@router.delete("/{editeur_id}", response_model=EditeurSchema)
def delete_editeur(editeur_id: int, db: Session = Depends(get_db)):   
    """Supprime un éditeur par son ID"""
    # Appel du Service pour récupérer l'éditeur
    editeur = editeur_service.get_editeur(db, editeur_id)
    
    if not editeur:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Éditeur non trouvé")
    
    # Appel du Repository pour supprimer l'éditeur
    deleted_editeur = editeur_service.delete_editeur(db, editeur_id)
    
    return deleted_editeur

# Route POST : Création d'un Éditeur
@router.post("/", response_model=EditeurSchema, status_code=status.HTTP_201_CREATED)
def create_editeur(editeur: EditeurCreateSchema, db: Session = Depends(get_db)):           
    """ Crée un nouvel éditeur. """
    try:
        # Appel du Service
        new_editeur = editeur_service.create_new_editeur(db, editeur)
        return new_editeur
    except ValueError as e:
        # Gère les erreurs de validation ou autres
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))