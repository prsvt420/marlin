class OrderError(Exception):
    pass


class EmptyCartError(OrderError):
    pass
