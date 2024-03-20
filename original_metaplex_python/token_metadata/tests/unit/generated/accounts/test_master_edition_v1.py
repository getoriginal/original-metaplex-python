from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from original_metaplex_python.token_metadata.generated.accounts.master_edition_v1 import (
    PROGRAM_ID,
    MasterEditionV1,
)
from original_metaplex_python.token_metadata.generated.types.key import KeyKind
from original_metaplex_python.token_metadata.generated.types.key import (
    MasterEditionV1 as MasterEditionV1Key,
)


@pytest.mark.asyncio
async def test_master_edition_v1_fetch_success(mocker: MockerFixture):
    mock_master_edition_v1 = MasterEditionV1(
        key=MasterEditionV1Key(),
        supply=100,
        max_supply=200,
        printing_mint=Pubkey.new_unique(),
        one_time_printing_authorization_mint=Pubkey.new_unique(),
    )
    mocker.patch.object(MasterEditionV1, "decode", return_value=mock_master_edition_v1)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"master_edition_v1_data",
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
    edition = await MasterEditionV1.fetch(mock_client, address)

    assert edition == mock_master_edition_v1


@pytest.mark.asyncio
async def test_master_edition_v1_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    edition = await MasterEditionV1.fetch(mock_client, address)
    assert edition is None


@pytest.mark.asyncio
async def test_master_edition_v1_fetch_wrong_program_id(mocker: MockerFixture):
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

    mocker.patch.object(MasterEditionV1, "decode", return_value=None)

    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await MasterEditionV1.fetch(mock_client, address)


@pytest.mark.asyncio
async def test_master_edition_v1_fetch_multiple_success(mocker: MockerFixture):
    mock_master_editions_v1 = [
        MasterEditionV1(
            key=MasterEditionV1Key(),
            supply=100,
            max_supply=200,
            printing_mint=Pubkey.new_unique(),
            one_time_printing_authorization_mint=Pubkey.new_unique(),
        ),
        MasterEditionV1(
            key=MasterEditionV1Key(),
            supply=150,
            max_supply=None,
            printing_mint=Pubkey.new_unique(),
            one_time_printing_authorization_mint=Pubkey.new_unique(),
        ),
    ]
    mocker.patch.object(MasterEditionV1, "decode", side_effect=mock_master_editions_v1)

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
        "original_metaplex_python.token_metadata.generated.accounts.master_edition_v1.get_multiple_accounts",
        return_value=resp_items,
    )

    editions = await MasterEditionV1.fetch_multiple(
        mock_client, addresses, commitment=None
    )
    assert len(editions) == len(mock_master_editions_v1)


def test_master_edition_v1_decode(mocker: MockerFixture):
    mocked_parsed_data = MasterEditionV1(
        key=cast(KeyKind, MasterEditionV1Key().to_encodable()),
        supply=0,
        max_supply=10,
        printing_mint=Pubkey.new_unique(),
        one_time_printing_authorization_mint=Pubkey.new_unique(),
    )

    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.master_edition_v1.MasterEditionV1.layout.parse",
        return_value=mocked_parsed_data,
    )

    mock_data = b"mock_data"
    decoded_edition = MasterEditionV1.decode(mock_data)

    assert decoded_edition.supply == mocked_parsed_data.supply
    assert decoded_edition.max_supply == mocked_parsed_data.max_supply


def test_master_edition_v1_to_json():
    edition = MasterEditionV1(
        key=MasterEditionV1Key(),
        supply=100,
        max_supply=200,
        printing_mint=Pubkey.new_unique(),
        one_time_printing_authorization_mint=Pubkey.new_unique(),
    )

    json_data = edition.to_json()

    assert json_data["supply"] == edition.supply
    assert json_data["max_supply"] == edition.max_supply


def test_master_edition_v1_from_json():
    json_data = {
        "key": {"kind": "MasterEditionV1"},
        "supply": 100,
        "max_supply": 200,
        "printing_mint": str(Pubkey.new_unique()),
        "one_time_printing_authorization_mint": str(Pubkey.new_unique()),
    }

    edition = MasterEditionV1.from_json(json_data)

    assert edition.supply == json_data["supply"]
    assert edition.max_supply == json_data["max_supply"]
