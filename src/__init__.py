# EXIF Cleaner Package

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .exif_processor import ExifProcessor
from .file_handler import FileHandler
from .version_manager import VersionManager
from .update_checker import UpdateChecker
from .gui import ExifCleanerGUI

__all__ = [
    "ExifProcessor",
    "FileHandler",
    "VersionManager",
    "UpdateChecker",
    "ExifCleanerGUI"
]