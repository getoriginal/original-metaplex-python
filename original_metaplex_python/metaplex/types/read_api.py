from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ReadApiCompressionMetadata:
    eligible: bool
    compressed: bool
    data_hash: str
    creator_hash: str
    asset_hash: str
    tree: str
    seq: int
    leaf_id: int


@dataclass
class ReadApiOwnershipMetadata:
    frozen: bool
    delegated: bool
    delegate: str | None
    owner: str
    ownership_model: str


@dataclass
class GetAssetProofRpcResponse:
    root: str
    proof: str
    node_index: int
    leaf: str
    tree_id: str


ConcurrentMerkleTreeAccount = (
    Any  # TODO_ORIGINAL solana-account-compression. Doesn't exist in python solana
)


@dataclass
class TransferNftCompressionParam:
    ownership: ReadApiOwnershipMetadata
    data: Optional[ReadApiCompressionMetadata] = None
    asset_proof: Optional[GetAssetProofRpcResponse] = None
    merkle_tree: Optional[ConcurrentMerkleTreeAccount] = None
