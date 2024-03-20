from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.master_edition_v2 import (
    PROGRAM_ID,
    MasterEditionV2,
)
from src.token_metadata.generated.types.key import KeyKind
from src.token_metadata.generated.types.key import MasterEditionV2 as MasterEditionV2Key


@pytest.mark.asyncio
async def test_master_edition_v2_fetch_success(mocker: MockerFixture):
    mock_master_edition_v2 = MasterEditionV2(
        key=MasterEditionV2Key(),
        supply=100,
        max_supply=200,
    )
    mocker.patch.object(MasterEditionV2, "decode", return_value=mock_master_edition_v2)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"master_edition_v2_data",
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
    edition = await MasterEditionV2.fetch(mock_client, address)

    assert edition == mock_master_edition_v2


@pytest.mark.asyncio
async def test_master_edition_v2_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    edition = await MasterEditionV2.fetch(mock_client, address)
    assert edition is None


@pytest.mark.asyncio
async def test_master_edition_v2_fetch_wrong_program_id(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    wrong_program_id = Pubkey.new_unique()
    fake_account_info = Account(
        data=b"wrong_data",
        owner=wrong_program_id,
        lamports=0,
        executable=False,
        rent_epoch=0,
    )
    resp = GetAccountInfoResp(
        value=fake_account_info, context=RpcResponseContext(slot=0)
    )
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()

    mocker.patch.object(MasterEditionV2, "decode", return_value=None)

    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await MasterEditionV2.fetch(mock_client, address)


@pytest.mark.asyncio
async def test_master_edition_v2_fetch_multiple_success(mocker: MockerFixture):
    mock_master_editions_v2 = [
        MasterEditionV2(key=MasterEditionV2Key(), supply=100, max_supply=200),
        MasterEditionV2(
            key=MasterEditionV2Key(),
            supply=150,
            max_supply=None,
        ),
    ]
    mocker.patch.object(MasterEditionV2, "decode", side_effect=mock_master_editions_v2)

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
        "src.token_metadata.generated.accounts.master_edition_v2.get_multiple_accounts",
        return_value=resp_items,
    )

    editions = await MasterEditionV2.fetch_multiple(
        mock_client, addresses, commitment=None
    )
    assert len(editions) == len(mock_master_editions_v2)


@pytest.mark.asyncio
async def test_master_edition_v2_fetch_multiple_wrong_program_id(mocker: MockerFixture):
    mock_master_edition_v2 = MasterEditionV2(
        key=MasterEditionV2Key(), supply=100, max_supply=200
    )

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    wrong_program_id = (
        Pubkey.new_unique()
    )  # Simulate a different program ID for one account

    fake_account_infos = [
        AccountInfo(
            data=b"data_1", owner=PROGRAM_ID, lamports=0, executable=False, rent_epoch=0
        ),
        AccountInfo(
            data=b"wrong_data",
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
        "src.token_metadata.generated.accounts.master_edition_v2.get_multiple_accounts",
        return_value=resp_items,
    )

    mocker.patch.object(
        MasterEditionV2,
        "decode",
        side_effect=[
            lambda x: mock_master_edition_v2,
            ValueError("Account does not belong to this program"),
        ],
    )

    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await MasterEditionV2.fetch_multiple(mock_client, addresses, commitment=None)


def test_master_edition_v2_decode(mocker: MockerFixture):
    mocked_parsed_data = MasterEditionV2(
        key=cast(KeyKind, MasterEditionV2Key().to_encodable()), supply=0, max_supply=10
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.master_edition_v2.MasterEditionV2.layout.parse",
        return_value=mocked_parsed_data,
    )

    mock_data = b"mock_data"
    decoded_edition = MasterEditionV2.decode(mock_data)

    assert decoded_edition.supply == mocked_parsed_data.supply
    assert decoded_edition.max_supply == mocked_parsed_data.max_supply


def test_master_edition_v2_to_json():
    edition = MasterEditionV2(key=MasterEditionV2Key(), supply=100, max_supply=200)

    json_data = edition.to_json()

    assert json_data["supply"] == edition.supply
    assert json_data["max_supply"] == edition.max_supply


def test_master_edition_v2_from_json():
    json_data = {"key": {"kind": "MasterEditionV2"}, "supply": 100, "max_supply": 200}

    edition = MasterEditionV2.from_json(json_data)

    assert edition.supply == json_data["supply"]
    assert edition.max_supply == json_data["max_supply"]
