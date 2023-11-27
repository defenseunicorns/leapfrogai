# Adapted from Gunicorn's errors module.

class AppImportError(Exception):
    """ Exception raised when loading an application """