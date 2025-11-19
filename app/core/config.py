from pydantic_settings import BaseSettings, SettingsConfigDict

# Pydantic BaseSettings charge automatiquement les variables d'environnement
# à partir des noms des attributs (ex: DATABASE_URL est chargé dans self.database_url)
class Settings(BaseSettings):
    # Infos de connexion PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # URL de connexion complète pour SQLAlchemy
    # Remplacez le driver 'postgresql' par 'postgresql+psycopg' ou 'postgresql+asyncpg' 
    # si vous utilisez un driver spécifique.
   # CORRECTION : Utilisation de @property pour calculer la chaîne après le chargement des settings
    @property
    def DATABASE_URL(self) -> str:
        # Nous utilisons 'self.POSTGRES_USER' etc., car les variables existent maintenant sur l'instance (self)
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Configuration pour charger les variables depuis un fichier .env (si existant)
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    SECRET_KEY: str = "12345kativaju"
    ALGORITHM: str = "HS256" # Algorithme standard
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Durée de validité du token



settings = Settings()