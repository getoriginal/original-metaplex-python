from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.edition_marker import (
    PROGRAM_ID,
    EditionMarker,
)
from src.token_metadata.generated.types.key import EditionMarker as EditionMarkerKey
from src.token_metadata.generated.types.key import KeyKind


@pytest.mark.asyncio
async def test_edition_marker_fetch_success(mocker: MockerFixture):
    mock_edition_marker = EditionMarker(key=EditionMarkerKey(), ledger=[0] * 31)
    mocker.patch.object(EditionMarker, "decode", return_value=mock_edition_marker)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"edition_marker_data",
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
    edition_marker = await EditionMarker.fetch(mock_client, address)

    assert edition_marker == mock_edition_marker


@pytest.mark.asyncio
async def test_edition_marker_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    edition_marker = await EditionMarker.fetch(mock_client, address)
    assert edition_marker is None


@pytest.mark.asyncio
async def test_edition_marker_fetch_multiple_success(mocker: MockerFixture):
    mock_edition_markers = [
        EditionMarker(key=EditionMarkerKey(), ledger=[1] * 31),
        EditionMarker(key=EditionMarkerKey(), ledger=[2] * 31),
    ]
    mocker.patch.object(EditionMarker, "decode", side_effect=mock_edition_markers)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    fake_account_infos = [
        AccountInfo(
            data=b"edition_marker_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(
            data=b"edition_marker_data_2",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
    ]

    resp_items = [
        _MultipleAccountsItem(pubkey=addresses[i], account=fake_account_infos[i])
        for i in range(len(addresses))
    ]
    mocker.patch(
        "src.token_metadata.generated.accounts.edition_marker.get_multiple_accounts",
        return_value=resp_items,
    )

    edition_markers = await EditionMarker.fetch_multiple(
        mock_client, addresses, commitment=None
    )
    assert len(edition_markers) == len(mock_edition_markers)


def test_edition_marker_decode(mocker: MockerFixture):
    mocked_parsed_data = EditionMarker(
        key=cast(KeyKind, EditionMarkerKey.to_encodable()), ledger=[42] * 31
    )
    mocker.patch(
        "src.token_metadata.generated.accounts.edition_marker.EditionMarker.layout.parse",
        return_value=mocked_parsed_data,
    )

    dummy_data = b"dummy_edition_marker_data"
    edition_marker = EditionMarker.decode(dummy_data)

    assert isinstance(edition_marker, EditionMarker)
    assert edition_marker.ledger == mocked_parsed_data.ledger


def test_edition_marker_to_json():
    edition_marker = EditionMarker(key=EditionMarkerKey(), ledger=[1, 2, 3] + [0] * 28)

    json_data = edition_marker.to_json()

    expected_json = {
        "key": {"kind": "EditionMarker"},
        "ledger": [1, 2, 3] + [0] * 28,
    }
    assert json_data == expected_json


def test_edition_marker_from_json():
    json_data = {
        "key": {"kind": "EditionMarker"},
        "ledger": [1, 2, 3] + [0] * 28,
    }

    edition_marker = EditionMarker.from_json(json_data)

    assert isinstance(edition_marker, EditionMarker)
    assert edition_marker.ledger == [1, 2, 3] + [0] * 28
