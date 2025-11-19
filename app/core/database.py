from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from typing import Generator

# 1. Création du moteur de connexion (Engine)
# 'echo=True' est utile pour le débug car il affiche les requêtes SQL générées
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True
)

# 2. Création de la Session Locale
# C'est l'objet que chaque requête utilisera pour interagir avec la DB
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 3. Base déclarative (utilisée par les modèles ORM pour la structure de la DB)
Base = declarative_base()


# 4. La dépendance FastAPI (Injection de Dépendance)
def get_db() -> Generator:
    """
    Dépendance utilisée par les routeurs et les services pour obtenir
    une session de base de données, qui sera automatiquement fermée après la requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()