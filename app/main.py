# Contenu du fichier app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auteurs, categories, editeurs, membres, documents, users  # Importe les objets APIRouter

# Importer les modèles pour s'assurer que SQLAlchemy a enregistré
# toutes les classes mapped (évite les erreurs de relation non résolues)
import app.models  # noqa: F401

# 1. Initialisation de l'application
app = FastAPI(
    title="API de Gestion de Bibliothèque",
    description="Backend pour le système de gestion des emprunts et du catalogue.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",  # Exemple standard de port Vite
    "http://127.0.0.1:5173",
    # Ajoutez d'autres ports si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # ⬅️ Liste des origines autorisées
    allow_credentials=True,            # ⬅️ Autoriser les cookies/headers d'authentification
    allow_methods=["*"],               # ⬅️ Autoriser TOUTES les méthodes (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],               # ⬅️ Autoriser TOUS les en-têtes (y compris Content-Type, Authorization)
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
app.include_router(auteurs.router, prefix="/api/v1/auteurs", tags=["Auteurs"])
app.include_router(editeurs.router, prefix="/api/v1/editeurs", tags=["Éditeurs"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Catégories"])