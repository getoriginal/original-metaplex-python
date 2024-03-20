import pytest

from original_metaplex_python.token_metadata.generated.errors.anchor import (
    ANCHOR_ERROR_MAP,
    AccountDiscriminatorAlreadySet,
    ConstraintMut,
    Deprecated,
    InstructionFallbackNotFound,
    InstructionMissing,
    from_code,
)


@pytest.mark.parametrize(
    "error_class,code",
    [
        (InstructionMissing, 100),
        (InstructionFallbackNotFound, 101),
        (ConstraintMut, 2000),
        (AccountDiscriminatorAlreadySet, 3000),
        (Deprecated, 5000),
    ],
)
def test_error_instantiation(error_class, code):
    error_instance = error_class()
    assert error_instance.code == code
    assert isinstance(error_instance, error_class)


def test_from_code():
    for code, expected_instance in ANCHOR_ERROR_MAP.items():
        error_instance = from_code(code)
        assert isinstance(error_instance, type(expected_instance))
        assert error_instance.code == expected_instance.code


def test_from_code_invalid():
    invalid_code = 9999  # Assuming 9999 is not a valid error code
    assert from_code(invalid_code) is None
