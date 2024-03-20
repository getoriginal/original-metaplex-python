from construct import Container

from src.token_metadata.generated.types.utilize_args import UtilizeArgs


def test_utilize_args_to_encodable():
    utilize_args = UtilizeArgs(number_of_uses=5)
    encodable = utilize_args.to_encodable()
    assert encodable == {"number_of_uses": 5}


def test_utilize_args_from_decoded():
    decoded = Container(number_of_uses=5)
    result = UtilizeArgs.from_decoded(decoded)
    assert isinstance(result, UtilizeArgs) and result.number_of_uses == 5


def test_utilize_args_to_json():
    utilize_args = UtilizeArgs(number_of_uses=5)
    json_obj = utilize_args.to_json()
    assert json_obj == {"number_of_uses": 5}


def test_utilize_args_from_json():
    json_obj = {"number_of_uses": 5}
    result = UtilizeArgs.from_json(json_obj)
    assert isinstance(result, UtilizeArgs) and result.number_of_uses == 5
