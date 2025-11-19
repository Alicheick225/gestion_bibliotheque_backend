from typing import Optional
import datetime
import decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Auteur(Base):
    __tablename__ = 'auteur'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auteur_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    prenoms: Mapped[Optional[str]] = mapped_column(String(100))
    nationalite: Mapped[Optional[str]] = mapped_column(String(50))
    date_naissance: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_deces: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    document_auteur: Mapped[list['DocumentAuteur']] = relationship('DocumentAuteur', back_populates='auteur')


class Categorie(Base):
    __tablename__ = 'categorie'
    __table_args__ = (
        ForeignKeyConstraint(['parent_categorie_id'], ['categorie.id'], name='categorie_parent_categorie_id_fkey'),
        PrimaryKeyConstraint('id', name='categorie_pkey'),
        UniqueConstraint('libelle', name='categorie_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    parent_categorie_id: Mapped[Optional[int]] = mapped_column(Integer)

    parent_categorie: Mapped[Optional['Categorie']] = relationship('Categorie', remote_side=[id], back_populates='parent_categorie_reverse')
    parent_categorie_reverse: Mapped[list['Categorie']] = relationship('Categorie', remote_side=[parent_categorie_id], back_populates='parent_categorie')
    document: Mapped[list['Document']] = relationship('Document', back_populates='categorie')


class Editeur(Base):
    __tablename__ = 'editeur'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='editeur_pkey'),
        UniqueConstraint('libelle', name='editeur_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(150), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    ville: Mapped[Optional[str]] = mapped_column(String(100))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    document: Mapped[list['Document']] = relationship('Document', back_populates='editeur')


class Emplacement(Base):
    __tablename__ = 'emplacement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='emplacement_pkey'),
        UniqueConstraint('code_rayon', name='emplacement_code_rayon_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_rayon: Mapped[str] = mapped_column(String(50), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    exemplaire: Mapped[list['Exemplaire']] = relationship('Exemplaire', back_populates='emplacement')


class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='permission_pkey'),
        UniqueConstraint('libelle', name='permission_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    role_permission: Mapped[list['RolePermission']] = relationship('RolePermission', back_populates='permission')


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='role_pkey'),
        UniqueConstraint('libelle', name='role_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(50), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    role_permission: Mapped[list['RolePermission']] = relationship('RolePermission', back_populates='role')
    utilisateur_role: Mapped[list['UtilisateurRole']] = relationship('UtilisateurRole', back_populates='role')


class TypeMembre(Base):
    __tablename__ = 'type_membre'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='type_membre_pkey'),
        UniqueConstraint('libelle', name='type_membre_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(50), nullable=False)
    max_emprunt: Mapped[int] = mapped_column(Integer, nullable=False)
    duree_emprunt: Mapped[int] = mapped_column(Integer, nullable=False)
    taux_penalite_jour: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='type_membre')


class UtilisateurSys(Base):
    __tablename__ = 'utilisateur_sys'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='utilisateur_sys_pkey'),
        UniqueConstraint('email', name='unique_email'),
        UniqueConstraint('username', name='utilisateur_sys_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    est_actif: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenoms: Mapped[str] = mapped_column(String(100), nullable=False)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_derniere_connexion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    adresse: Mapped[Optional[str]] = mapped_column(String(255))
    telephone: Mapped[Optional[str]] = mapped_column(String(20))

    document: Mapped[list['Document']] = relationship('Document', back_populates='utilisateur_creation')
    utilisateur_role: Mapped[list['UtilisateurRole']] = relationship('UtilisateurRole', back_populates='utilisateur_sys')
    exemplaire: Mapped[list['Exemplaire']] = relationship('Exemplaire', back_populates='utilisateur_ajout')
    emprunt: Mapped[list['Emprunt']] = relationship('Emprunt', foreign_keys='[Emprunt.utilisateur_emprunt_id]', back_populates='utilisateur_emprunt')
    emprunt_: Mapped[list['Emprunt']] = relationship('Emprunt', foreign_keys='[Emprunt.utilisateur_retour_id]', back_populates='utilisateur_retour')
    penalite: Mapped[list['Penalite']] = relationship('Penalite', back_populates='utilisateur_creation')


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = (
        ForeignKeyConstraint(['categorie_id'], ['categorie.id'], name='document_categorie_id_fkey'),
        ForeignKeyConstraint(['editeur_id'], ['editeur.id'], name='document_editeur_id_fkey'),
        ForeignKeyConstraint(['utilisateur_creation_id'], ['utilisateur_sys.id'], name='document_utilisateur_creation_id_fkey'),
        PrimaryKeyConstraint('id', name='document_pkey'),
        UniqueConstraint('isbn', name='document_isbn_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    categorie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    editeur_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_creation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    annee_publication: Mapped[Optional[int]] = mapped_column(Integer)
    isbn: Mapped[Optional[str]] = mapped_column(String(13))
    resume: Mapped[Optional[str]] = mapped_column(Text)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    categorie: Mapped['Categorie'] = relationship('Categorie', back_populates='document')
    editeur: Mapped['Editeur'] = relationship('Editeur', back_populates='document')
    utilisateur_creation: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='document')
    document_auteur: Mapped[list['DocumentAuteur']] = relationship('DocumentAuteur', back_populates='document')
    exemplaire: Mapped[list['Exemplaire']] = relationship('Exemplaire', back_populates='document')
    reservation: Mapped[list['Reservation']] = relationship('Reservation', back_populates='document')


class Membre(Base):
    __tablename__ = 'membre'
    __table_args__ = (
        ForeignKeyConstraint(['type_membre_id'], ['type_membre.id'], name='membre_type_membre_id_fkey'),
        PrimaryKeyConstraint('id', name='membre_pkey'),
        UniqueConstraint('email', name='membre_email_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenoms: Mapped[str] = mapped_column(String(100), nullable=False)
    est_actif: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    date_adhesion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    type_membre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    adresse: Mapped[Optional[str]] = mapped_column(String(255))
    telephone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    type_membre: Mapped['TypeMembre'] = relationship('TypeMembre', back_populates='membre')
    reservation: Mapped[list['Reservation']] = relationship('Reservation', back_populates='membre')
    emprunt: Mapped[list['Emprunt']] = relationship('Emprunt', back_populates='membre')
    penalite: Mapped[list['Penalite']] = relationship('Penalite', back_populates='membre')


class RolePermission(Base):
    __tablename__ = 'role_permission'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['permission.id'], name='role_permission_permission_id_fkey'),
        ForeignKeyConstraint(['role_id'], ['role.id'], name='role_permission_role_id_fkey'),
        PrimaryKeyConstraint('role_id', 'permission_id', name='role_permission_pkey')
    )

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    permission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    permission: Mapped['Permission'] = relationship('Permission', back_populates='role_permission')
    role: Mapped['Role'] = relationship('Role', back_populates='role_permission')


class UtilisateurRole(Base):
    __tablename__ = 'utilisateur_role'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['role.id'], name='utilisateur_role_role_id_fkey'),
        ForeignKeyConstraint(['utilisateur_sys_id'], ['utilisateur_sys.id'], name='utilisateur_role_utilisateur_sys_id_fkey'),
        PrimaryKeyConstraint('utilisateur_sys_id', 'role_id', name='utilisateur_role_pkey')
    )

    utilisateur_sys_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    role: Mapped['Role'] = relationship('Role', back_populates='utilisateur_role')
    utilisateur_sys: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='utilisateur_role')


