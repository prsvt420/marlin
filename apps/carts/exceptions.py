class CartError(Exception):
    pass


class CartItemError(CartError):
    pass


class ProductUnavailableError(CartError):
    pass


class InsufficientStockError(CartError):
    pass


class CartItemNotFoundError(CartItemError):
    pass


class CartItemAlreadyExistsError(CartItemError):
    pass


class InvalidCartItemQuantityError(CartItemError):
    pass
