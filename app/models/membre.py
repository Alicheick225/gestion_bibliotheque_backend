from typing import Optional
import datetime
import decimal

from app.core.database import Base

from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='type_membre')
