class ProductDoesntExist(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        product -- input product which caused the error
        message -- explanation of the error
    """
    def __init__(self, product, message="Product name not found in stock"):
        self.product = product
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"'{self.product}': {self.message}"


class SizeUnavailable(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        product -- input product which caused the error
        message -- explanation of the error
    """
    def __init__(self, product, message="Size is already sold out"):
        self.product = product
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"'{self.product}': {self.message}"


class ItemSoldOut(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        product -- input product which caused the error
        message -- explanation of the error
    """
    def __init__(self, product, message="Product or colorway is already sold out"):
        self.product = product
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"'{self.product}': {self.message}"