from typing import Optional
import datetime
import decimal
from app.core.database import Base
from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Reservation(Base):
    __tablename__ = 'reservation'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['document.id'], name='reservation_document_id_fkey'),
        ForeignKeyConstraint(['membre_id'], ['membre.id'], name='reservation_membre_id_fkey'),
        PrimaryKeyConstraint('id', name='reservation_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_reservation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False)
    date_modification_statut: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    motif: Mapped[str] = mapped_column(String(50), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False)
    date_modification_statut: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    membre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    utilisateur_creation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    emprunt_id: Mapped[Optional[int]] = mapped_column(Integer)

    emprunt: Mapped[Optional['Emprunt']] = relationship('Emprunt', back_populates='penalite')
    membre: Mapped['Membre'] = relationship('Membre', back_populates='penalite')
    utilisateur_creation: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='penalite')
