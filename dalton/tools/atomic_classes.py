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
            setattr(self, key, data)
        self.key = ""

    def _process_data(self, key: str, data: dict):
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
        if key in conversions:
            data = conversions[key](data)
        return (key, data)

    def get_id(self):
        """Returns the primary atomic assets identifier of the object
        E.g. For an asset, returns asset id. For a schema, returns schema name


        Returns:
                str: id
        """
        return self.key


class Asset(AtomicBaseClass):
    """Class for instantizing Atomic Assets"""

    def __init__(self, api_data):
        """Creates an Asset from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.asset_id

    def get_mint(self):
        """Method to obtain mint information of the asset
        if max supply (list[2]) returns 0, there is no maximum limit
        Returns:
                list[int,int,int]: [mint number, total in circulation, max supply]
        """
        return [
            int(i)
            for i in [
                self.template_mint,
                self.template.issued_supply,
                self.template.max_supply,
            ]
        ]

    def get_image(self):
        """Returns the primary image of the asset

        Returns:
            str: direct link to the image
        """
        return "https://ipfs.io/ipfs/" + self.data["img"]

    def __str__(self):
        """Pretty prints basic asset information in format
        `Asset [Asset ID]: [Collection Name] - [Asset Name] #[Mint/Total Supply] (Max Supply: [Max Supply])`

        Returns:
            [type]: [description]
        """
        name = self.name
        asset_id = self.asset_id
        collection = self.collection.get_id()
        mint = self.get_mint()
        mint = "%s/%s (Max Supply: %s)" % tuple(mint)
        return "Asset " + asset_id + ": " + collection + " - " + name + " #" + mint


class Collection(AtomicBaseClass):
    """Class for instantizing Atomic Asset Collections"""

    def __init__(self, api_data):
        """Creates a Collection from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.collection_name

    def get_image(self):
        """Returns the primary image of the collection

        Returns:
            str: direct link to the image
        """
        if self.img is None:
            raise NoCollectionImageError
        return "https://ipfs.io/ipfs/" + self.img


class Schema(AtomicBaseClass):
    """Class for instantizing Atomic Asset Schemas"""

    def __init__(self, api_data):
        """Creates  Schema from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.schema_name


class Template(AtomicBaseClass):
    """Class for instantizing Atomic Asset Templates"""

    def __init__(self, api_data):
        """Creates a Template from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.template_id


class Offer(AtomicBaseClass):
    """Class for instantizing Atomic Asset Offer Data"""

    def __init__(self, api_data):
        """Creates an Offer data object from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.offer_id


class Transfer(AtomicBaseClass):
    """Class for instantizing Atomic Asset Transfer Data"""

    def __init__(self, api_data):
        """Creates a Transfer data object from API data

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        super().__init__(api_data)
        self.key = self.transfer_id

    def __str__(self):
        """Pretty prints Transfer information in the format
        `[DateAndTime]: [Sender] ---> [Recipient]`

        Args:
            api_data (dict): Data from the AtomicAssets API
        """
        when = datetime.fromtimestamp(float(self.created_at_time) / 1000).isoformat()
        sender = self.sender_name
        to = self.recipient_name
        return when + ": %s ---> %s" % (sender, to)


class Account:
    """Coming soon!"""

    pass