class DocumentAuteur(Base):
    __tablename__ = 'document_auteur'
    __table_args__ = (
        ForeignKeyConstraint(['auteur_id'], ['auteur.id'], name='document_auteur_auteur_id_fkey'),
        ForeignKeyConstraint(['document_id'], ['document.id'], name='document_auteur_document_id_fkey'),
        PrimaryKeyConstraint('document_id', 'auteur_id', name='document_auteur_pkey')
    )

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auteur_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    auteur: Mapped['Auteur'] = relationship('Auteur', back_populates='document_auteur')
    document: Mapped['Document'] = relationship('Document', back_populates='document_auteur')


class Exemplaire(Base):
    __tablename__ = 'exemplaire'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['document.id'], name='exemplaire_document_id_fkey'),
        ForeignKeyConstraint(['emplacement_id'], ['emplacement.id'], name='exemplaire_emplacement_id_fkey'),
        ForeignKeyConstraint(['utilisateur_ajout_id'], ['utilisateur_sys.id'], name='exemplaire_utilisateur_ajout_id_fkey'),
        PrimaryKeyConstraint('id', name='exemplaire_pkey'),
        UniqueConstraint('numero_inventaire', name='exemplaire_numero_inventaire_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_inventaire: Mapped[str] = mapped_column(String(50), nullable=False)
    etat: Mapped[str] = mapped_column(String(50), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False)
    date_mise_en_service: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    emplacement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_ajout_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    document: Mapped['Document'] = relationship('Document', back_populates='exemplaire')
    emplacement: Mapped['Emplacement'] = relationship('Emplacement', back_populates='exemplaire')
    utilisateur_ajout: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='exemplaire')
    emprunt: Mapped[list['Emprunt']] = relationship('Emprunt', back_populates='exemplaire')


