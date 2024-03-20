from dataclasses import dataclass
from typing import Any, Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.models.json_metadata import (
    Creator,
    JsonMetadata,
)
from original_metaplex_python.metaplex.nft_module.models.metadata import (
    Collection,
    CollectionDetails,
    Metadata,
)
from original_metaplex_python.metaplex.token_module.models.mint import Mint
from original_metaplex_python.metaplex.token_module.models.token import Token
from original_metaplex_python.token_metadata.generated.types import Uses


@dataclass
class Sft:
    model: str
    address: Pubkey
    metadata_address: Pubkey
    mint: Mint
    update_authority_address: Pubkey
    json_loaded: bool
    name: str
    symbol: str
    uri: str
    is_mutable: bool
    primary_sale_happened: bool
    seller_fee_basis_points: int
    creators: list[Creator]
    json: Optional[JsonMetadata] = None
    edition_nonce: Optional[int] = None
    token_standard: Optional[int] = None
    collection: Optional[Collection] = None
    collection_details: Optional[CollectionDetails] = None
    uses: Optional[Uses] = None
    programmable_config: Optional[Any] = None


@dataclass
class SftWithToken(Sft):
    token: Optional[Token] = None


def is_sft(value: Any) -> bool:
    return isinstance(value, dict) and value.get("model") == "sft"


def assert_sft(value: Any):
    if not is_sft(value):
        raise AssertionError("Expected Sft model")


def to_sft(metadata: Metadata, mint: Mint) -> Sft:
    assert (
        metadata.mint_address == mint.address
    ), "The provided mint does not match the mint address in the metadata"

    return Sft(
        model="sft",
        address=metadata.mint_address,
        metadata_address=metadata.address,
        mint=mint,
        update_authority_address=metadata.update_authority_address,
        json=metadata.json,
        json_loaded=metadata.json_loaded,
        name=metadata.name,
        symbol=metadata.symbol,
        uri=metadata.uri,
        is_mutable=metadata.is_mutable,
        primary_sale_happened=metadata.primary_sale_happened,
        seller_fee_basis_points=metadata.seller_fee_basis_points,
        edition_nonce=metadata.edition_nonce,
        creators=metadata.creators,
        token_standard=metadata.token_standard,
        collection=metadata.collection,
        collection_details=metadata.collection_details,
        uses=metadata.uses,
        programmable_config=metadata.programmable_config,
    )


def is_sft_with_token(value: Any) -> bool:
    return is_sft(value) and "token" in value


def assert_sft_with_token(value: Any):
    if not is_sft_with_token(value):
        raise AssertionError("Expected Sft model with token")


def to_sft_with_token(metadata: Metadata, mint: Mint, token: Token) -> SftWithToken:
    sft = to_sft(metadata, mint)
    sft_with_token = SftWithToken(**sft.__dict__, token=token)

    return sft_with_token
