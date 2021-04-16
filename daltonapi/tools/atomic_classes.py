"""Atomic Classes

Classes for instantizing Atomic Asset data structures"""

from typing import Dict, List, Tuple
from datetime import datetime
from .atomic_errors import NoCollectionImageError


class AtomicBaseClass:
    """Template class for AtomicAssets API data"""

    def __init__(self, api_data):
        """Creates the Atomic Object

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        for key in api_data:
            key, data = self._process_data(key, api_data[key])
            setattr(self, "_" + key, data)
        self.key = ""

    def _process_data(self, key: str, data: dict) -> Tuple[str, "AtomicBaseClass"]:
        """function to intercept and construct classes

        Args:
            key (str): key to the dict

        Returns:
            dict or class object
        """
        conversions = {
            "collection": Collection,
            "schema": Schema,
            "template": Template,
        }
        if key in conversions and data is not None:
            data = conversions[key](data)
        return (key, data)

    def get_id(self) -> str:
        """Returns the primary atomic assets identifier of the object
        E.g. For an asset, returns asset id. For a schema, returns schema name

        Returns:
            str: id
        """
        return self.key

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"{self.__class__.__name__}({self.key})"


class Asset(AtomicBaseClass):
    """Class for instantizing Atomic Assets"""

    def __init__(self, api_data):
        """Creates an Asset from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._asset_id

    @property
    def name(self) -> str:
        """Returns the asset's name

        Returns:
            str: Asset name
        """
        return self._data["name"]

    @property
    def owner(self) -> str:
        """Returns the Asset's owner

        Returns:
            str: Asset Owner
        """
        return self._owner

    @property
    def mint(self) -> Tuple[int, int, int]:
        """Method to obtain mint information of the asset
        if max supply (list[2]) returns 0, there is no maximum limit

        Returns:
            tuple(int,int,int): [mint number, total in circulation, max supply]
        """

        if getattr(self.template, "_issued_supply", None) is None:
            return (
                0,
                0,
                0,
            )  # if no issued supply, likely this asset exists without template
        return tuple(
            [
                int(i)
                for i in [
                    self._template_mint,
                    self.template._issued_supply,
                    self.template._max_supply,
                ]
            ]
        )

    @property
    def image(self) -> str:
        """Returns the primary image of the asset

        Returns:
            str: direct link to the image
        """
        return f"https://ipfs.io/ipfs/{self._data['img']}"

    @property
    def all_media(self) -> Dict[str, str]:
        """Returns a dict of all media properties of the asset

        Returns:
            dict: key:image_link pairs
        """
        return {
            key: f"https://ipfs.io/ipfs/{val}"
            for key, val in self._data.items()
            if val.startswith("Qm")
        }

    @property
    def burned(self) -> Tuple[str, str, str]:
        """Burn information of the asset.
        Returns (None,None,None) if unburned.

        Returns:
            tuple: (block, timestamp, account)
        """
        return (self._burned_at_block, self._burned_at_time, self._burned_by_account)

    @property
    def burnable(self) -> bool:
        """Is the asset burnable?

        Returns:
            bool
        """
        return self._is_burnable

    @property
    def transferable(self) -> bool:
        """Is the asset transferable?

        Returns:
            bool
        """
        return self._is_transferable

    @property
    def last_transferred(self) -> Tuple[str, str]:
        """Information about the last transfer of the asset

        Returns:
            tuple: (block,timestamp)
        """
        return (self._transferred_at_block, self._transferred_at_time)

    @property
    def last_updated(self) -> Tuple[str, str]:
        """Information about the last update to the asset

        Returns:
            tuple: (block,timestamp)
        """
        return (self._updated_at_block, self._updated_at_time)

    @property
    def collection(self) -> "Collection":
        """Returns the Asset's collection

        Returns:
            Collection: The collection of the Asset
        """
        return self._collection

    @property
    def schema(self) -> "Schema":
        """Returns the Asset's schema

        Returns:
            Schema: The schema of the Asset
        """
        return self._schema

    @property
    def template(self) -> "Template":
        """Returns the Asset's template
        Returns None if no template

        Returns:
            Template: The template of the Asset
        """
        return self._template

    def __str__(self):
        """Pretty prints basic asset information in format
        `Asset [Asset ID]: [Collection Name] - [Asset Name] #[Mint/Total Supply] (Max Supply: [Max Supply])`

        Returns:
            str: String representation of the class
        """
        name = self.name
        asset_id = self._asset_id
        collection = self._collection.get_id()
        mint = ""
        if self.mint != (0, 0, 0):
            mint = " #%s/%s (Max Supply: %s)" % self.mint
        return f"Asset {asset_id}:  {collection} - {name} {mint}"


class Collection(AtomicBaseClass):
    """Class for instantizing Atomic Asset Collections"""

    def __init__(self, api_data):
        """Creates a Collection from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._collection_name

    @property
    def image(self) -> str:
        """Returns the primary image of the collection

        Returns:
            str: direct link to the image
        """
        if self._img is None:
            raise NoCollectionImageError
        return f"https://ipfs.io/ipfs/{self._img}"


class Schema(AtomicBaseClass):
    """Class for instantizing Atomic Asset Schemas"""

    def __init__(self, api_data):
        """Creates  Schema from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._schema_name


class Template(AtomicBaseClass):
    """Class for instantizing Atomic Asset Templates"""

    def __init__(self, api_data):
        """Creates a Template from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._template_id

    @property
    def image(self) -> str:
        """Returns the primary image of the asset

        Returns:
            str: direct link to the image
        """
        return f"https://ipfs.io/ipfs/{self._immutable_data['img']}"

    @property
    def all_media(self) -> Dict[str, str]:
        """Returns a dict of all media properties of the asset

        Returns:
            dict: key:image_link pairs
        """
        return {
            key: f"https://ipfs.io/ipfs/{val}"
            for key, val in self._immutable_data.items()
            if val.startswith("Qm")
        }

    @property
    def name(self) -> str:
        """Returns template name

        Returns:
            str: Template name
        """
        return self._immutable_data["name"]


class Offer(AtomicBaseClass):
    """Class for instantizing Atomic Asset Offer Data

    More features coming soon"""

    def __init__(self, api_data):
        """Creates an Offer data object from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._offer_id


class Transfer(AtomicBaseClass):
    """Class for instantizing Atomic Asset Transfer Data"""

    def __init__(self, api_data):
        """Creates a Transfer data object from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self._transfer_id

    @property
    def assets(self) -> List["Asset"]:
        """Returns a list of assets transferred in the transfer

        Returns:
            List: List of Asset
        """
        return [Asset(nft) for nft in self._assets]

    @property
    def memo(self) -> str:
        """Returns memo of transfer

        Returns:
            str: Memo text
        """
        return self._memo

    @property
    def contract(self) -> str:
        """Returns contract type of transfer

        Returns:
            str: contract type
        """
        return self._contract

    @property
    def timestamp(self) -> int:
        """Returns timestamp of transfer

        Returns:
            int: timestamp to millisecond precision
        """
        return int(self._created_at_time)

    def __str__(self):
        """Pretty prints Transfer information in the format
        `[DateAndTime]: [Sender] ---> [Recipient]`

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        when = datetime.fromtimestamp(float(self._created_at_time) / 1000).isoformat()
        sender = self._sender_name
        recipient = self._recipient_name
        return f"{when}: {sender} ---> {recipient} : {self.memo}"
