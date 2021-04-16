"""Classes for the WAX chain API

Uses other endpoints for more information
"""

class WaxBaseClass:
    """Template class for WAX API data"""

    def __init__(self, api_data):
        """Creates the WAX Object

        Args:
            api_data (dict): Data from the WAX API
        """
        for key, val in api_data.items():
            # key, data = self._process_data(key, api_data[key])
            setattr(self, "_" + key, val)
        self.key = ""

    # def _process_data(self, key: str, data: dict):
    #     """function to intercept and construct classes

    #     Args:
    #             key (str): key to the dict

    #     Returns:
    #             dict or class object
    #     """
    #     conversions = {
    #         "collection": Collection,
    #         "schema": Schema,
    #         "template": Template,
    #     }
    #     if key in conversions and data is not None:
    #         data = conversions[key](data)
    #     return (key, data)

    def get_id(self):
        """Returns the primary atomic assets identifier of the object
        E.g. For an asset, returns asset id. For a schema, returns schema name


        Returns:
                str: id
        """
        return self.key


class Account(WaxBaseClass):
    """Class for WAX accounts"""

    def __init__(self, api_data: dict):
        super().__init__(api_data)
        self.key = self._account_name

    @property
    def balance(self):
        """Returns liquid balance of account

        Returns:
            float: Liquid Balance
        """
        bal = float(self._core_liquid_balance.rstrip(" WAX"))
        return bal

    @property
    def staked_balance(self):
        """Returns staked balance

        Returns:
            dict: {"cpu":float,"net":float}
        """
        resources = self._total_resources
        net = float(resources["net_weight"].rstrip(" WAX"))
        cpu = float(resources["cpu_weight"].rstrip(" WAX"))
        return {"cpu": cpu, "net": net}

    @property
    def total_balance(self):
        """Returns total account balance

        Returns:
            float: Total account balance in WAX
        """
        staked = self.staked_balance
        return self.balance + staked["cpu"] + staked["net"]
