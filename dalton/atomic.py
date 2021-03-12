import json
from pathlib import Path

import requests

from atomic_classes import *
from atomic_errors import AssetIDError, NoFiltersError, RequestFailedError


class Atom:
    def __init__(self, endpoint="https://wax.api.atomicassets.io/atomicassets/v1/"):
        self.endpoint = endpoint

    def _query(self, endpoint: str):
        """Internal function to make a query and return data

        Args:
                endpoint (str): Endpoint of query

        Returns:
                data (dict): Request data

        Raises:
                RequestFailedError: API success returned with False - likely invalid endpoint
        """
        data = requests.get(endpoint)
        data = json.loads(data.content)
        if data["success"]:
            return data["data"]
        raise RequestFailedError

    def _process_input(self, field):
        if field.__class__.__bases__[0] == AtomicBaseClass:
            field = field.get_id()
        return field

    def get_asset(self, asset_id: str):
        """Gets an atomic asset by ID

        Args:
                asset_id (str): Asset ID

        Raises:
                AssetIDError: Raised when an incorrect asset_id is passed

        Returns:
                Asset: Corresponding object
        """
        assert type(asset_id) == str, "Asset ID should be passed as a strpr"
        if not asset_id.isnumeric():
            raise AssetIDError(asset_id)
        data = self._query(self.endpoint + "assets/" + asset_id)
        return Asset(data)

    def get_assets(self, owner="", collection="", schema="", template="", limit=100):
        """Get a list of assets based on critera. Must have at least 1 criteria
        Args:
                owner (str, optional): account name. Defaults to "".
                collection (str, optional): collection name. Defaults to "".
                schema (str, optional): schema name. Defaults to "".
                template (str, optional): template ID. Defaults to "".
                limit (int, optional): maximum number of results to return. Defaults to 100.

        Raises:
                NoFiltersError: Raised when no filters are passed

        Returns:
                list[Assets]: List of asset objects matching the criteria
        """
        fields = {
            "owner": self._process_input(owner),
            "collection_name": self._process_input(collection),
            "schema_name": self._process_input(schema),
            "template_id": self._process_input(template),
        }
        for key in list(fields.keys()):
            if fields[key] == "":
                del fields[key]
        if not len(fields):
            raise NoFiltersError
        q = "&".join([key + "=" + val for key, val in fields.items()])
        data = self._query(self.endpoint + "assets?limit=%s&" % limit + q)
        return [Asset(nft) for nft in data]
