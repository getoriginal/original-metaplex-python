from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from original_metaplex_python.token_metadata.generated.accounts.use_authority_record import (
    PROGRAM_ID,
    UseAuthorityRecord,
)
from original_metaplex_python.token_metadata.generated.types.key import KeyKind
from original_metaplex_python.token_metadata.generated.types.key import (
    UseAuthorityRecord as UseAuthorityRecordKey,
)


@pytest.mark.asyncio
async def test_use_authority_record_fetch_success(mocker: MockerFixture):
    mock_use_authority_record = UseAuthorityRecord(
        key=UseAuthorityRecordKey(),
        allowed_uses=10,
        bump=1,
    )
    mocker.patch.object(
        UseAuthorityRecord, "decode", return_value=mock_use_authority_record
    )

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"use_authority_record_data",
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
    use_authority_record = await UseAuthorityRecord.fetch(mock_client, address)

    assert use_authority_record == mock_use_authority_record


@pytest.mark.asyncio
async def test_use_authority_record_fetch_multiple_success(mocker: MockerFixture):
    mock_records = [
        UseAuthorityRecord(
            key=UseAuthorityRecordKey(),
            allowed_uses=10,
            bump=1,
        )
        for _ in range(2)
    ]
    mocker.patch.object(UseAuthorityRecord, "decode", side_effect=mock_records)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    account_info_list = [
        AccountInfo(
            data=b"data_1", owner=PROGRAM_ID, lamports=0, executable=False, rent_epoch=0
        ),
        AccountInfo(
            data=b"data_2", owner=PROGRAM_ID, lamports=0, executable=False, rent_epoch=0
        ),
    ]

    resp_items = [
        _MultipleAccountsItem(pubkey=addresses[i], account=account_info_list[i])
        for i in range(len(addresses))
    ]
    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.use_authority_record.get_multiple_accounts",
        return_value=resp_items,
    )

    records = await UseAuthorityRecord.fetch_multiple(mock_client, addresses)
    assert len(records) == len(mock_records)


def test_use_authority_record_decode(mocker: MockerFixture):
    mocked_data = UseAuthorityRecord(
        key=cast(KeyKind, UseAuthorityRecordKey().to_encodable()),
        allowed_uses=10,
        bump=1,
    )

    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.use_authority_record.UseAuthorityRecord.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_record = UseAuthorityRecord.decode(data_bytes)

    assert decoded_record.allowed_uses == mocked_data.allowed_uses
    assert decoded_record.bump == mocked_data.bump


def test_use_authority_record_to_json():
    record = UseAuthorityRecord(
        key=UseAuthorityRecordKey(),
        allowed_uses=10,
        bump=1,
    )

    json_data = record.to_json()

    assert json_data["allowed_uses"] == record.allowed_uses
    assert json_data["bump"] == record.bump


def test_use_authority_record_from_json():
    json_data = {
        "key": {"kind": "UseAuthorityRecord"},
        "allowed_uses": 10,
        "bump": 1,
    }

    record = UseAuthorityRecord.from_json(json_data)

    assert record.allowed_uses == json_data["allowed_uses"]
    assert record.bump == json_data["bump"]