class Reservation(Base):
    __tablename__ = 'reservation'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['document.id'], name='reservation_document_id_fkey'),
        ForeignKeyConstraint(['membre_id'], ['membre.id'], name='reservation_membre_id_fkey'),
        PrimaryKeyConstraint('id', name='reservation_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_reservation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    statut: Mapped[str] = mapped_column(String(50), nullable=False)
    date_modification: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    membre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_disponibilite: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_expiration_mise_de_cote: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    document: Mapped['Document'] = relationship('Document', back_populates='reservation')
    membre: Mapped['Membre'] = relationship('Membre', back_populates='reservation')


class Emprunt(Base):
    __tablename__ = 'emprunt'
    __table_args__ = (
        ForeignKeyConstraint(['exemplaire_id'], ['exemplaire.id'], name='emprunt_exemplaire_id_fkey'),
        ForeignKeyConstraint(['membre_id'], ['membre.id'], name='emprunt_membre_id_fkey'),
        ForeignKeyConstraint(['utilisateur_emprunt_id'], ['utilisateur_sys.id'], name='emprunt_utilisateur_emprunt_id_fkey'),
        ForeignKeyConstraint(['utilisateur_retour_id'], ['utilisateur_sys.id'], name='emprunt_utilisateur_retour_id_fkey'),
        PrimaryKeyConstraint('id', name='emprunt_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_emprunt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_retour_prevue: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    membre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exemplaire_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_emprunt_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_retour_reelle: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    utilisateur_retour_id: Mapped[Optional[int]] = mapped_column(Integer)

    exemplaire: Mapped['Exemplaire'] = relationship('Exemplaire', back_populates='emprunt')
    membre: Mapped['Membre'] = relationship('Membre', back_populates='emprunt')
    utilisateur_emprunt: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', foreign_keys=[utilisateur_emprunt_id], back_populates='emprunt')
    utilisateur_retour: Mapped[Optional['UtilisateurSys']] = relationship('UtilisateurSys', foreign_keys=[utilisateur_retour_id], back_populates='emprunt_')
    penalite: Mapped[list['Penalite']] = relationship('Penalite', back_populates='emprunt')


class Penalite(Base):
    __tablename__ = 'penalite'
    __table_args__ = (
        ForeignKeyConstraint(['emprunt_id'], ['emprunt.id'], name='penalite_emprunt_id_fkey'),
        ForeignKeyConstraint(['membre_id'], ['membre.id'], name='penalite_membre_id_fkey'),
        ForeignKeyConstraint(['utilisateur_creation_id'], ['utilisateur_sys.id'], name='penalite_utilisateur_creation_id_fkey'),
        PrimaryKeyConstraint('id', name='penalite_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    montant_du: Mapped[decimal.Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    montant_paye: Mapped[decimal.Decimal] = mapped_column(Numeric(6, 2), nullable=False, server_default=text('0.00'))
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    motif: Mapped[str] = mapped_column(String(50), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False)
    date_modification: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    membre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_creation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    emprunt_id: Mapped[Optional[int]] = mapped_column(Integer)

    emprunt: Mapped[Optional['Emprunt']] = relationship('Emprunt', back_populates='penalite')
    membre: Mapped['Membre'] = relationship('Membre', back_populates='penalite')
    utilisateur_creation: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='penalite')
