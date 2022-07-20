import requests
import pytest
from pydantic.error_wrappers import ValidationError

from daltonapi.atomic import Collection

sample_collection_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/collections/tag"
).json()['data']
sample_asset_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/assets/1099765021842"
).json()['data']['collection']


class TestCollection:
    """Tests the Atom class"""

    def test_init(self):
        collection = Collection(
            collection_name="tag",
            market_fee=0.1,
            author="me",
            created_at_time=1627366070000,
            created_at_block=1,
            allow_notify=True,
            authorized_accounts=[],
            notify_accounts=[]
        )
        assert collection.img == None
        assert collection.author == "me"
        # c = Asset(contract="testcontract", asset_id=1)
        # assert asset.contract == "testcontract"

    def test_create_from_collections_endpoint(self):
        collection = Collection(**sample_collection_data)
        assert collection.collection_name == "tag"
        assert collection.data.socials.get("discord") == "theadventurersguild"
    
    def test_create_from_asset_reference(self):
        collection = Collection(**sample_asset_data)
        assert collection.collection_name == "tag"
        assert collection.data.socials == {}
        