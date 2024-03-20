from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from original_metaplex_python.token_metadata.generated.accounts.metadata import (
    PROGRAM_ID,
    Metadata,
)
from original_metaplex_python.token_metadata.generated.types import Creator
from original_metaplex_python.token_metadata.generated.types.data import Data
from original_metaplex_python.token_metadata.generated.types.key import KeyKind
from original_metaplex_python.token_metadata.generated.types.key import (
    MetadataV1 as MetadataV1Key,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    NonFungible,
    TokenStandardKind,
)


@pytest.mark.asyncio
async def test_metadata_fetch_success(mocker: MockerFixture):
    mock_metadata = Metadata(
        key=MetadataV1Key(),
        update_authority=Pubkey.new_unique(),
        mint=Pubkey.new_unique(),
        data=Data(
            name="Example NFT",
            symbol="EXMPL",
            uri="https://example.com/nft",
            seller_fee_basis_points=500,
            creators=[Creator(address=Pubkey.new_unique(), verified=True, share=100)],
        ),
        primary_sale_happened=True,
        is_mutable=False,
        edition_nonce=None,
        token_standard=NonFungible(),
        collection=None,
        uses=None,
        collection_details=None,
        programmable_config=None,
    )
    mocker.patch.object(Metadata, "decode", return_value=mock_metadata)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"metadata_data",
        owner=PROGRAM_ID,
        lamports=0,
        executable=False,
        rent_epoch=0,
    )
    resp = GetAccountInfoResp(
        value=fake_account_info, context=RpcResponseContext(slot=0)
    )
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    metadata = await Metadata.fetch(mock_client, address)

    assert metadata == mock_metadata


@pytest.mark.asyncio
async def test_metadata_fetch_sync_success(mocker: MockerFixture):
    mock_metadata = Metadata(
        key=MetadataV1Key(),
        update_authority=Pubkey.new_unique(),
        mint=Pubkey.new_unique(),
        data=Data(
            name="Example NFT",
            symbol="EXMPL",
            uri="https://example.com/nft",
            seller_fee_basis_points=500,
            creators=[Creator(address=Pubkey.new_unique(), verified=True, share=100)],
        ),
        primary_sale_happened=True,
        is_mutable=False,
        edition_nonce=None,
        token_standard=NonFungible(),
        collection=None,
        uses=None,
        collection_details=None,
        programmable_config=None,
    )
    mocker.patch.object(Metadata, "decode", return_value=mock_metadata)

    mock_client = mocker.Mock(spec=Client)
    fake_account_info = Account(
        data=b"metadata_data_sync",
        owner=PROGRAM_ID,
        lamports=0,
        executable=False,
        rent_epoch=0,
    )
    resp = GetAccountInfoResp(
        value=fake_account_info, context=RpcResponseContext(slot=0)
    )
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    metadata = Metadata.fetch_sync(mock_client, address)

    assert metadata == mock_metadata


@pytest.mark.asyncio
async def test_metadata_fetch_multiple_success(mocker: MockerFixture):
    mock_metadatas = [
        Metadata(
            key=MetadataV1Key(),
            update_authority=Pubkey.new_unique(),
            mint=Pubkey.new_unique(),
            data=Data(
                name="Example NFT",
                symbol="EXMPL",
                uri="https://example.com/nft",
                seller_fee_basis_points=500,
                creators=[
                    Creator(address=Pubkey.new_unique(), verified=True, share=100)
                ],
            ),
            primary_sale_happened=True,
            is_mutable=False,
            edition_nonce=None,
            token_standard=NonFungible(),
            collection=None,
            uses=None,
            collection_details=None,
            programmable_config=None,
        )
        for _ in range(2)
    ]
    mocker.patch.object(Metadata, "decode", side_effect=mock_metadatas)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    fake_account_infos = [
        AccountInfo(
            data=b"data_1", owner=PROGRAM_ID, lamports=0, executable=False, rent_epoch=0
        ),
        AccountInfo(
            data=b"data_2", owner=PROGRAM_ID, lamports=0, executable=False, rent_epoch=0
        ),
    ]

    resp_items = [
        _MultipleAccountsItem(pubkey=addresses[i], account=fake_account_infos[i])
        for i in range(len(addresses))
    ]
    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.metadata.get_multiple_accounts",
        return_value=resp_items,
    )

    metadatas = await Metadata.fetch_multiple(mock_client, addresses, commitment=None)
    assert len(metadatas) == len(mock_metadatas)


