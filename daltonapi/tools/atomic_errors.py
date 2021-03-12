class RequestFailedError(Exception):
    """Exception called when an API request fails"""

    def __init__(self):
        self.message = "The request did not succeed."

    def __str__(self):
        return self.message


class AssetIDError(Exception):
    """Exception called when Asset ID is invalid"""

    def __init__(self, asset_id):
        self.message = (
            "Asset ID %s is invalid. The asset ID must be an integer." % asset_id
        )

    def __str__(self):
        return self.message


class NoFiltersError(Exception):
    """Exception called when no filters are provided"""

    def __init__(self):
        self.message = "This method requires at least one argument."

    def __str__(self):
        return self.message


class NoCollectionImageError(Exception):
    """Exception called when a collection has no image"""

    def __init__(self):
        self.message = "This collection has no image."

    def __str__(self):
        return self.message
