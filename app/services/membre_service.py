from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.utilisateur import UtilisateurSys
from ..repositories import membre_repo
from ..schemas.membre_schema import MembreCreate, MembreRead, MembreUpdate

def create_new_member(db: Session, member_data: MembreCreate, current_user_id: int) -> MembreRead:
    """
    Logique métier pour la création d'un membre (y compris les vérifications).
    """
    # 1. LOGIQUE MÉTIER : Vérification de l'unicité de l'email
    existing_member = membre_repo.get_member_by_email(db, member_data.email)
    if existing_member:
        # Remonter une erreur personnalisée pour que le Routeur la gère en HTTP 400
        raise ValueError("Cet email est déjà utilisé par un autre adhérent.")

    # 2. LOGIQUE MÉTIER : Validation simple du type (devrait être fait par un autre service, mais simple ici)
    type_obj = membre_repo.get_type_membre_by_id(db, member_data.type_membre_id)
    # Vérifier que le type existe
    if not type_obj:
        raise ValueError("Type de membre ID invalide.")

    type_membre_libelle = type_obj.libelle
    if type_membre_libelle not in ["Etudiant", "Professeur", "Standard"]:
        raise ValueError("Type de membre ID invalide.")

    # 3. Appel du Repository pour l'insertion DB
    db_membre = membre_repo.create_membre(db, member_data)
    
    # 4. Conversion de l'objet DB en Schéma de Sortie (sérialisation)
    return MembreRead.model_validate(db_membre)

def get_member(db: Session, membre_id: int) -> MembreRead | None:
    """
    Logique métier pour récupérer et traiter les informations d'un membre.
    """
    db_membre = membre_repo.get_membre_by_id(db, membre_id)
    
    if not db_membre:
        return None 
        
    # LOGIQUE MÉTIER : On pourrait ajouter ici la vérification des droits ou des pénalités
    # if not db_membre.est_actif:
    #     raise HTTPException(status_code=403, detail="Membre inactif")

    return MembreRead.model_validate(db_membre)

def get_members(db: Session) -> list[MembreRead]:
    """
    Logique métier pour récupérer et formater les informations des membres.
    Retourne une liste (vide si aucun membre).
    """
    db_members = membre_repo.get_members(db)

    # Si la requête retourne une liste vide, renvoyer une liste vide (ne pas renvoyer None)
    if not db_members:
        return []

    # Convertir chaque objet DB en schéma de sortie
    return [MembreRead.model_validate(m) for m in db_members]


def delete_member(db: Session, member_id: int) -> MembreRead:
    """
    Logique métier pour supprimer un membre.
    """
    db_member = membre_repo.get_member_by_id(db, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Membre non trouvé")

    # Appel du Repository pour la suppression
    membre_repo.delete_member(db, member_id)
    return MembreRead.model_validate(db_member)

def update_member(db: Session, member_id: int, update_data: MembreUpdate) -> MembreRead:
    """
    Logique métier pour mettre à jour les informations d'un membre.
    """
    db_member = membre_repo.update_member(db, member_id, update_data)
    if not db_member:
        raise HTTPException(status_code=404, detail="Membre non trouvé")

    return MembreRead.model_validate(db_member)