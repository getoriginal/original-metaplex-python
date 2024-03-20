from dataclasses import asdict

from construct import Container
from solders.pubkey import Pubkey

from src.token_metadata.generated.types.reservation import Reservation


def test_reservation_to_encodable():
    pubkey = Pubkey.new_unique()
    reservation = Reservation(address=pubkey, spots_remaining=5, total_spots=10)
    encodable = reservation.to_encodable()
    assert encodable == {"address": pubkey, "spots_remaining": 5, "total_spots": 10}


def test_reservation_from_decoded():
    pubkey = Pubkey.new_unique()
    decoded = Container(address=pubkey, spots_remaining=5, total_spots=10)
    reservation = Reservation.from_decoded(decoded)
    assert (
        isinstance(reservation, Reservation)
        and reservation.address == pubkey
        and reservation.spots_remaining == 5
        and reservation.total_spots == 10
    )


def test_reservation_to_json():
    pubkey = Pubkey.new_unique()
    reservation = Reservation(address=pubkey, spots_remaining=5, total_spots=10)
    json_obj = reservation.to_json()
    assert json_obj == {"address": str(pubkey), "spots_remaining": 5, "total_spots": 10}


def test_reservation_from_json():
    pubkey_str = str(Pubkey.new_unique())
    json_obj = {"address": pubkey_str, "spots_remaining": 5, "total_spots": 10}
    reservation = Reservation.from_json(json_obj)
    assert (
        isinstance(reservation, Reservation)
        and str(reservation.address) == pubkey_str
        and reservation.spots_remaining == 5
        and reservation.total_spots == 10
    )


def test_reservation_dataclass():
    pubkey = Pubkey.new_unique()
    reservation = Reservation(address=pubkey, spots_remaining=5, total_spots=10)
    assert asdict(reservation) == {
        "address": pubkey,
        "spots_remaining": 5,
        "total_spots": 10,
    }
