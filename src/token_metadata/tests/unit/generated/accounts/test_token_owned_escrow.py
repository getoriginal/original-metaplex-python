from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.token_owned_escrow import (
    PROGRAM_ID,
    TokenOwnedEscrow,
)
from src.token_metadata.generated.types.escrow_authority import (
    EscrowAuthorityKind,
    TokenOwner,
)
from src.token_metadata.generated.types.key import KeyKind
from src.token_metadata.generated.types.key import (
    TokenOwnedEscrow as TokenOwnedEscrowKey,
)


@pytest.mark.asyncio
async def test_token_owned_escrow_fetch_success(mocker: MockerFixture):
    mock_escrow = TokenOwnedEscrow(
        key=TokenOwnedEscrowKey(),
        base_token=Pubkey.new_unique(),
        authority=TokenOwner(),
        bump=1,
    )
    mocker.patch.object(TokenOwnedEscrow, "decode", return_value=mock_escrow)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"token_owned_escrow_data",
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
    escrow = await TokenOwnedEscrow.fetch(mock_client, address)

    assert escrow == mock_escrow


@pytest.mark.asyncio
async def test_token_owned_escrow_fetch_multiple_success(mocker: MockerFixture):
    mock_escrows = [
        TokenOwnedEscrow(
            key=TokenOwnedEscrowKey(),
            base_token=Pubkey.new_unique(),
            authority=TokenOwner(),
            bump=i,
        )
        for i in range(2)
    ]
    mocker.patch.object(TokenOwnedEscrow, "decode", side_effect=mock_escrows)

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
        "src.token_metadata.generated.accounts.token_owned_escrow.get_multiple_accounts",
        return_value=resp_items,
    )

    escrows = await TokenOwnedEscrow.fetch_multiple(mock_client, addresses)
    assert len(escrows) == len(mock_escrows)


def test_token_owned_escrow_decode(mocker: MockerFixture):
    mocked_data = TokenOwnedEscrow(
        key=cast(KeyKind, TokenOwnedEscrowKey().to_encodable()),
        base_token=Pubkey.new_unique(),
        authority=cast(EscrowAuthorityKind, TokenOwner().to_encodable()),
        bump=1,
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.token_owned_escrow.TokenOwnedEscrow.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_escrow = TokenOwnedEscrow.decode(data_bytes)

    assert decoded_escrow.bump == mocked_data.bump
    assert decoded_escrow.base_token == mocked_data.base_token
    assert decoded_escrow.authority.to_encodable() == mocked_data.authority


def test_token_owned_escrow_to_json():
    escrow = TokenOwnedEscrow(
        key=TokenOwnedEscrowKey(),
        base_token=Pubkey.new_unique(),
        authority=cast(EscrowAuthorityKind, TokenOwner()),
        bump=1,
    )

    json_data = escrow.to_json()

    assert json_data["bump"] == escrow.bump
    assert json_data["base_token"] == str(escrow.base_token)
    assert json_data["authority"] == escrow.authority.to_json()


def test_token_owned_escrow_from_json():
    json_data = {
        "key": {"kind": "TokenOwnedEscrow"},
        "base_token": str(Pubkey.new_unique()),
        "authority": {"kind": "TokenOwner"},
        "bump": 1,
    }

    escrow = TokenOwnedEscrow.from_json(json_data)

    assert escrow.bump == json_data["bump"]
    assert str(escrow.base_token) == json_data["base_token"]
    assert escrow.authority.to_json() == json_data["authority"]
