from ...core.database import get_db
from ...services import categorie_service
from ...schemas.categorie_schema import CategorieCreateSchema, CategorieSchema

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


# Création du routeur. Le prefixe est défini dans main.py
router = APIRouter()


# Route GET : Lecture d'une Catégorie par ID
@router.get("/{categorie_id}", response_model=CategorieSchema)
def read_categorie(categorie_id: int, db: Session = Depends(get_db)):
    """ Récupère les détails d'une catégorie. """
    
    # Appel du Service
    categorie = categorie_service.get_categorie(db, categorie_id)
    
    if not categorie:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie non trouvée")
        
    return categorie


# Route GET: Lecture de toutes les catégories
@router.get("/", response_model=list[CategorieSchema])
def read_categories(db:Session = Depends(get_db)):
    """Récupère toutes les catégories"""

    # Retourne la liste des catégories (vide si aucune catégorie)
    return categorie_service.get_categories(db)


# Route DELETE: Suppression d'une catégorie
@router.delete("/{categorie_id}", response_model=CategorieSchema)
def delete_categorie(categorie_id: int, db: Session = Depends(get_db)):   
    """Supprime une catégorie par son ID"""
    # Appel du Service pour récupérer la catégorie
    categorie = categorie_service.get_categorie(db, categorie_id)
    
    if not categorie:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie non trouvée")
    
    # Appel du Repository pour supprimer la catégorie
    deleted_categorie = categorie_service.delete_categorie(db, categorie_id)
    
    return deleted_categorie


# Route POST : Création d'une Catégorie
@router.post("/", response_model=CategorieSchema, status_code=status.HTTP_201_CREATED)
def create_categorie(categorie: CategorieCreateSchema, db: Session = Depends(get_db)):           
    """ Crée une nouvelle catégorie. """
    try:
        # Appel du Service
        new_categorie = categorie_service.create_new_categorie(db, categorie)
        return new_categorie
    except ValueError as e:
        # Gère les erreurs de validation ou autres
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))