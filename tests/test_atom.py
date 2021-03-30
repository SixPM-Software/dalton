"""Tests for the Atom class"""
import pytest
from daltonapi.api import Atom
from daltonapi.tools.atomic_classes import Asset
from daltonapi.tools.atomic_errors import AtomicIDError, RequestFailedError


class TestAtom:
    """Tests the Atom class"""

    default_endpoint = "https://wax.api.atomicassets.io/atomicassets/v1/"

    def test_init(self):
        atom = Atom()
        assert atom.endpoint == self.default_endpoint

        atom = Atom("test_endpoint")
        assert atom.endpoint == "test_endpoint"

    def test_get_asset(self, atom: Atom):
        asset = atom.get_asset("1099518029159")
        assert isinstance(asset, Asset)

    def test_get_asset_typecheck(self, atom: Atom):
        with pytest.raises(AtomicIDError):
            atom.get_asset("")

        with pytest.raises(AtomicIDError):
            atom.get_asset("1te2st1")

        with pytest.raises(AtomicIDError):
            atom.get_asset("1.1")

        with pytest.raises(AtomicIDError):  # maybe this should be supported
            atom.get_asset(1)

    def test_get_asset_not_found(self, atom: Atom):
        with pytest.raises(RequestFailedError):
            atom.get_asset("0")
