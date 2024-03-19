import pytest
from construct import Container

from src.token_metadata.generated.types.key import (
    CollectionAuthorityRecord,
    EditionMarker,
    EditionMarkerV2,
    EditionV1,
    MasterEditionV1,
    MasterEditionV2,
    MetadataDelegate,
    MetadataV1,
    ReservationListV1,
    ReservationListV2,
    TokenOwnedEscrow,
    TokenRecord,
    Uninitialized,
    UseAuthorityRecord,
    from_decoded,
    from_json,
)


@pytest.mark.parametrize(
    "kind_class,json_kind",
    [
        (Uninitialized, "Uninitialized"),
        (EditionV1, "EditionV1"),
        (MasterEditionV1, "MasterEditionV1"),
        (ReservationListV1, "ReservationListV1"),
        (MetadataV1, "MetadataV1"),
        (ReservationListV2, "ReservationListV2"),
        (MasterEditionV2, "MasterEditionV2"),
        (EditionMarker, "EditionMarker"),
        (UseAuthorityRecord, "UseAuthorityRecord"),
        (CollectionAuthorityRecord, "CollectionAuthorityRecord"),
        (TokenOwnedEscrow, "TokenOwnedEscrow"),
        (TokenRecord, "TokenRecord"),
        (MetadataDelegate, "MetadataDelegate"),
        (EditionMarkerV2, "EditionMarkerV2"),
    ],
)
def test_to_json(kind_class, json_kind):
    kind_instance = kind_class()
    json_obj = kind_instance.to_json()
    assert json_obj == {"kind": json_kind}


@pytest.mark.parametrize(
    "kind_class,json_kind",
    [
        (Uninitialized, "Uninitialized"),
        (EditionV1, "EditionV1"),
        (MasterEditionV1, "MasterEditionV1"),
        (ReservationListV1, "ReservationListV1"),
        (MetadataV1, "MetadataV1"),
        (ReservationListV2, "ReservationListV2"),
        (MasterEditionV2, "MasterEditionV2"),
        (EditionMarker, "EditionMarker"),
        (UseAuthorityRecord, "UseAuthorityRecord"),
        (CollectionAuthorityRecord, "CollectionAuthorityRecord"),
        (TokenOwnedEscrow, "TokenOwnedEscrow"),
        (TokenRecord, "TokenRecord"),
        (MetadataDelegate, "MetadataDelegate"),
        (EditionMarkerV2, "EditionMarkerV2"),
    ],
)
def test_from_json(kind_class, json_kind):
    json_obj = {"kind": json_kind}
    kind_instance = from_json(json_obj)
    assert isinstance(kind_instance, kind_class)


@pytest.mark.parametrize(
    "kind_class,encoded_dict",
    [
        (Uninitialized, {"Uninitialized": {}}),
        (EditionV1, {"EditionV1": {}}),
        (MasterEditionV1, {"MasterEditionV1": {}}),
        (ReservationListV1, {"ReservationListV1": {}}),
        (MetadataV1, {"MetadataV1": {}}),
        (ReservationListV2, {"ReservationListV2": {}}),
        (MasterEditionV2, {"MasterEditionV2": {}}),
        (EditionMarker, {"EditionMarker": {}}),
        (UseAuthorityRecord, {"UseAuthorityRecord": {}}),
        (CollectionAuthorityRecord, {"CollectionAuthorityRecord": {}}),
        (TokenOwnedEscrow, {"TokenOwnedEscrow": {}}),
        (TokenRecord, {"TokenRecord": {}}),
        (MetadataDelegate, {"MetadataDelegate": {}}),
        (EditionMarkerV2, {"EditionMarkerV2": {}}),
    ],
)
def test_to_encodable(kind_class, encoded_dict):
    kind_instance = kind_class()
    encodable = kind_instance.to_encodable()
    assert encodable == encoded_dict


@pytest.mark.parametrize(
    "kind_class,decoded_dict",
    [
        (Uninitialized, {"Uninitialized": {}}),
        (EditionV1, {"EditionV1": {}}),
        (MasterEditionV1, {"MasterEditionV1": {}}),
        (ReservationListV1, {"ReservationListV1": {}}),
        (MetadataV1, {"MetadataV1": {}}),
        (ReservationListV2, {"ReservationListV2": {}}),
        (MasterEditionV2, {"MasterEditionV2": {}}),
        (EditionMarker, {"EditionMarker": {}}),
        (UseAuthorityRecord, {"UseAuthorityRecord": {}}),
        (CollectionAuthorityRecord, {"CollectionAuthorityRecord": {}}),
        (TokenOwnedEscrow, {"TokenOwnedEscrow": {}}),
        (TokenRecord, {"TokenRecord": {}}),
        (MetadataDelegate, {"MetadataDelegate": {}}),
        (EditionMarkerV2, {"EditionMarkerV2": {}}),
    ],
)
def test_from_decoded(kind_class, decoded_dict):
    decoded = Container(**decoded_dict)
    kind_instance = from_decoded(decoded)
    assert isinstance(kind_instance, kind_class)
