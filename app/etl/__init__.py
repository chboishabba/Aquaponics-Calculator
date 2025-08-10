"""ETL helpers for loading reference datasets.

Each module exposes a ``load(session, data_file=None)`` function that
reads a CSV file and populates the database.
"""

from .ausnut import load as load_ausnut
from .fdc import load as load_fdc
from .feedipedia import load as load_feedipedia
from .aquaculture import load as load_aquaculture

__all__ = [
    "load_ausnut",
    "load_fdc",
    "load_feedipedia",
    "load_aquaculture",
]
