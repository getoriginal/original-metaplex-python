from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.metadata_delegate_record import (
    PROGRAM_ID,
    MetadataDelegateRecord,
)
from src.token_metadata.generated.types.key import KeyKind
from src.token_metadata.generated.types.key import (
    MetadataDelegate as MetadataDelegateKey,
)


@pytest.mark.asyncio
async def test_metadata_delegate_record_fetch_success(mocker: MockerFixture):
    mock_delegate_record = MetadataDelegateRecord(
        key=MetadataDelegateKey(),
        bump=1,
        mint=Pubkey.new_unique(),
        delegate=Pubkey.new_unique(),
        update_authority=Pubkey.new_unique(),
    )
    mocker.patch.object(
        MetadataDelegateRecord, "decode", return_value=mock_delegate_record
    )

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"metadata_delegate_record_data",
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
    delegate_record = await MetadataDelegateRecord.fetch(mock_client, address)

    assert delegate_record == mock_delegate_record


@pytest.mark.asyncio
async def test_metadata_delegate_record_fetch_multiple_success(mocker: MockerFixture):
    mock_records = [
        MetadataDelegateRecord(
            key=MetadataDelegateKey(),
            bump=i,
            mint=Pubkey.new_unique(),
            delegate=Pubkey.new_unique(),
            update_authority=Pubkey.new_unique(),
        )
        for i in range(2)
    ]
    mocker.patch.object(MetadataDelegateRecord, "decode", side_effect=mock_records)

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
        "src.token_metadata.generated.accounts.metadata_delegate_record.get_multiple_accounts",
        return_value=resp_items,
    )

    records = await MetadataDelegateRecord.fetch_multiple(mock_client, addresses)
    assert len(records) == len(mock_records)


def test_metadata_delegate_record_decode(mocker: MockerFixture):
    mocked_data = MetadataDelegateRecord(
        key=cast(KeyKind, MetadataDelegateKey().to_encodable()),
        bump=1,
        mint=Pubkey.new_unique(),
        delegate=Pubkey.new_unique(),
        update_authority=Pubkey.new_unique(),
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.metadata_delegate_record.MetadataDelegateRecord.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_data = MetadataDelegateRecord.decode(data_bytes)

    assert decoded_data.bump == mocked_data.bump
    assert decoded_data.mint == mocked_data.mint
    assert decoded_data.delegate == mocked_data.delegate
    assert decoded_data.update_authority == mocked_data.update_authority


def test_metadata_delegate_record_to_json():
    record = MetadataDelegateRecord(
        key=MetadataDelegateKey(),
        bump=1,
        mint=Pubkey.new_unique(),
        delegate=Pubkey.new_unique(),
        update_authority=Pubkey.new_unique(),
    )

    json_data = record.to_json()

    assert json_data["bump"] == record.bump
    assert json_data["mint"] == str(record.mint)
    assert json_data["delegate"] == str(record.delegate)
    assert json_data["update_authority"] == str(record.update_authority)


def test_metadata_delegate_record_from_json():
    json_data = {
        "key": {"kind": "MetadataDelegate"},
        "bump": 1,
        "mint": str(Pubkey.new_unique()),
        "delegate": str(Pubkey.new_unique()),
        "update_authority": str(Pubkey.new_unique()),
    }

    record = MetadataDelegateRecord.from_json(json_data)

    assert record.bump == json_data["bump"]
    assert str(record.mint) == json_data["mint"]
    assert str(record.delegate) == json_data["delegate"]
    assert str(record.update_authority) == json_data["update_authority"]
