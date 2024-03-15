from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.edition import PROGRAM_ID, Edition
from src.token_metadata.generated.types.key import EditionV1 as EditionKey
from src.token_metadata.generated.types.key import KeyKind


@pytest.mark.asyncio
async def test_edition_fetch_success(mocker: MockerFixture):
    mock_edition = Edition(key=EditionKey(), parent=Pubkey.new_unique(), edition=42)
    mocker.patch.object(Edition, "decode", return_value=mock_edition)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"edition_data",
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
    edition = await Edition.fetch(mock_client, address)

    assert edition == mock_edition
    mock_client.get_account_info.assert_called_with(address, commitment=None)


@pytest.mark.asyncio
async def test_edition_fetch_account_not_found(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    resp = GetAccountInfoResp(value=None, context=RpcResponseContext(slot=0))
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()
    edition = await Edition.fetch(mock_client, address)
    assert edition is None


@pytest.mark.asyncio
async def test_edition_fetch_wrong_program_id(mocker: MockerFixture):
    mock_client = mocker.Mock(spec=AsyncClient)
    wrong_program_id = Pubkey.new_unique()  # Simulate a different program ID
    fake_account_info = Account(
        data=b"some_data",
        owner=wrong_program_id,  # Owner is not the expected PROGRAM_ID
        lamports=0,
        executable=False,
        rent_epoch=0,
    )
    resp = GetAccountInfoResp(
        value=fake_account_info, context=RpcResponseContext(slot=0)
    )
    mocker.patch.object(mock_client, "get_account_info", return_value=resp)
    address = Pubkey.new_unique()

    # Since `fetch` is not an async method, we do not use await here.
    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await Edition.fetch(mock_client, address)


@pytest.mark.asyncio
async def test_edition_fetch_multiple_success(mocker: MockerFixture):
    mock_editions = [
        Edition(key=EditionKey(), parent=Pubkey.new_unique(), edition=1),
        Edition(key=EditionKey(), parent=Pubkey.new_unique(), edition=2),
    ]
    mocker.patch.object(Edition, "decode", side_effect=mock_editions)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    fake_account_infos = [
        AccountInfo(
            data=b"edition_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(
            data=b"edition_data_2",
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

    mocker.patch(
        "src.token_metadata.generated.accounts.edition.get_multiple_accounts",
        return_value=resp_values,
    )

    editions = await Edition.fetch_multiple(mock_client, addresses, commitment=None)
    assert len(editions) == len(mock_editions)


@pytest.mark.asyncio
async def test_edition_fetch_multiple_wrong_program_id(mocker: MockerFixture):
    mock_editions = [
        Edition(key=EditionKey(), parent=Pubkey.new_unique(), edition=1),
        Edition(key=EditionKey(), parent=Pubkey.new_unique(), edition=2),
    ]
    mocker.patch.object(Edition, "decode", side_effect=mock_editions)

    mock_client = mocker.Mock(spec=AsyncClient)
    addresses = [Pubkey.new_unique() for _ in range(2)]
    wrong_program_id = (
        Pubkey.new_unique()
    )  # Simulate a different program ID for the second account

    fake_account_infos = [
        AccountInfo(  # Correct program ID for the first account
            data=b"correctly_encoded_data_1",
            owner=PROGRAM_ID,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
        AccountInfo(  # Wrong program ID for the second account
            data=b"wrong_encoded_data_2",
            owner=wrong_program_id,
            lamports=0,
            executable=False,
            rent_epoch=0,
        ),
    ]

    resp_values = [
        _MultipleAccountsItem(pubkey=addresses[i], account=fake_account_infos[i])
        for i in range(len(fake_account_infos))
    ]

    mocker.patch(
        "src.token_metadata.generated.accounts.edition.get_multiple_accounts",
        return_value=resp_values,
    )

    with pytest.raises(ValueError, match="Account does not belong to this program"):
        await Edition.fetch_multiple(mock_client, addresses, commitment=None)


def test_edition_decode(mocker: MockerFixture):
    mocked_parsed_data = Edition(
        key=cast(KeyKind, EditionKey.to_encodable()),
        parent=Pubkey.new_unique(),
        edition=42,
    )
    mocker.patch(
        "src.token_metadata.generated.accounts.edition.Edition.layout.parse",
        return_value=mocked_parsed_data,
    )

    dummy_data = b"dummy_edition_data"
    edition = Edition.decode(dummy_data)

    assert isinstance(edition, Edition)
    assert edition.edition == mocked_parsed_data.edition


def test_edition_to_json():
    test_pubkey = Pubkey.new_unique()
    edition = Edition(key=EditionKey(), parent=test_pubkey, edition=1)

    json_data = edition.to_json()

    expected_json = {
        "key": {"kind": "EditionV1"},
        "parent": str(test_pubkey),
        "edition": 1,
    }
    assert json_data == expected_json


def test_edition_from_json():
    test_pubkey_str = str(Pubkey.new_unique())
    json_data = {
        "key": {"kind": "EditionV1"},
        "parent": test_pubkey_str,
        "edition": 1,
    }

    edition = Edition.from_json(json_data)

    assert isinstance(edition, Edition)
    assert edition.edition == 1
    assert str(edition.parent) == test_pubkey_str
