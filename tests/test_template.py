import requests
import datetime
import pytest
from pydantic.error_wrappers import ValidationError

from daltonapi.atomic import Asset, Template

sample_template_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/templates/tag/512726"
).json()['data']
sample_asset_data = requests.get(
    "https://aa.neftyblocks.com/atomicassets/v1/assets/1099765021842"
).json()['data']


class TestTemplate:
    """Tests the Template class"""

    def test_create_from_templates_endpoint(self):
        template = Template(**sample_template_data)
        assert template.collection.collection_name == "tag"
        assert template.immutable_data.get('name') == template.name == "Paintbrush of Creation: Larkhen"
        assert template.created_at_time == datetime.datetime.fromtimestamp(1652414497000/1000, tz = datetime.timezone.utc)
    
    def test_create_from_asset_reference(self):
        template = Asset(**sample_asset_data).template
        assert template.collection.collection_name == "tag"
        assert template.immutable_data.get('name') == template.name == "Paintbrush of Creation: Larkhen"
        assert template.created_at_time == datetime.datetime.fromtimestamp(1652414497000/1000, tz = datetime.timezone.utc)
        