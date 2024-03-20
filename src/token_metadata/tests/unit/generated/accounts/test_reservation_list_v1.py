from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.reservation_list_v1 import (
    PROGRAM_ID,
    ReservationListV1,
)
from src.token_metadata.generated.types.key import KeyKind
from src.token_metadata.generated.types.key import (
    ReservationListV1 as ReservationListV1Key,
)
from src.token_metadata.generated.types.reservation_v1 import ReservationV1


@pytest.mark.asyncio
async def test_reservation_list_v1_fetch_success(mocker: MockerFixture):
    mock_reservation_list = ReservationListV1(
        key=ReservationListV1Key(),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            ReservationV1(
                address=Pubkey.new_unique(), spots_remaining=10, total_spots=15
            )
        ],
    )
    mocker.patch.object(ReservationListV1, "decode", return_value=mock_reservation_list)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"reservation_list_v1_data",
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
    reservation_list = await ReservationListV1.fetch(mock_client, address)

    assert reservation_list == mock_reservation_list


@pytest.mark.asyncio
async def test_reservation_list_v1_fetch_multiple_success(mocker: MockerFixture):
    mock_lists = [
        ReservationListV1(
            key=ReservationListV1Key(),
            master_edition=Pubkey.new_unique(),
            supply_snapshot=None,
            reservations=[
                ReservationV1(
                    address=Pubkey.new_unique(), spots_remaining=10, total_spots=15
                )
            ],
        )
        for _ in range(2)
    ]
    mocker.patch.object(ReservationListV1, "decode", side_effect=mock_lists)

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
        "src.token_metadata.generated.accounts.reservation_list_v1.get_multiple_accounts",
        return_value=resp_items,
    )

    lists = await ReservationListV1.fetch_multiple(mock_client, addresses)
    assert len(lists) == len(mock_lists)


def test_reservation_list_v1_decode(mocker: MockerFixture):
    mocked_data = ReservationListV1(
        key=cast(KeyKind, ReservationListV1Key().to_encodable()),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            ReservationV1(
                address=Pubkey.new_unique(), spots_remaining=10, total_spots=15
            )
        ],
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.reservation_list_v1.ReservationListV1.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_list = ReservationListV1.decode(data_bytes)

    assert decoded_list.master_edition == mocked_data.master_edition
    assert decoded_list.supply_snapshot == mocked_data.supply_snapshot
    assert len(decoded_list.reservations) == len(mocked_data.reservations)


def test_reservation_list_v1_to_json():
    list_v1 = ReservationListV1(
        key=ReservationListV1Key(),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            ReservationV1(
                address=Pubkey.new_unique(), spots_remaining=10, total_spots=15
            )
        ],
    )

    json_data = list_v1.to_json()

    assert json_data["master_edition"] == str(list_v1.master_edition)
    assert json_data["supply_snapshot"] == list_v1.supply_snapshot
    assert len(json_data["reservations"]) == len(list_v1.reservations)


def test_reservation_list_v1_from_json():
    json_data = {
        "key": {"kind": "ReservationListV1"},
        "master_edition": str(Pubkey.new_unique()),
        "supply_snapshot": None,
        "reservations": [
            {
                "address": str(Pubkey.new_unique()),
                "spots_remaining": 10,
                "total_spots": 15,
            }
        ],
    }

    list_v1 = ReservationListV1.from_json(json_data)

    assert str(list_v1.master_edition) == json_data["master_edition"]
    assert list_v1.supply_snapshot == json_data["supply_snapshot"]
    assert len(list_v1.reservations) == len(json_data["reservations"])
