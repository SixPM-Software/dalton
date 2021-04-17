"""Dalton API Wrapper for WAX

This is the core module of the Dalton API wrapper, providing the Atom Class,
which can be used to query the various API endpoints."""

import json
from typing import List, Union

import requests

from .tools.atomic_classes import (
    Asset,
    Schema,
    Template,
    Collection,
    Transfer,
    AtomicBaseClass,
)
from .tools.atomic_errors import AtomicIDError, NoFiltersError, RequestFailedError

from .tools.wax_classes import Account


class Atom:
    """API Wrapper Class for AtomicAssets"""

    def __init__(self, endpoint: str = ""):
        """Creates an Atom object for accessing the AtomicAssets API

        Args:
            endpoint (str, optional): Sets API endpoint. Defaults to AtomicAssets hosted API.
        """
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = "https://wax.api.atomicassets.io/atomicassets/v1/"

    def _query(self, endpoint: str, params=None) -> dict:
        """Internal function to make a query and return data

        Args:
            endpoint (str): Endpoint of query
            params (dict): Dictionary of parameters for the query

        Returns:
            data (dict): Request data

        Raises:
            RequestFailedError: API success returned with False - likely invalid endpoint
        """
        if params is None:
            params = {}
        r = requests.get(endpoint, params=params)
        data = json.loads(r.content)
        if data["success"]:
            return data["data"]
        raise RequestFailedError

    def _process_input(self, field) -> str:
        if field.__class__.__bases__[0] == AtomicBaseClass:
            field = field.get_id()
        return field

    def get_asset(self, asset_id: str) -> Asset:
        """Gets an atomic asset by ID

        Args:
            asset_id (str): Asset ID

        Raises:
            AtomicIDError: Raised when an incorrect asset_id is passed

        Returns:
            Asset: Corresponding object
        """
        if not isinstance(asset_id, str) or not asset_id.isnumeric():
            raise AtomicIDError(asset_id)
        data = self._query(f"{self.endpoint}assets/{asset_id}")
        return Asset(data)

    def get_assets(
        self,
        owner: str = "",
        collection: Collection = "",
        schema: Schema = "",
        template: Template = "",
        limit=100,
        page: int = 1,
    ) -> List[Asset]:
        """Get a list of assets based on critera. Must have at least 1 criteria

        Args:
            owner (str, optional): account name. Defaults to "".
            collection (str, Collection, optional): collection name. Defaults to "".
            schema (str, Schema, optional): schema name. Defaults to "".
            template (str, Template, optional): template ID. Defaults to "".
            limit (int, optional): maximum number of results to return. Defaults to 100.

        Raises:
            NoFiltersError: Raised when no filters are passed

        Returns:
            list[Asset]: List of Asset objects matching the criteria
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
        if len(fields) == 0:
            raise NoFiltersError
        fields["limit"] = limit
        fields["page"] = page
        data = self._query(f"{self.endpoint}assets", params=fields)
        return [Asset(nft) for nft in data]

    def get_asset_history(
        self, item: Union[Asset, str], page: int = 1
    ) -> List[Transfer]:
        """Fetches transfer history of an asset

        Args:
            item (Union[Asset, str]): An Asset Object or a string with the asset id

        Returns:
            list[Transfer]: List of transfer objects
        """
        if isinstance(item, str) and not item.isnumeric():
            raise AtomicIDError(item)
        if isinstance(item, Asset):
            item = item.get_id()
        params = {"asset_id": item, "page": page}
        data = self._query(f"{self.endpoint}transfers", params=params)
        data = [Transfer(t) for t in data]
        return data

    def get_collection(self, collection_id: str, verbose: bool = False) -> Collection:
        """Gets an atomic collection by ID

        Args:
            collection_id (str): Collection ID

        Raises:
            AtomicIDError: Raised when an incorrect template_id is passed

        Returns:
            Template: Corresponding object
        """
        assert isinstance(collection_id, str), "Collection ID should be passed as a str"
        data = self._query(f"{self.endpoint}collections/{collection_id}")
        if verbose:
            print(data)
        return Collection(data)

    def get_template(
        self, collection_id: Union[Collection, str], template_id: str
    ) -> Template:
        """Gets an atomic template by ID

        Args:
            collection_id (Union[Collection, str]): Collection ID
            template_id (str): Template ID

        Raises:
            AtomicIDError: Raised when an incorrect template_id is passed

        Returns:
            Template: Corresponding object
        """
        assert isinstance(template_id, str), "Template ID should be passed as a str"
        assert isinstance(
            collection_id, (str, Collection)
        ), "Collection ID should be passed as a str or a Collection object"
        if isinstance(collection_id, Collection):
            collection_id = collection_id.get_id()
        if not template_id.isnumeric():
            raise AtomicIDError(template_id)

        data = self._query(f"{self.endpoint}templates/{collection_id}/{template_id}")
        return Template(data)

    def get_schema(
        self, collection_id: Union[Collection, str], schema_id: str
    ) -> Schema:
        """Gets an atomic template by ID

        Args:
            collection_id (Union[Collection, str]): Collection ID
            schema_id (str): Schema ID

        Raises:
            AtomicIDError: Raised when an incorrect schema_id is passed

        Returns:
            Schema: Corresponding object
        """
        assert isinstance(schema_id, str), "Schema ID should be passed as a str"
        assert isinstance(
            collection_id, (str, Collection)
        ), "Collection ID should be passed as a str or a Collection object"
        if isinstance(collection_id, Collection):
            collection_id = collection_id.get_id()

        data = self._query(f"{self.endpoint}schemas/{collection_id}/{schema_id}")
        return Schema(data)

    def get_holders(
        self,
        collection: Collection = "",
        schema: Schema = "",
        template: Template = "",
        limit: int = 100,
        page: int = 1,
    ):
        """Returns a list of accouts holding some entity (collection, schema, template)

        Args:
            collection (str, Collection, optional): collection name. Defaults to "".
            schema (str, Schema, optional): schema name. Defaults to "".
            template (str, Template, optional): template ID. Defaults to "".
            limit (int, optional): maximum number of results to return. Defaults to 100.

        Raises:
            NoFiltersError: Raised when no filters are passed

        Returns:
            list[dict]: List of dicts containing account names and number
            of matching assets held.
        """    
        fields = {
            "collection_name": self._process_input(collection),
            "schema_name": self._process_input(schema),
            "template_id": self._process_input(template),
        }
        for key in list(fields.keys()):
            if fields[key] == "":
                del fields[key]
        if len(fields) == 0:
            raise NoFiltersError
        fields["limit"] = limit
        fields["page"] = page
        data = self._query(f"{self.endpoint}accounts", params=fields)
        return data

    def get_burned(
        self,
        owner: str = "",
        collection: Collection = "",
        schema: Schema = "",
        template: Template = "",
        limit=100,
    ) -> List[Asset]:
        """Get a list of burned assets based on critera. Must have at least 1 criteria

        Args:
            owner (str, optional): account name. Defaults to "".
            collection (str, Collection, optional): collection name. Defaults to "".
            schema (str, Schema, optional): schema name. Defaults to "".
            template (str, Template, optional): template ID. Defaults to "".
            limit (int, optional): maximum number of results to return. Defaults to 100.

        Raises:
            NoFiltersError: Raised when no filters are passed

        Returns:
            list[Asset]: List of Asset objects matching the criteria
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
        if len(fields) == 0:
            raise NoFiltersError
        fields["limit"] = limit
        fields["burned"] = True

        data = self._query(f"{self.endpoint}/assets", params=fields)
        return [Asset(nft) for nft in data]

    # def get_transfer(self):
    #     pass

    def get_transfers(
        self,
        sender: str = "",
        recipient: str = "",
        collection: Collection = "",
        schema: Schema = "",
        template: Template = "",
        page: int = 1,
        limit=100,
    ) -> List[Transfer]:
        """Search for transfers fulfilling a criteria

        Args:
            sender (str, optional): Sender address. Defaults to "".
            recipient (str, optional): Recipient address. Defaults to "".
            collection (str, Collection, optional): collection name. Defaults to "".
            schema (str, Schema, optional): schema name. Defaults to "".
            template (str, Template, optional): template ID. Defaults to "".
            page (int, optional): start page. Defaults to 1
            limit (int, optional): maximum number of results to return. Defaults to 100.

        Raises:
            NoFiltersError: Raised when no criteria provided

        Returns:
            list[Transfer]: List of Transfer objects matching the criteria
        """
        assert (
            sender != "" or recipient != ""
        ), "Sender and recipient can't both be blank"
        fields = {
            "collection_name": self._process_input(collection),
            "schema_name": self._process_input(schema),
            "template_id": self._process_input(template),
            "sender": sender,
            "recipient": recipient,
            "page": page,
        }
        for key in list(fields.keys()):
            if fields[key] == "":
                del fields[key]
        fields["limit"] = limit
        data = self._query(f"{self.endpoint}transfers", params=fields)
        if data:
            built_data = [Transfer(t) for t in data]
            return built_data
        return []


