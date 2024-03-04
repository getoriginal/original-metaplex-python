from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.collection_authority_record import (
    PROGRAM_ID,
    CollectionAuthorityRecord,
)
from src.token_metadata.generated.types.key import (
    CollectionAuthorityRecord as CollectionAuthorityRecordKey,
)
from src.token_metadata.generated.types.key import KeyKind


@pytest.mark.asyncio
async def test_fetch_success(mocker: MockerFixture):
    mock_record = CollectionAuthorityRecord(
        key=CollectionAuthorityRecordKey(), bump=1, update_authority=Pubkey.new_unique()
    )
    mocker.patch.object(CollectionAuthorityRecord, "decode", return_value=mock_record)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"correctly_encoded_data",
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
    record = await CollectionAuthorityRecord.fetch(mock_client, address)

    assert record == mock_record
    mock_client.get_account_info.assert_awaited_with(address, commitment=None)


@pytest.mark.asyncio
async def test_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    record = await CollectionAuthorityRecord.fetch(mock_client, address)
    assert record is None


@pytest.mark.asyncio
async def test_fetch_multiple_success(mocker: MockerFixture):
    mock_records = [
        CollectionAuthorityRecord(
            key=CollectionAuthorityRecordKey(),
            bump=1,
            update_authority=Pubkey.new_unique(),
        ),
        CollectionAuthorityRecord(
            key=CollectionAuthorityRecordKey(),
            bump=2,
            update_authority=Pubkey.new_unique(),
        ),
    ]
    mocker.patch.object(CollectionAuthorityRecord, "decode", side_effect=mock_records)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    fake_account_infos = [
        AccountInfo(
            data=b"correctly_encoded_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(
            data=b"correctly_encoded_data_2",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
    ]
    resp_values = [
        _MultipleAccountsItem(pubkey=Pubkey.new_unique(), account=fake_account_info)
        for fake_account_info in fake_account_infos
    ]

    mock_get_multiple_accounts = mocker.patch(
        "src.token_metadata.generated.accounts.collection_authority_record.get_multiple_accounts",
        return_value=resp_values,
    )

    records = await CollectionAuthorityRecord.fetch_multiple(
        mock_client, addresses, commitment=None
    )
    assert len(records) == len(mock_records)
    mock_get_multiple_accounts.assert_called_once_with(
        mock_client, addresses, commitment=None
    )


def test_decode(mocker: MockerFixture):
    mocked_parsed_data = CollectionAuthorityRecord(
        key=cast(KeyKind, CollectionAuthorityRecordKey.to_encodable()),
        bump=42,
        update_authority=Pubkey.new_unique(),
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.collection_authority_record.CollectionAuthorityRecord.layout.parse",
        return_value=mocked_parsed_data,
    )

    dummy_data = b"dummy_data"
    record = CollectionAuthorityRecord.decode(dummy_data)

    assert isinstance(record.key, CollectionAuthorityRecordKey)
    assert record.bump == mocked_parsed_data.bump
    assert record.update_authority == mocked_parsed_data.update_authority


def test_collection_authority_record_to_json():
    test_pubkey = Pubkey.new_unique()
    record = CollectionAuthorityRecord(
        key=CollectionAuthorityRecordKey(), bump=1, update_authority=test_pubkey
    )

    json_data = record.to_json()

    expected_json = {
        "key": {"kind": "CollectionAuthorityRecord"},
        "bump": 1,
        "update_authority": str(test_pubkey),
    }
    assert json_data == expected_json


def test_collection_authority_record_from_json():
    test_pubkey_str = str(Pubkey.new_unique())
    json_data = {
        "key": {"kind": "CollectionAuthorityRecord"},
        "bump": 1,
        "update_authority": test_pubkey_str,
    }

    record = CollectionAuthorityRecord.from_json(json_data)

    assert isinstance(record.key, CollectionAuthorityRecordKey)
    assert record.bump == 1
    assert str(record.update_authority) == test_pubkey_str
