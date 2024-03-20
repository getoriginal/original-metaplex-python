from dataclasses import asdict

from construct import Container
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types.reservation_v1 import (
    ReservationV1,
)


def test_reservation_v1_to_encodable():
    pubkey = Pubkey.new_unique()
    reservation_v1 = ReservationV1(address=pubkey, spots_remaining=5, total_spots=10)
    encodable = reservation_v1.to_encodable()
    assert encodable == {"address": pubkey, "spots_remaining": 5, "total_spots": 10}


def test_reservation_v1_from_decoded():
    pubkey = Pubkey.new_unique()
    decoded = Container(address=pubkey, spots_remaining=5, total_spots=10)
    reservation_v1 = ReservationV1.from_decoded(decoded)
    assert (
        isinstance(reservation_v1, ReservationV1)
        and reservation_v1.address == pubkey
        and reservation_v1.spots_remaining == 5
        and reservation_v1.total_spots == 10
    )


def test_reservation_v1_to_json():
    pubkey = Pubkey.new_unique()
    reservation_v1 = ReservationV1(address=pubkey, spots_remaining=5, total_spots=10)
    json_obj = reservation_v1.to_json()
    assert json_obj == {"address": str(pubkey), "spots_remaining": 5, "total_spots": 10}


def test_reservation_v1_from_json():
    pubkey_str = str(Pubkey.new_unique())
    json_obj = {"address": pubkey_str, "spots_remaining": 5, "total_spots": 10}
    reservation_v1 = ReservationV1.from_json(json_obj)
    assert (
        isinstance(reservation_v1, ReservationV1)
        and str(reservation_v1.address) == pubkey_str
        and reservation_v1.spots_remaining == 5
        and reservation_v1.total_spots == 10
    )


def test_reservation_v1_dataclass():
    pubkey = Pubkey.new_unique()
    reservation_v1 = ReservationV1(address=pubkey, spots_remaining=5, total_spots=10)
    assert asdict(reservation_v1) == {
        "address": pubkey,
        "spots_remaining": 5,
        "total_spots": 10,
    }
