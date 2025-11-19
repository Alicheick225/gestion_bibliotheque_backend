# Contenu du fichier app/main.py
from fastapi import FastAPI

from app.api.v1 import membres, documents, users  # Importe les objets APIRouter

# Importer les modèles pour s'assurer que SQLAlchemy a enregistré
# toutes les classes mapped (évite les erreurs de relation non résolues)
import app.models  # noqa: F401

# 1. Initialisation de l'application
app = FastAPI(
    title="API de Gestion de Bibliothèque",
    description="Backend pour le système de gestion des emprunts et du catalogue.",
    version="1.0.0"
)

# 2. Définition du premier point de terminaison (endpoint)
@app.get("/")
def read_root():
    """
    Point de terminaison de base pour vérifier que l'API est en cours d'exécution.
    """
    return {"message": "Bienvenue sur l'API de Gestion de Bibliothèque. Voir /docs pour la documentation."}

# Inclure les routeurs. Le préfixe permet de séparer les routes.
app.include_router(membres.router, prefix="/api/v1/membres", tags=["Membres"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Utilisateurs"])
