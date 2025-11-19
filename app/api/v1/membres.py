from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...models.utilisateur import UtilisateurSys # Le type Session est utilisé pour la dépendance
from ...schemas.membre_schema import MembreCreate, MembreRead, MembreUpdate
from ...services import membre_service
from ...core.database import get_db # Importe la dépendance de session DB
from ...core.security import get_current_active_user 

# Création du routeur. Le prefixe est défini dans main.py
router = APIRouter()


# Route POST : Création d'un Membre
@router.post("/", response_model=MembreRead, status_code=status.HTTP_201_CREATED)
def create_member(membre: MembreCreate, db: Session = Depends(get_db), current_user: UtilisateurSys = Depends(get_current_active_user)):
    """ Crée un nouvel adhérent. """
    try:
        # Appel du Service
        new_member = membre_service.create_new_membre(db, membre, current_user.id)
        return new_member
    except ValueError as e:
        # Gère l'erreur métier (email déjà utilisé) comme une requête mal formée (400)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Route GET : Lecture d'un Membre par ID
@router.get("/{membre_id}", response_model=MembreRead)
def read_member(membre_id: int, db: Session = Depends(get_db)):
    """ Récupère les détails d'un adhérent. """
    
    # Appel du Service
    member = membre_service.get_membre(db, membre_id)
    
    if not member:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membre non trouvé")
        
    return member

# Route GET: Lecture de tous les membres

@router.get("/", response_model=list[MembreRead])
def read_members(db:Session = Depends(get_db)):
    """Récupère tous les adhérents"""

    # Retourne la liste des membres (vide si aucun membre)
    return membre_service.get_members(db)


# Route DELETE: Suppression d'un membre

@router.delete("/{member_id}", response_model=MembreRead)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """Supprime un adhérent par son ID"""
    # Appel du Service pour récupérer le membre
    member = membre_service.get_membre(db, member_id)
    
    if not member:
        # Gère l'absence de ressource (404)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membre non trouvé")
    
    # Appel du Repository pour supprimer le membre
    deleted_member = membre_service.delete_member(db, member_id)
    
    return deleted_member


# Route PATCH: Mise à jour partielle d'un membre
@router.patch("/{member_id}", response_model=MembreRead)
def patch_member(member_id: int, updates: MembreUpdate, db: Session = Depends(get_db)):
    """Met à jour partiellement un adhérent"""
    try:
        return membre_service.update_member(db, member_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise HTTPException(status_code=404, detail="Membre non trouvé")