class Wax:
    """Class for the WAX API"""

    def __init__(self, endpoint: str = ""):
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = "https://api.waxsweden.org/"

    def _query(self, endpoint: str, method: str = "POST", data=None):
        """Internal function to make a query and return data

        Args:
                endpoint (str): Endpoint of query
                data (dict): Dictionary of parameters for the query

        Returns:
                data (dict): Request data

        Raises:
                RequestFailedError: API success returned with False - likely invalid endpoint
        """
        if data is None:
            data = {}
        request_data = requests.request(method, endpoint, json=data)
        json_data = json.loads(request_data.content)
        if request_data.status_code == 200:
            return json_data
        raise RequestFailedError

    def get_account(self, account_name: str):
        """[summary]

        Args:
            account_name (str): [description]

        Returns:
            [type]: [description]
        """
        data = {"account_name": account_name}
        account = self._query(f"{self.endpoint}v1/chain/get_account", data=data)
        return Account(account)


class WaxTable:
    """Class for WAX Tables" """

    def __init__(self, contract: str, table: str, endpoint: str = ""):
        self.contract = contract
        self.table = table
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = "https://api.waxsweden.org/v1/chain/get_table_rows"

    def _query(self, endpoint: str, method: str = "POST", data=None):
        """Internal function to make a query and return data

        Args:
                endpoint (str): Endpoint of query
                data (dict): Dictionary of parameters for the query

        Returns:
                data (dict): Request data

        Raises:
                RequestFailedError: API success returned with False - likely invalid endpoint
        """
        if data is None:
            data = {}
        request_data = requests.request(method, endpoint, json=data)
        json_data = json.loads(request_data.content)
        if request_data.status_code == 200:
            return json_data
        raise RequestFailedError

    def get_table_row(self, scope: str, key: str):
        """Returns a table row using a scope and key

        Args:
            scope (str): [description]
            key (str): [description]

        Raises:
            RequestFailedError: When Request status code not 200

        Returns:
            dict: [description]
        """
        data = {
            "code": self.contract,
            "table": self.table,
            "scope": scope,
            "upper_bound": key,
            "lower_bound": key,
            "json": True,
        }
        request_data = requests.post(self.endpoint, json=data)
        json_data = json.loads(request_data.content)
        if request_data.status_code == 200:
            row = json_data["rows"]
            if row:
                return row[0]
            return None
        raise RequestFailedError

    def get_table_rows(
        self, scope: str, search_params: dict, start_at: int = 1, limit: int = 1000
    ):
        """Returns a list of table rows matching search criteria. This can be a
        very slow process for large tables.

        Args:
            scope (str): Scope of table rows
            search_params (dict): Dict of column_name:value pairs
            start_at (int, optional): Row to start searching at. Defaults to 1.

        Raises:
            RequestFailedError: When Request status code not 200

        Returns:
            list: list of dict
        """
        data = {
            "code": self.contract,
            "table": self.table,
            "scope": scope,
            "json": True,
            "limit": limit,
        }
        hits = []
        next_key = start_at
        while True:
            data["lower_bound"] = next_key
            request_data = requests.post(self.endpoint, json=data)
            json_data = json.loads(request_data.content)
            if request_data.status_code == 200:
                rows = json_data["rows"]
                for row in rows:
                    if all(row[key] == val for key, val in search_params.items()):
                        hits.append(row)
                        continue
                if json_data["more"]:
                    next_key = json_data["next_key"]
                    continue
                break
            raise RequestFailedError
        return hits
