from app.exceptions.base import InventoryException

class CustomerAlreadyExists(InventoryException):
    pass

class CustomerNotFound(InventoryException):
    pass