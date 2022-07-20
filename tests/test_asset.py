import requests

import pytest
from pydantic.error_wrappers import ValidationError

from daltonapi.atomic import Asset, Collection

sample_asset_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/assets/1099765021842"
).json()['data']

sample_transfer_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/transfers?asset_id=1099765021842"
).json()['data'][0]['assets'][0]

class TestAtom:
    """Tests the Atom class"""

    def test_create_from_asset_endpoint(self):
        asset = Asset(**sample_asset_data)
        assert asset.asset_id == 1099765021842
        assert asset.name == "Paintbrush of Creation: Larkhen", "Incorrect asset name"
        assert asset.template_mint == 13, "Template mint incorrect"
        assert asset.burned == False, "burned should return False"
        assert asset.data != {}, "No asset data field found"
        assert asset.data.get("element") == "Water"
    
    def test_create_from_transfer_reference(self):
        asset = Asset(**sample_transfer_data)
        assert asset.asset_id == 1099765021842
        assert asset.name == "Paintbrush of Creation: Larkhen", "Incorrect asset name"
        assert asset.template_mint == 13, "Template mint incorrect"
        assert asset.burned == False, "burned should return False"
        assert asset.data != {}, "No asset data field found"
        assert asset.data.get("element") == "Water"