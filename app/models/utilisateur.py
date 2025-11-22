from typing import Optional
import datetime
import decimal
from app.core.database import Base

from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='permission_pkey'),
        UniqueConstraint('libelle', name='permission_libelle_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_modification: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    role_permission: Mapped[list['RolePermission']] = relationship('RolePermission', back_populates='role')
    utilisateur_role: Mapped[list['UtilisateurRole']] = relationship('UtilisateurRole', back_populates='role')




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



class RolePermission(Base):
    __tablename__ = 'role_permission'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['permission.id'], name='role_permission_permission_id_fkey'),
        ForeignKeyConstraint(['role_id'], ['role.id'], name='role_permission_role_id_fkey'),
        PrimaryKeyConstraint('role_id', 'permission_id', name='role_permission_pkey')
    )

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    permission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

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
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    role: Mapped['Role'] = relationship('Role', back_populates='utilisateur_role')
    utilisateur_sys: Mapped['UtilisateurSys'] = relationship('UtilisateurSys', back_populates='utilisateur_role')

