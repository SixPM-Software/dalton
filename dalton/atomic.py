import json
from pathlib import Path
import requests
from atomic_errors import RequestFailedError, AssetIDError, NoFiltersError
from atomic_classes import *


class Atom():

	def __init__(self,endpoint="https://wax.api.atomicassets.io/atomicassets/v1/"):
		self.endpoint = endpoint

	def _query(self,endpoint: str):
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

	def _process_input(self,field):
		if field.__class__.__bases__[0] == AtomicBaseClass:
			field = field.get_id()
		return field

	def get_asset(self,asset: str):
		"""Gets an atomic asset from 

		Args:
			asset (str): [description]

		Raises:
			AssetIDError: [description]

		Returns:
			[type]: [description]
		"""		
		assert type(asset) == str, "Asset ID should be passed as a strpr"
		if not asset.isnumeric():
			raise AssetIDError(asset)
		data = self._query(self.endpoint + "assets/" + asset)
		return Asset(data)

	def get_assets(self,owner="",collection_name="",schema_name="",template_id=""):
		fields = {
			"owner":self._process_input(owner),
			"collection_name":self._process_input(collection_name),
			"schema_name":self._process_input(schema_name),
			"template_id":self._process_input(template_id),
		}
		for key in list(fields.keys()):
			if fields[key] == "":
				del fields[key]
		if not len(fields):
			raise NoFiltersError
		q = "&".join([key+"="+val for key,val in fields.items()])
		print(q)
		data = self._query(self.endpoint+"assets?"+q)
		return [Asset(nft) for nft in data]


	def get_assets_by_owner(self,owner:str):
		pass

		

a = Atom()
card = a.get_asset("1099519059528")