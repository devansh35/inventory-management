from app.exceptions.base import InventoryException

class OrderNotFound(InventoryException):
    pass

class InsufficientStock(InventoryException):
    pass