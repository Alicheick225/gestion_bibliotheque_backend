"""Package-level import to ensure all model modules are imported and
registered with SQLAlchemy's metadata when the package is imported.

This helps avoid relationship resolution errors caused by models not
being imported before mapper configuration.
"""

# Import model modules so they are registered on import
from . import document  # noqa: F401
from . import emprunt  # noqa: F401
from . import membre  # noqa: F401
from . import utilisateur  # noqa: F401

