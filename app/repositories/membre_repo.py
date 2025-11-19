from sqlalchemy.orm import Session
from ..models.membre import Membre, TypeMembre
from ..schemas.membre_schema import MembreCreate, MembreUpdate
from sqlalchemy import select

def create_membre(db: Session, membre_data: MembreCreate) -> Membre:
    """ Insère un nouvel enregistrement membre dans la base de données. """
    
    # Conversion du Schéma Pydantic en Modèle DB (la clé étrangère doit correspondre au MLD)
    db_membre = Membre(
        nom=membre_data.nom,
        prenoms=membre_data.prenoms,
        adresse=membre_data.adresse,
        telephone=membre_data.telephone,
        email=membre_data.email,
        type_membre_id=membre_data.type_membre_id
    )
    
    db.add(db_membre)
    db.commit()
    db.refresh(db_membre) # Récupère l'objet mis à jour avec son ID
    
    # Ajouter dynamiquement l'attribut `type_membre_libelle` à l'instance
    # (ne pas utiliser la syntaxe de dictionnaire qui échoue sur une instance SQLAlchemy)
    type_obj = get_type_membre_by_id(db, membre_data.type_membre_id)
    if type_obj:
        setattr(db_membre, "type_membre_libelle", type_obj.libelle)

    return db_membre

# Le Repository utilise des fonctions synchrones (def) car nous sommes en mode synchrone
def get_membre_by_id(db: Session, membre_id: int) -> Membre | None:
    """ Récupère un membre par son ID. """
    db_member = db.query(Membre).filter(Membre.id == membre_id).first()
    type_obj = get_type_membre_by_id(db, db_member.type_membre_id) if db_member else None
    if db_member and type_obj:
        setattr(db_member, "type_membre_libelle", type_obj.libelle)
    return db_member

def get_membre_by_email(db: Session, email: str) -> Membre | None:
    """ Récupère un membre par son email. """
    return db.query(Membre).filter(Membre.email == email).first()


def get_type_membre_by_id (db: Session, type_membre_id: int) -> TypeMembre | None:
    """Récupère un type membre par son id"""
    return db.query(TypeMembre).filter(TypeMembre.id == type_membre_id).first()

def get_members(db: Session) -> Membre | None: 
    """Fetch all the members of the database"""
    db_members = db.query(Membre).all()
    for member in db_members:
        type_obj = get_type_membre_by_id(db, member.type_membre_id)
        if type_obj:
            setattr(member, "type_membre_libelle", type_obj.libelle)
    return db_members


def delete_member(db: Session, member_id: int) -> Membre:
    """Supprime un membre par son ID et retourne l'objet supprimé"""
    member = db.query(Membre).filter(Membre.id == member_id).first()
    if member:
        db.delete(member)
        db.commit()

    type_obj = get_type_membre_by_id(db, member.type_membre_id) if member else None
    if member and type_obj:
        setattr(member, "type_membre_libelle", type_obj.libelle)
    return member


def update_member(db: Session, member_id: int, update_data: MembreUpdate) -> Membre:
    """Met à jour les informations d'un membre et retourne l'objet mis à jour"""
    member = db.query(Membre).filter(Membre.id == member_id).first()
    if not member:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    type_obj = get_type_membre_by_id(db, member.type_membre_id)
    if member and type_obj:
        setattr(member, "type_membre_libelle", type_obj.libelle)
        
    return member