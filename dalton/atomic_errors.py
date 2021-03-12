class RequestFailedError(Exception):
	def __init__(self):
		self.message = "The request did not succeed."
	
	def __str__(self):
		return self.message

class AssetIDError(Exception):
	def __init__(self,asset_id):
		self.message = "Asset ID %s is invalid. The asset ID must be an integer."%asset_id

	def __str__(self):
		return self.message

class NoFiltersError(Exception):
	def __init__(self):
		self.message = "This method requires at least one argument"

	def __str__(self):
		return self.message