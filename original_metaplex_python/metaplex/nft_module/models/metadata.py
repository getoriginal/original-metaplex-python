from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List, Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.models.json_metadata import (
    Creator,
    JsonMetadata,
)
from original_metaplex_python.metaplex.types.pda import Pda
from original_metaplex_python.metaplex.types.read_api import ReadApiCompressionMetadata
from original_metaplex_python.metaplex.utils.common import remove_empty_chars
from original_metaplex_python.token_metadata.generated.types import Uses
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    NonFungible,
    NonFungibleEdition,
    ProgrammableNonFungible,
    ProgrammableNonFungibleEdition,
    TokenStandardKind,
)


@dataclass
class Collection:
    address: Pubkey
    verified: bool


@dataclass
class CollectionDetails:
    version: str
    size: Decimal


@dataclass
class Metadata:
    model: str
    address: Pubkey
    mint_address: Pubkey
    update_authority_address: Pubkey
    json: Optional[JsonMetadata]
    json_loaded: bool
    name: str
    symbol: str
    uri: str
    is_mutable: bool
    primary_sale_happened: bool
    seller_fee_basis_points: int
    creators: List[Creator]
    edition_nonce: Optional[int] = None
    token_standard: Optional[int] = None
    collection: Optional[Collection] = None
    collection_details: Optional[CollectionDetails] = None
    uses: Optional[Uses] = None
    programmable_config: Optional[Any] = None
    compression: Optional[ReadApiCompressionMetadata] = None


def is_metadata(value: Any) -> bool:
    return isinstance(value, dict) and value.get("model") == "metadata"


def assert_metadata(value: Any):
    assert is_metadata(value), "Expected Metadata model"


def to_metadata(account, public_key, json=None):
    address = Pda.find(
        public_key,
        [
            bytes("metadata", "utf-8"),
            bytes(
                account.update_authority
            ),  # TODO_ORIGINAL - original JS code. Is this correct? account.owner.to_bytes(),
            bytes(account.mint),  # account.data.mint.to_bytes()
        ],
    )

    json_loaded = json is not None

    name = remove_empty_chars(account.data.name)
    symbol = remove_empty_chars(account.data.symbol)
    uri = remove_empty_chars(account.data.uri)

    collection = None
    if account.collection:
        collection = Collection(
            address=account.collection.key, verified=account.collection.verified
        )

    collection_details = None
    if account.collection_details:
        collection_details = CollectionDetails(
            version=account.collection_details.kind,
            size=Decimal(account.collection_details.value["size"]),
        )

    uses = None
    if account.uses:
        uses = Uses(
            remaining=Decimal(account.uses.remaining), total=Decimal(account.uses.total)
        )

    return Metadata(
        model="metadata",
        address=address,
        mint_address=account.mint,
        update_authority_address=account.update_authority,
        json=json or None,
        json_loaded=json_loaded,
        name=name,
        symbol=symbol,
        uri=uri,
        is_mutable=account.is_mutable,
        primary_sale_happened=account.primary_sale_happened,
        seller_fee_basis_points=account.data.seller_fee_basis_points,
        edition_nonce=account.edition_nonce,
        creators=account.data.creators or [],
        token_standard=account.token_standard,
        collection=collection,
        collection_details=collection_details,
        uses=uses,
        programmable_config=account.programmable_config,
    )


def is_non_fungible_token_standard(token_standard: TokenStandardKind) -> bool:
    return token_standard in [
        NonFungible,
        NonFungibleEdition,
        ProgrammableNonFungible,
        ProgrammableNonFungibleEdition,
    ]


def is_non_fungible(nft_or_sft) -> bool:
    token_standard = nft_or_sft.token_standard
    return is_non_fungible_token_standard(token_standard)


def is_programmable_token_standard(token_standard: TokenStandardKind) -> bool:
    return token_standard in [ProgrammableNonFungible, ProgrammableNonFungibleEdition]


def is_programmable(nft_or_sft) -> bool:
    token_standard = nft_or_sft.token_standard
    return is_programmable_token_standard(token_standard)
