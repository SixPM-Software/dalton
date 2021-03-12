from dalton import Atom

a = Atom()
c = a.get_asset("1099519071240")
a.get_asset_history(c)
a.get_assets(template=c.template)
print(c.get_image())
print(c.collection.get_image())
