from typing import cast

import pytest
from anchorpy.utils.rpc import AccountInfo, _MultipleAccountsItem
from pytest_mock import MockerFixture
from solana.rpc.async_api import AsyncClient
from solders.account import Account
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp, RpcResponseContext

from src.token_metadata.generated.accounts.reservation_list_v2 import (
    PROGRAM_ID,
    ReservationListV2,
)
from src.token_metadata.generated.types.key import KeyKind
from src.token_metadata.generated.types.key import (
    ReservationListV2 as ReservationListV2Key,
)
from src.token_metadata.generated.types.reservation import Reservation


@pytest.mark.asyncio
async def test_reservation_list_v2_fetch_success(mocker: MockerFixture):
    mock_reservation_list = ReservationListV2(
        key=ReservationListV2Key(),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            Reservation(
                address=Pubkey.new_unique(), spots_remaining=100, total_spots=150
            )
        ],
        total_reservation_spots=100,
        current_reservation_spots=50,
    )
    mocker.patch.object(ReservationListV2, "decode", return_value=mock_reservation_list)

    mock_client = mocker.Mock(spec=AsyncClient)
    fake_account_info = Account(
        data=b"reservation_list_v2_data",
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
    reservation_list = await ReservationListV2.fetch(mock_client, address)

    assert reservation_list == mock_reservation_list


@pytest.mark.asyncio
async def test_reservation_list_v2_fetch_multiple_success(mocker: MockerFixture):
    mock_lists = [
        ReservationListV2(
            key=ReservationListV2Key(),
            master_edition=Pubkey.new_unique(),
            supply_snapshot=None,
            reservations=[
                Reservation(
                    address=Pubkey.new_unique(), spots_remaining=100, total_spots=150
                )
            ],
            total_reservation_spots=100,
            current_reservation_spots=50,
        )
        for _ in range(2)
    ]
    mocker.patch.object(ReservationListV2, "decode", side_effect=mock_lists)

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
        "src.token_metadata.generated.accounts.reservation_list_v2.get_multiple_accounts",
        return_value=resp_items,
    )

    lists = await ReservationListV2.fetch_multiple(mock_client, addresses)
    assert len(lists) == len(mock_lists)


def test_reservation_list_v2_decode(mocker: MockerFixture):
    mocked_data = ReservationListV2(
        key=cast(KeyKind, ReservationListV2Key().to_encodable()),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            Reservation(
                address=Pubkey.new_unique(), spots_remaining=100, total_spots=150
            )
        ],
        total_reservation_spots=100,
        current_reservation_spots=50,
    )

    mocker.patch(
        "src.token_metadata.generated.accounts.reservation_list_v2.ReservationListV2.layout.parse",
        return_value=mocked_data,
    )

    data_bytes = b"some_bytes"
    decoded_list = ReservationListV2.decode(data_bytes)

    assert decoded_list.total_reservation_spots == mocked_data.total_reservation_spots
    assert (
        decoded_list.current_reservation_spots == mocked_data.current_reservation_spots
    )
    assert len(decoded_list.reservations) == len(mocked_data.reservations)


def test_reservation_list_v2_to_json():
    list_v2 = ReservationListV2(
        key=ReservationListV2Key(),
        master_edition=Pubkey.new_unique(),
        supply_snapshot=None,
        reservations=[
            Reservation(
                address=Pubkey.new_unique(), spots_remaining=100, total_spots=150
            )
        ],
        total_reservation_spots=100,
        current_reservation_spots=50,
    )

    json_data = list_v2.to_json()

    assert json_data["total_reservation_spots"] == list_v2.total_reservation_spots
    assert json_data["current_reservation_spots"] == list_v2.current_reservation_spots
    assert len(json_data["reservations"]) == len(list_v2.reservations)


def test_reservation_list_v2_from_json():
    json_data = {
        "key": {"kind": "ReservationListV2"},
        "master_edition": str(Pubkey.new_unique()),
        "supply_snapshot": None,
        "reservations": [
            {
                "address": str(Pubkey.new_unique()),
                "spots_remaining": 100,
                "total_spots": 150,
            }
        ],
        "total_reservation_spots": 100,
        "current_reservation_spots": 50,
    }

    list_v2 = ReservationListV2.from_json(json_data)

    assert list_v2.total_reservation_spots == json_data["total_reservation_spots"]
    assert list_v2.current_reservation_spots == json_data["current_reservation_spots"]
    assert len(list_v2.reservations) == len(json_data["reservations"])
