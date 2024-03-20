from dataclasses import asdict

from original_metaplex_python.token_metadata.generated.types.print_supply import (
    Limited,
    Unlimited,
    Zero,
    from_decoded,
    from_json,
)


def test_print_supply_zero_to_encodable():
    zero = Zero()
    encodable = zero.to_encodable()
    assert encodable == {"Zero": {}}


def test_print_supply_limited_to_encodable():
    limited = Limited(value=(5,))
    encodable = limited.to_encodable()
    assert encodable == {"Limited": {"item_0": 5}}


def test_print_supply_unlimited_to_encodable():
    unlimited = Unlimited()
    encodable = unlimited.to_encodable()
    assert encodable == {"Unlimited": {}}


def test_print_supply_zero_from_decoded():
    decoded = {"Zero": {}}
    zero = from_decoded(decoded)
    assert isinstance(zero, Zero)


def test_print_supply_limited_from_decoded():
    decoded = {"Limited": {"item_0": 5}}
    limited = from_decoded(decoded)
    assert limited.value == (5,)


def test_print_supply_unlimited_from_decoded():
    decoded = {"Unlimited": {}}
    unlimited = from_decoded(decoded)
    assert isinstance(unlimited, Unlimited)


def test_print_supply_zero_to_json():
    zero = Zero()
    json_obj = zero.to_json()
    assert json_obj == {"kind": "Zero"}


def test_print_supply_limited_to_json():
    limited = Limited(value=(5,))
    json_obj = limited.to_json()
    assert json_obj == {"kind": "Limited", "value": (5,)}


def test_print_supply_unlimited_to_json():
    unlimited = Unlimited()
    json_obj = unlimited.to_json()
    assert json_obj == {"kind": "Unlimited"}


def test_print_supply_zero_from_json():
    json_obj = {"kind": "Zero"}
    zero = from_json(json_obj)
    assert isinstance(zero, Zero)


def test_print_supply_limited_from_json():
    json_obj = {"kind": "Limited", "value": (5,)}
    limited = from_json(json_obj)
    assert limited.value == (5,)


def test_print_supply_unlimited_from_json():
    json_obj = {"kind": "Unlimited"}
    unlimited = from_json(json_obj)
    assert isinstance(unlimited, Unlimited)


def test_print_supply_dataclass():
    limited = Limited(value=(5,))
    assert asdict(limited) == {"value": (5,)}
