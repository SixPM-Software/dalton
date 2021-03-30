"""Atomic Errors

Error Classes for the package"""


class RequestFailedError(Exception):
    """Exception called when an API request fails"""

    def __init__(self):
        super().__init__(self)
        self.message = "The request did not succeed."

    def __str__(self):
        return self.message


class AtomicIDError(Exception):
    """Exception called when Atomic ID is invalid"""

    def __init__(self, asset_id):
        super().__init__(self)
        self.message = (
            f"Atomic ID {asset_id} is invalid. The Atomic ID must be a string integer."
        )

    def __str__(self):
        return self.message


class NoFiltersError(Exception):
    """Exception called when no filters are provided"""

    def __init__(self):
        super().__init__(self)
        self.message = "This method requires at least one argument."

    def __str__(self):
        return self.message


class NoCollectionImageError(Exception):
    """Exception called when a collection has no image"""

    def __init__(self):
        super().__init__(self)
        self.message = "This collection has no image."

    def __str__(self):
        return self.message
