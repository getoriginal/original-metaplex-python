from dataclasses import asdict

from construct import Container

from src.token_metadata.generated.types.proof_info import ProofInfo


def test_proof_info_to_encodable():
    proof = [[i for i in range(32)]]
    proof_info = ProofInfo(proof=proof)
    encodable = proof_info.to_encodable()
    assert encodable == {"proof": proof}


def test_proof_info_from_decoded():
    proof = [[i for i in range(32)]]
    decoded = Container(proof=proof)
    proof_info = ProofInfo.from_decoded(decoded)
    assert isinstance(proof_info, ProofInfo) and proof_info.proof == proof


def test_proof_info_to_json():
    proof = [[i for i in range(32)]]
    proof_info = ProofInfo(proof=proof)
    json_obj = proof_info.to_json()
    assert json_obj == {"proof": proof}


def test_proof_info_from_json():
    proof = [[i for i in range(32)]]
    json_obj = {"proof": proof}
    proof_info = ProofInfo.from_json(json_obj)
    assert isinstance(proof_info, ProofInfo) and proof_info.proof == proof


def test_proof_info_dataclass():
    proof = [[i for i in range(32)]]
    proof_info = ProofInfo(proof=proof)
    assert asdict(proof_info) == {"proof": proof}