def test_metadata_decode(mocker: MockerFixture):
    mocked_parsed_data = Metadata(
        key=cast(KeyKind, MetadataV1Key().to_encodable()),
        update_authority=Pubkey.new_unique(),
        mint=Pubkey.new_unique(),
        data=Data(
            name="Example NFT",
            symbol="EXMPL",
            uri="https://example.com/nft",
            seller_fee_basis_points=500,
            creators=[Creator(address=Pubkey.new_unique(), verified=True, share=100)],
        ),
        primary_sale_happened=True,
        is_mutable=False,
        edition_nonce=None,
        token_standard=cast(TokenStandardKind, NonFungible().to_encodable()),
        collection=None,
        uses=None,
        collection_details=None,
        programmable_config=None,
    )

    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.metadata.Metadata.layout.parse",
        return_value=mocked_parsed_data,
    )

    mock_data = b"mock_data"
    decoded_metadata = Metadata.decode(mock_data)

    assert decoded_metadata.key.to_encodable() == mocked_parsed_data.key
    assert decoded_metadata.update_authority == mocked_parsed_data.update_authority
    assert decoded_metadata.mint == mocked_parsed_data.mint
    assert decoded_metadata.data.name == mocked_parsed_data.data.name
    assert decoded_metadata.data.symbol == mocked_parsed_data.data.symbol
    assert decoded_metadata.data.uri == mocked_parsed_data.data.uri
    assert (
        decoded_metadata.data.seller_fee_basis_points
        == mocked_parsed_data.data.seller_fee_basis_points
    )
    assert decoded_metadata.data.creators == mocked_parsed_data.data.creators
    assert (
        decoded_metadata.primary_sale_happened
        == mocked_parsed_data.primary_sale_happened
    )
    assert decoded_metadata.is_mutable == mocked_parsed_data.is_mutable
    assert decoded_metadata.edition_nonce == mocked_parsed_data.edition_nonce
    assert isinstance(decoded_metadata.token_standard, NonFungible)
    assert decoded_metadata.collection == mocked_parsed_data.collection
    assert decoded_metadata.uses == mocked_parsed_data.uses
    assert decoded_metadata.collection_details == mocked_parsed_data.collection_details
    assert (
        decoded_metadata.programmable_config == mocked_parsed_data.programmable_config
    )


def test_metadata_to_json():
    metadata = Metadata(
        key=MetadataV1Key(),
        update_authority=Pubkey.new_unique(),
        mint=Pubkey.new_unique(),
        data=Data(
            name="Example NFT",
            symbol="EXMPL",
            uri="https://example.com/nft",
            seller_fee_basis_points=500,
            creators=[Creator(address=Pubkey.new_unique(), verified=True, share=100)],
        ),
        primary_sale_happened=True,
        is_mutable=False,
        edition_nonce=None,
        token_standard=NonFungible(),
        collection=None,
        uses=None,
        collection_details=None,
        programmable_config=None,
    )

    json_data = metadata.to_json()

    assert json_data["key"]["kind"] == "MetadataV1"
    assert json_data["update_authority"] == str(metadata.update_authority)
    assert json_data["mint"] == str(metadata.mint)
    assert json_data["data"]["name"] == metadata.data.name
    assert json_data["data"]["symbol"] == metadata.data.symbol
    assert json_data["data"]["uri"] == metadata.data.uri
    assert (
        json_data["data"]["seller_fee_basis_points"]
        == metadata.data.seller_fee_basis_points
    )
    for i, creator in enumerate(json_data["data"]["creators"]):
        assert creator["address"] == str(metadata.data.creators[i].address)
        assert creator["verified"] == metadata.data.creators[i].verified
        assert creator["share"] == metadata.data.creators[i].share
    assert json_data["primary_sale_happened"] == metadata.primary_sale_happened
    assert json_data["is_mutable"] == metadata.is_mutable
    assert json_data["edition_nonce"] == metadata.edition_nonce
    assert json_data["token_standard"]["kind"] == "NonFungible"
    assert json_data.get("collection") is None
    assert json_data.get("uses") is None
    assert json_data.get("collection_details") is None
    assert json_data.get("programmable_config") is None


def test_metadata_from_json():
    json_data = {
        "key": {"kind": "MetadataV1"},
        "update_authority": str(Pubkey.new_unique()),
        "mint": str(Pubkey.new_unique()),
        "data": {
            "name": "Example NFT",
            "symbol": "EXMPL",
            "uri": "https://example.com/nft",
            "seller_fee_basis_points": 500,
            "creators": [
                {"address": str(Pubkey.new_unique()), "verified": True, "share": 100}
            ],
        },
        "primary_sale_happened": True,
        "is_mutable": False,
        "edition_nonce": None,
        "token_standard": {"kind": "NonFungible"},
        "collection": None,
        "uses": None,
        "collection_details": None,
        "programmable_config": None,
    }

    metadata = Metadata.from_json(json_data)

    assert str(metadata.key.kind) == json_data["key"]["kind"]
    assert str(metadata.update_authority) == json_data["update_authority"]
    assert str(metadata.mint) == json_data["mint"]
    assert metadata.data.name == json_data["data"]["name"]
    assert metadata.data.symbol == json_data["data"]["symbol"]
    assert metadata.data.uri == json_data["data"]["uri"]
    assert (
        metadata.data.seller_fee_basis_points
        == json_data["data"]["seller_fee_basis_points"]
    )
    for i, creator_json in enumerate(json_data["data"]["creators"]):
        assert str(metadata.data.creators[i].address) == creator_json["address"]
        assert metadata.data.creators[i].verified == creator_json["verified"]
        assert metadata.data.creators[i].share == creator_json["share"]

    assert metadata.primary_sale_happened == json_data["primary_sale_happened"]
    assert metadata.is_mutable == json_data["is_mutable"]
    assert metadata.edition_nonce == json_data["edition_nonce"]
    assert metadata.token_standard.kind == json_data["token_standard"]["kind"]
    assert metadata.collection is None
    assert metadata.uses is None
    assert metadata.collection_details is None
    assert metadata.programmable_config is None
