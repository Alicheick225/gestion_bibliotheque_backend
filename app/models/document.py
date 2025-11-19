from typing import Optional
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, func, text
import datetime
from app.models.emprunt import Reservation
from app.models.utilisateur import UtilisateurSys
import decimal

class Auteur(Base):
    __tablename__ = 'auteur'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auteur_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenoms: Mapped[Optional[str]] = mapped_column(String(100))
    nationalite: Mapped[Optional[str]] = mapped_column(String(50))
    date_naissance: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_deces: Mapped[Optional[datetime.date]] = mapped_column(Date)
    document_auteur: Mapped[list['DocumentAuteur']] = relationship('DocumentAuteur', back_populates='auteur')
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    date_modification: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'), onupdate=func.now())


class Categorie(Base):
    __tablename__ = 'categorie'
    __table_args__ = (
        ForeignKeyConstraint(['parent_categorie_id'], ['categorie.id'], name='categorie_parent_categorie_id_fkey'),
        PrimaryKeyConstraint('id', name='categorie_pkey'),
        UniqueConstraint('libelle', name='categorie_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ville: Mapped[Optional[str]] = mapped_column(String(100))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    document: Mapped[list['Document']] = relationship('Document', back_populates='editeur')


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
    categorie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    editeur_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_creation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    annee_publication: Mapped[Optional[int]] = mapped_column(Integer)
    isbn: Mapped[Optional[str]] = mapped_column(String(13))
    resume: Mapped[Optional[str]] = mapped_column(Text)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=False, onupdate=func.now())

    categorie: Mapped['Categorie'] = relationship('Categorie', back_populates='document')
    editeur: Mapped['Editeur'] = relationship('Editeur', back_populates='document')
    utilisateur_creation: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='document')
    document_auteur: Mapped[list['DocumentAuteur']] = relationship('DocumentAuteur', back_populates='document')
    exemplaire: Mapped[list['Exemplaire']] = relationship('Exemplaire', back_populates='document')
    reservation: Mapped[list['Reservation']] = relationship('Reservation', back_populates='document')


class DocumentAuteur(Base):
    __tablename__ = 'document_auteur'
    __table_args__ = (
        ForeignKeyConstraint(['auteur_id'], ['auteur.id'], name='document_auteur_auteur_id_fkey'),
        ForeignKeyConstraint(['document_id'], ['document.id'], name='document_auteur_document_id_fkey'),
        PrimaryKeyConstraint('document_id', 'auteur_id', name='document_auteur_pkey')
    )

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auteur_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    emplacement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_ajout_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    document: Mapped['Document'] = relationship('Document', back_populates='exemplaire')
    emplacement: Mapped['Emplacement'] = relationship('Emplacement', back_populates='exemplaire')
    utilisateur_ajout: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='exemplaire')
    emprunt: Mapped[list['Emprunt']] = relationship('Emprunt', back_populates='exemplaire')




class Emplacement(Base):
    __tablename__ = 'emplacement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='emplacement_pkey'),
        UniqueConstraint('code_rayon', name='emplacement_code_rayon_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_rayon: Mapped[str] = mapped_column(String(50), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    exemplaire: Mapped[list['Exemplaire']] = relationship('Exemplaire', back_populates='emplacement')
