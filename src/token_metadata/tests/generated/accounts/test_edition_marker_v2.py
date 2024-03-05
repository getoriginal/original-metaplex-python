from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.edition_marker_v2 import (
    PROGRAM_ID,
    EditionMarkerV2,
)
from src.token_metadata.generated.types.key import EditionMarkerV2 as EditionMarkerV2Key
from src.token_metadata.generated.types.key import KeyKind


@pytest.mark.asyncio
async def test_edition_marker_v2_fetch_success(mocker: MockerFixture):
    mock_edition_marker_v2 = EditionMarkerV2(
        key=EditionMarkerV2Key(), ledger=bytes([0] * 31)
    )
    mocker.patch.object(EditionMarkerV2, "decode", return_value=mock_edition_marker_v2)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"edition_marker_v2_data",
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
    edition_marker_v2 = await EditionMarkerV2.fetch(mock_client, address)

    assert edition_marker_v2 == mock_edition_marker_v2


@pytest.mark.asyncio
async def test_edition_marker_v2_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    edition_marker_v2 = await EditionMarkerV2.fetch(mock_client, address)
    assert edition_marker_v2 is None


@pytest.mark.asyncio
async def test_edition_marker_v2_fetch_multiple_success(mocker: MockerFixture):
    mock_edition_markers_v2 = [
        EditionMarkerV2(key=EditionMarkerV2Key(), ledger=bytes([1] * 31)),
        EditionMarkerV2(key=EditionMarkerV2Key(), ledger=bytes([2] * 31)),
    ]
    mocker.patch.object(EditionMarkerV2, "decode", side_effect=mock_edition_markers_v2)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    fake_account_infos = [
        AccountInfo(
            data=b"edition_marker_v2_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(
            data=b"edition_marker_v2_data_2",
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
        "src.token_metadata.generated.accounts.edition_marker_v2.get_multiple_accounts",
        return_value=resp_items,
    )

    edition_markers_v2 = await EditionMarkerV2.fetch_multiple(
        mock_client, addresses, commitment=None
    )
    assert len(edition_markers_v2) == len(mock_edition_markers_v2)


@pytest.mark.asyncio
async def test_edition_marker_v2_fetch_multiple_wrong_program_id(mocker: MockerFixture):
    mock_edition_marker_v2 = EditionMarkerV2(
        key=EditionMarkerV2Key(), ledger=bytes([1] * 31)
    )

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    wrong_program_id = Pubkey.new_unique()

    fake_account_infos = [
        AccountInfo(
            data=b"edition_marker_v2_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(
            data=b"wrong_edition_marker_v2_data",
            owner=wrong_program_id,
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
        "src.token_metadata.generated.accounts.edition_marker_v2.get_multiple_accounts",
        return_value=resp_items,
    )

    mocker.patch.object(
        EditionMarkerV2,
        "decode",
        side_effect=[
            lambda x: mock_edition_marker_v2,
            ValueError("Account does not belong to this program"),
        ],
    )

    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await EditionMarkerV2.fetch_multiple(mock_client, addresses, commitment=None)


def test_edition_marker_v2_decode(mocker: MockerFixture):
    mocked_parsed_data = EditionMarkerV2(
        key=cast(KeyKind, EditionMarkerV2Key.to_encodable()), ledger=bytes([42] * 31)
    )
    mocker.patch(
        "src.token_metadata.generated.accounts.edition_marker_v2.EditionMarkerV2.layout.parse",
        return_value=mocked_parsed_data,
    )

    dummy_data = b"dummy_edition_marker_v2_data"
    edition_marker_v2 = EditionMarkerV2.decode(dummy_data)

    assert isinstance(edition_marker_v2, EditionMarkerV2)
    assert edition_marker_v2.ledger == mocked_parsed_data.ledger


def test_edition_marker_v2_to_json():
    edition_marker_v2 = EditionMarkerV2(
        key=EditionMarkerV2Key(), ledger=bytes([1, 2, 3] + [0] * 28)
    )
    json_data = edition_marker_v2.to_json()

    expected_json = {
        "key": {"kind": "EditionMarkerV2"},
        "ledger": [1, 2, 3] + [0] * 28,
    }
    assert json_data == expected_json


def test_edition_marker_v2_from_json():
    json_data = {
        "key": {"kind": "EditionMarkerV2"},
        "ledger": [1, 2, 3] + [0] * 28,
    }

    edition_marker_v2 = EditionMarkerV2.from_json(json_data)

    assert isinstance(edition_marker_v2, EditionMarkerV2)
    assert edition_marker_v2.ledger == bytes([1, 2, 3] + [0] * 28)
