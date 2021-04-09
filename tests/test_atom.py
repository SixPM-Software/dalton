"""Tests for the Atom class"""
import pytest
from daltonapi.api import Atom
from daltonapi.tools.atomic_classes import Asset, Template, Collection, Schema, Transfer
from daltonapi.tools.atomic_errors import (
    AtomicIDError,
    RequestFailedError,
    NoFiltersError,
)

default_endpoint = "https://wax.api.atomicassets.io/atomicassets/v1/"
account = "atomicmarket"


class TestAtom:
    """Tests the Atom class"""

    def test_init(self):
        atom = Atom()
        assert atom.endpoint == default_endpoint

        atom = Atom("test_endpoint")
        assert atom.endpoint == "test_endpoint"

    class TestAtomGetAsset:
        def test_get_asset(self, atom: Atom, asset: Asset):
            result_asset = atom.get_asset(asset.get_id())
            assert isinstance(result_asset, Asset)
            assert result_asset == asset

        def test_get_asset_param_check(self, atom: Atom):
            with pytest.raises(AtomicIDError):
                atom.get_asset("")

            with pytest.raises(AtomicIDError):
                atom.get_asset("not numeric")

            with pytest.raises(AtomicIDError):
                atom.get_asset("1.1")

            with pytest.raises(AtomicIDError):  # maybe this should be supported
                atom.get_asset(1)

        def test_get_asset_not_found(self, atom: Atom):
            with pytest.raises(RequestFailedError):
                atom.get_asset("0")

    class TestAtomGetAssets:
        def test_get_assets_owner(self, atom: Atom):
            result = atom.get_assets(owner=account, limit=5)
            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], Asset)

        def test_get_assets_collection(self, atom: Atom, collection: Collection):
            result_class = atom.get_assets(collection=collection, limit=5)
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Asset)

            result_str = atom.get_assets(collection=collection.get_id(), limit=5)
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Asset)

            assert result_class == result_str

        def test_get_assets_schema(self, atom: Atom, schema: Schema):
            result_class = atom.get_assets(schema=schema, limit=5)
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Asset)

            result_str = atom.get_assets(schema=schema.get_id(), limit=5)
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Asset)

            assert result_class == result_str

        def test_get_assets_template(self, atom: Atom, template: Template):
            result_class = atom.get_assets(template=template, limit=5)
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Asset)

            result_str = atom.get_assets(template=template.get_id(), limit=5)
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Asset)

            result_int = atom.get_assets(template=int(template.get_id()), limit=5)
            assert isinstance(result_int, list)
            assert len(result_int) > 0
            assert isinstance(result_int[0], Asset)

            assert result_class == result_str == result_int

        def test_get_assets_param_check(self, atom: Atom):
            with pytest.raises(NoFiltersError):
                atom.get_assets()

        def test_get_assets_not_found(self, atom: Atom):
            result = atom.get_assets(owner="/")
            assert isinstance(result, list)
            assert len(result) == 0

        def test_get_assets_invalid_request(self, atom: Atom):
            with pytest.raises(RequestFailedError):
                atom.get_assets(template="failed")

    class TestAtomGetAssetHistory:
        def test_get_asset_history(self, atom: Atom, asset: Asset):
            result_class = atom.get_asset_history(asset)
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Transfer)

            result_str = atom.get_asset_history(asset.get_id())
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Transfer)

            assert result_class == result_str

        def test_get_asset_param_check(self, atom: Atom):
            with pytest.raises(AtomicIDError):
                atom.get_asset_history("fail")

        def test_get_asset_not_found(self, atom: Atom):
            result = atom.get_asset_history("0")
            assert isinstance(result, list)
            assert len(result) == 0

    class TestAtomGetCollection:
        def test_get_collection(self, atom: Atom, collection: Collection):
            result_collection = atom.get_collection(collection.get_id())
            assert isinstance(result_collection, Collection)
            assert result_collection == collection

        def test_get_collection_param_check(self, atom: Atom):
            with pytest.raises(AssertionError):
                atom.get_collection(1)

        def test_get_collection_not_found(self, atom: Atom):
            with pytest.raises(RequestFailedError):
                atom.get_collection("not valid id")

    class TestAtomGetTemplate:
        def test_get_template(
            self, atom: Atom, collection: Collection, template: Template
        ):
            result_template_class = atom.get_template(collection, template.get_id())
            assert isinstance(result_template_class, Template)
            assert result_template_class == template

            result_template_str = atom.get_template(
                collection.get_id(), template.get_id()
            )
            assert isinstance(result_template_str, Template)
            assert result_template_str == template

            assert result_template_class == result_template_str == template

        def test_get_template_param_check(self, atom: Atom):
            with pytest.raises(AssertionError):
                atom.get_template(123, 123)

            with pytest.raises(AtomicIDError):
                atom.get_template("123", "not numeric")

        def test_get_template_not_found(
            self, atom: Atom, collection: Collection, template: Template
        ):
            with pytest.raises(RequestFailedError):
                atom.get_template("invalid collection id", "0")

            with pytest.raises(RequestFailedError):
                atom.get_template("invalid collection id", template.get_id())

            with pytest.raises(RequestFailedError):
                atom.get_template(collection.get_id(), "0")

    class TestAtomGetSchema:
        def test_get_schema(self, atom: Atom, collection: Collection, schema: Schema):
            result_schema_class = atom.get_schema(collection, schema.get_id())
            assert isinstance(result_schema_class, Schema)
            assert result_schema_class == schema

            result_schema_str = atom.get_schema(collection.get_id(), schema.get_id())
            assert isinstance(result_schema_str, Schema)
            assert result_schema_str == schema

            assert result_schema_class == result_schema_str == schema

        def test_get_schema_param_check(self, atom: Atom):
            with pytest.raises(AssertionError):
                atom.get_schema(123, 123)

        def test_get_schema_not_found(
            self, atom: Atom, collection: Collection, schema: Schema
        ):
            with pytest.raises(RequestFailedError):
                atom.get_schema("invalid collection id", "invalid schema id")

            with pytest.raises(RequestFailedError):
                atom.get_schema("invalid collection id", schema.get_id())

            with pytest.raises(RequestFailedError):
                atom.get_schema(collection.get_id(), "0")

    class TestAtomGetTransfers:
        def test_get_transfers_sender(self, atom: Atom):
            result = atom.get_transfers(sender=account, limit=5)
            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], Transfer)

        def test_get_transfers_recipient(self, atom: Atom):
            result = atom.get_transfers(recipient=account, limit=5)
            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], Transfer)

        def test_get_transfers_collection(self, atom: Atom, collection: Collection):
            result_class = atom.get_transfers(
                sender=account, collection=collection, limit=5
            )
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Transfer)

            result_str = atom.get_transfers(
                sender=account, collection=collection.get_id(), limit=5
            )
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Transfer)

            assert result_class == result_str

        def test_get_transfers_schema(self, atom: Atom, schema: Schema):
            result_class = atom.get_transfers(sender=account, schema=schema, limit=5)
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Transfer)

            result_str = atom.get_transfers(
                sender=account, schema=schema.get_id(), limit=5
            )
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Transfer)

            assert result_class == result_str

        def test_get_transfers_template(self, atom: Atom, template: Template):
            result_class = atom.get_transfers(
                sender=account, template=template, limit=5
            )
            assert isinstance(result_class, list)
            assert len(result_class) > 0
            assert isinstance(result_class[0], Transfer)

            result_str = atom.get_transfers(
                sender=account, template=template.get_id(), limit=5
            )
            assert isinstance(result_str, list)
            assert len(result_str) > 0
            assert isinstance(result_str[0], Transfer)

            result_int = atom.get_transfers(
                sender=account, template=int(template.get_id()), limit=5
            )
            assert isinstance(result_int, list)
            assert len(result_int) > 0
            assert isinstance(result_int[0], Transfer)

            assert result_class == result_str == result_int

        def test_get_transfers_param_check(self, atom: Atom):
            with pytest.raises(AssertionError):
                atom.get_transfers()

            with pytest.raises(AssertionError):
                atom.get_transfers(
                    collection="missing", schema="sender and", template="recipient"
                )

        def test_get_transfers_not_found(self, atom: Atom):
            result = atom.get_transfers(sender="/", recipient="/")
            assert isinstance(result, list)
            assert len(result) == 0

        def test_get_transfers_invalid_request(self, atom: Atom):
            with pytest.raises(RequestFailedError):
                atom.get_transfers(sender="/", recipient="/", template="failed")
