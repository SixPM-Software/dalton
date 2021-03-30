"""Test configuration"""
import pytest
from daltonapi.api import Atom


@pytest.fixture(scope="session")
def atom():
    return Atom()
