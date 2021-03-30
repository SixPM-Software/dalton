"""Test configuration"""
import pytest
from daltonapi.api import Atom
from daltonapi.tools.atomic_classes import Asset, Collection, Schema, Template


@pytest.fixture(scope="session")
def atom():
    return Atom()


@pytest.fixture(scope="session")
def asset():
    return Asset(api_data={"asset_id": "1099518029159"})


@pytest.fixture(scope="session")
def collection():
    return Collection(api_data={"collection_name": "gpk.topps"})


@pytest.fixture(scope="session")
def schema():
    return Schema(api_data={"schema_name": "series1"})


@pytest.fixture(scope="session")
def template():
    return Template(api_data={"template_id": "59492"})
