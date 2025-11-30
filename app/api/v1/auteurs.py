from ...core.database import get_db
from ...services import auteur_service
from ...schemas.auteur_schema import AuteurCreateSchema, AuteurSchema

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Création du routeur. Le prefixe est défini dans main.py
router = APIRouter()

# Route GET : Lecture d'un Auteur par ID
@router.get("/{auteur_id}", response_model=AuteurSchema)
def read_auteur(auteur_id: int, db: Session = Depends(get_db)):
    """ Récupère les détails d'un auteur. """
    
    # Appel du Service
    auteur = auteur_service.get_auteur(db, auteur_id)
    
    if not auteur:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auteur non trouvé")
        
    return auteur

# Route GET: Lecture de tous les auteurs
@router.get("/", response_model=list[AuteurSchema])
def read_auteurs(db:Session = Depends(get_db)):
    """Récupère tous les auteurs"""

    # Retourne la liste des auteurs (vide si aucun auteur)
    return auteur_service.get_auteurs(db)


# Route DELETE: Suppression d'un auteur
@router.delete("/{auteur_id}", response_model=AuteurSchema)
def delete_auteur(auteur_id: int, db: Session = Depends(get_db)):
    """Supprime un auteur par son ID"""
    # Appel du Service pour récupérer l'auteur
    auteur = auteur_service.get_auteur(db, auteur_id)
    
    if not auteur:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auteur non trouvé")
    
    # Appel du Repository pour supprimer l'auteur
    deleted_auteur = auteur_service.delete_auteur(db, auteur_id)
    
    return deleted_auteur


# Route POST : Création d'un Auteur
@router.post("/", response_model=AuteurSchema, status_code=status.HTTP_201_CREATED)
def create_auteur(auteur: AuteurCreateSchema, db: Session = Depends(get_db)): 
    """ Crée un nouvel auteur. """
    try:
        # Appel du Service
        new_auteur = auteur_service.create_new_auteur(db, auteur)
        return new_auteur
    except ValueError as e:
        # Gère l'erreur métier comme une requête mal formée (400)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

