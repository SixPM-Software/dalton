# Asset, Collection, Schema, Templates, Offers, Transfers, Accounts,

class AtomicBaseClass():
	def __init__(self,api_data):
		for key in api_data:
			key,data = self._process_data(key,api_data[key])
			setattr(self, key, data)
		self.key = ""
		
	def _process_data(self,key:str,data:dict):
		"""function to intercept and construct classes

		Args:
			key (str): key to the dict

		Returns:
			dict or class object
		"""
		conversions = {
			"collection":Collection,
			"schema":Schema,
			"template":Template,
		}
		if key in conversions:
			data = conversions[key](data)
		return (key,data)

	def get_id(self):
		"""Returns the primary atomic assets identifier of the object
		E.g. For an asset, returns asset id. For a schema, returns schema name
		

		Returns:
			str: id
		"""		
		return self.key



class Asset(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.asset_id

	def get_mint(self):
		"""method to obtain mint information of the asset
		if max supply (list[2]) returns 0, there is no maximum limit
		Returns:
			list[int,int,int]: [mint number, total in circulation, max supply]
		"""		
		return [int(i) for i in [self.template_mint,self.template.issued_supply,self.template.max_supply]]

	def __str__(self):
		name = self.name
		asset_id = self.asset_id
		collection = self.collection.get_id()
		mint = self.get_mint()
		mint = "%s/%s (Max Supply: %s)"%tuple(mint)
		return "Asset " + asset_id + ": " + collection + " - " + name + " #" + mint

		
class Collection(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.collection_name


class Schema(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.schema_name

class Template(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.template_id
		
class Offer(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.offer_id

class Transfer(AtomicBaseClass):
	def __init__(self,api_data):
		super().__init__(api_data)
		self.key = self.transfer_id

class Account():
	pass

