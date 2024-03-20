from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from original_metaplex_python.token_metadata.generated.accounts.token_record import (
    PROGRAM_ID,
    TokenRecord,
)
from original_metaplex_python.token_metadata.generated.types.key import KeyKind
from original_metaplex_python.token_metadata.generated.types.key import (
    TokenRecord as TokenRecordKey,
)
from original_metaplex_python.token_metadata.generated.types.token_delegate_role import (
    TokenDelegateRoleKind,
    Transfer,
)
from original_metaplex_python.token_metadata.generated.types.token_state import (
    TokenStateKind,
    Unlocked,
)


@pytest.mark.asyncio
async def test_token_record_fetch_success(mocker: MockerFixture):
    mock_token_record = TokenRecord(
        key=TokenRecordKey(),
        bump=1,
        state=Unlocked(),
        rule_set_revision=1,
        delegate=Pubkey.new_unique(),
        delegate_role=Transfer(),
        locked_transfer=Pubkey.new_unique(),
    )
    mocker.patch.object(TokenRecord, "decode", return_value=mock_token_record)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"token_record_data",
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
    token_record = await TokenRecord.fetch(mock_client, address)

    assert token_record == mock_token_record


@pytest.mark.asyncio
async def test_token_record_fetch_multiple_success(mocker: MockerFixture):
    mock_records = [
        TokenRecord(
            key=TokenRecordKey(),
            bump=i,
            state=Unlocked(),
            rule_set_revision=i,
            delegate=Pubkey.new_unique(),
            delegate_role=Transfer(),
            locked_transfer=Pubkey.new_unique(),
        )
        for i in range(2)
    ]
    mocker.patch.object(TokenRecord, "decode", side_effect=mock_records)

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
        "original_metaplex_python.token_metadata.generated.accounts.token_record.get_multiple_accounts",
        return_value=resp_items,
    )

    records = await TokenRecord.fetch_multiple(mock_client, addresses)
    assert len(records) == len(mock_records)


def test_token_record_decode(mocker: MockerFixture):
    mocked_data = TokenRecord(
        key=cast(KeyKind, TokenRecordKey().to_encodable()),
        bump=1,
        state=cast(TokenStateKind, Unlocked().to_encodable()),
        rule_set_revision=1,
        delegate=Pubkey.new_unique(),
        delegate_role=cast(TokenDelegateRoleKind, Transfer().to_encodable()),
        locked_transfer=Pubkey.new_unique(),
    )

    mocker.patch(
        "original_metaplex_python.token_metadata.generated.accounts.token_record.TokenRecord.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_record = TokenRecord.decode(data_bytes)

    assert decoded_record.bump == mocked_data.bump
    assert decoded_record.delegate == mocked_data.delegate
    assert decoded_record.locked_transfer == mocked_data.locked_transfer


def test_token_record_to_json():
    record = TokenRecord(
        key=TokenRecordKey(),
        bump=1,
        state=Unlocked(),
        rule_set_revision=1,
        delegate=Pubkey.new_unique(),
        delegate_role=Transfer(),
        locked_transfer=Pubkey.new_unique(),
    )

    json_data = record.to_json()

    assert json_data["bump"] == record.bump
    assert json_data["state"] == record.state.to_json()
    assert json_data["delegate_role"] == record.delegate_role.to_json()


def test_token_record_from_json():
    json_data = {
        "key": {"kind": "TokenRecord"},
        "bump": 1,
        "state": {"kind": "Unlocked"},
        "rule_set_revision": 1,
        "delegate": str(Pubkey.new_unique()),
        "delegate_role": {"kind": "Transfer"},
        "locked_transfer": str(Pubkey.new_unique()),
    }

    record = TokenRecord.from_json(json_data)

    assert record.bump == json_data["bump"]
    assert record.rule_set_revision == json_data["rule_set_revision"]
    assert str(record.delegate) == json_data["delegate"]
