import pytest

from original_metaplex_python.token_metadata.generated.errors.custom import (
    CUSTOM_ERROR_MAP,
    AlreadyInitialized,
    AmountMustBeGreaterThanZero,
    BorshSerializationError,
    CannotWipeVerifiedCreators,
    CollectionNotFound,
    DataIncrementLimitExceeded,
    DataIsEmptyOrZeroed,
    DelegateNotFound,
    EditionAlreadyMinted,
    FeatureNotSupported,
    InstructionNotSupported,
    InstructionUnpackError,
    InvalidAmount,
    InvalidAuthorityType,
    InvalidBubblegumSigner,
    InvalidCollectionSizeChange,
    InvalidDelegateRole,
    InvalidDelegateRoleForTransfer,
    InvalidEditionIndex,
    InvalidFreezeAuthority,
    InvalidMetadataKey,
    InvalidMetadataPointer,
    InvalidMintCloseAuthority,
    InvalidMintForTokenStandard,
    InvalidOperation,
    InvalidSystemWallet,
    InvalidTokenStandard,
    InvalidUseMethod,
    KeyMismatch,
    LockedToken,
    MintIsNotSigner,
    MissingArgumentInBuilder,
    MissingDelegateRole,
    MissingImmutableOwnerExtension,
    MissingLockedTransferAddress,
    MissingMasterEditionAccount,
    MissingTokenAccount,
    MissingTokenRecord,
    NameTooLong,
    NoFreezeAuthoritySet,
    NotRentExempt,
    NumericalOverflowError,
    PrintingMintDecimalsShouldBeZero,
    PrintingMintSupplyMustBeZeroForConversion,
    Unusable,
    UpdateAuthorityIncorrect,
    from_code,
)


@pytest.mark.parametrize(
    "error_class,code",
    [
        (InstructionUnpackError, 0),
        (NotRentExempt, 2),
        (AlreadyInitialized, 3),
        (InvalidMetadataKey, 5),
        (UpdateAuthorityIncorrect, 7),
        (NameTooLong, 11),
        (EditionAlreadyMinted, 21),
        (PrintingMintDecimalsShouldBeZero, 22),
        (NumericalOverflowError, 51),
        (InvalidOperation, 67),
        (PrintingMintSupplyMustBeZeroForConversion, 69),
        (InvalidEditionIndex, 71),
        (CollectionNotFound, 80),
        (InvalidUseMethod, 77),
        (Unusable, 85),
        (InvalidFreezeAuthority, 91),
        (CannotWipeVerifiedCreators, 95),
        (InvalidAmount, 174),
        (DataIsEmptyOrZeroed, 161),
        (InvalidDelegateRole, 165),
        (MissingMasterEditionAccount, 167),
        (AmountMustBeGreaterThanZero, 168),
        (MissingLockedTransferAddress, 170),
        (DataIncrementLimitExceeded, 172),
        (LockedToken, 155),
        (MissingDelegateRole, 157),
        (InvalidTokenStandard, 135),
        (BorshSerializationError, 129),
        (NoFreezeAuthoritySet, 130),
        (InvalidCollectionSizeChange, 131),
        (InvalidBubblegumSigner, 132),
        (MintIsNotSigner, 134),
        (InvalidMintForTokenStandard, 136),
        (DelegateNotFound, 142),
        (MissingArgumentInBuilder, 144),
        (FeatureNotSupported, 145),
        (InvalidSystemWallet, 146),
        (MissingTokenAccount, 148),
        (InvalidDelegateRoleForTransfer, 151),
        (InstructionNotSupported, 153),
        (KeyMismatch, 154),
        (InvalidAuthorityType, 158),
        (MissingTokenRecord, 159),
        (InvalidMintCloseAuthority, 195),
        (InvalidMetadataPointer, 196),
        (MissingImmutableOwnerExtension, 198),
    ],
)
def test_error_instantiation(error_class, code):
    error_instance = error_class()
    assert error_instance.code == code
    assert isinstance(error_instance, error_class)


def test_from_code():
    for code, expected_instance in CUSTOM_ERROR_MAP.items():
        error_instance = from_code(code)
        assert isinstance(error_instance, type(expected_instance))
        assert error_instance.code == expected_instance.code


def test_from_code_invalid():
    invalid_code = 9999  # Assuming 9999 is not a valid error code
    assert from_code(invalid_code) is None
