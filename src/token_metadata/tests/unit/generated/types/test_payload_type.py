from solders.pubkey import Pubkey

from src.token_metadata.generated.types.payload_type import (
    MerkleProof,
    Number,
    PubkeyPayload,
    Seeds,
)
from src.token_metadata.generated.types.payload_type import (
    from_decoded as payload_type_from_decoded,
)
from src.token_metadata.generated.types.payload_type import (
    from_json as payload_type_from_json,
)
from src.token_metadata.generated.types.proof_info import ProofInfo
from src.token_metadata.generated.types.seeds_vec import SeedsVec


def test_payload_type_kind_to_json():
    kinds = [
        PubkeyPayload((Pubkey.new_unique(),)),
        Seeds((SeedsVec([bytes(Pubkey.new_unique())]),)),
        MerkleProof(
            (ProofInfo([bytes(Pubkey.new_unique()), bytes(Pubkey.new_unique())]),)
        ),
        Number((42,)),
    ]
    for kind in kinds:
        json_obj = kind.to_json()
        assert json_obj["kind"] == kind.kind


def test_payload_type_kind_to_encodable():
    kinds = [
        PubkeyPayload((Pubkey.new_unique(),)),
        Seeds((SeedsVec([Pubkey.new_unique()]),)),
        MerkleProof((ProofInfo([Pubkey.new_unique(), Pubkey.new_unique()]),)),
        Number((42,)),
    ]
    for kind in kinds:
        encodable = kind.to_encodable()
        assert list(encodable.keys())[0] == kind.kind


def test_payload_type_kind_from_json():
    pubkey = Pubkey.new_unique()
    pubkey_bytes = list(bytes(pubkey))
    proof_bytes = [[int(byte) for byte in pubkey_bytes]]

    kinds_json = [
        {"kind": "PubkeyPayload", "value": (str(Pubkey.new_unique()),)},
        {"kind": "Seeds", "value": [{"seeds": pubkey_bytes}]},
        {"kind": "MerkleProof", "value": [{"proof": proof_bytes}]},
        {"kind": "Number", "value": (42,)},
    ]
    for kind_json in kinds_json:
        kind = payload_type_from_json(kind_json)
        assert kind.kind == kind_json["kind"]


def test_payload_type_kind_from_decoded():
    kinds_decoded = [
        {"PubkeyPayload": {"item_0": Pubkey.new_unique()}},
        {"Seeds": {"item_0": SeedsVec([])}},
        {"MerkleProof": {"item_0": ProofInfo([])}},
        {"Number": {"item_0": 42}},
    ]
    for kind_decoded in kinds_decoded:
        kind = payload_type_from_decoded(kind_decoded)
        assert kind.kind == list(kind_decoded.keys())[0]
