from app.exceptions.base import InventoryException

class ProductAlreadyExists(InventoryException):
    pass

class ProductNotFound(InventoryException):
    pass