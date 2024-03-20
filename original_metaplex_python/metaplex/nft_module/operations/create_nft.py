from dataclasses import dataclass
from typing import Optional, cast

from solders.keypair import Keypair
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types import Uses
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    NonFungible,
    TokenStandardKind,
)

from ...types.amount import token
from ...types.creator import CreatorInput
from ...types.signer import Signer
from ...utils.transaction_builder import TransactionBuilder, TransactionBuilderOptions
from ..nft_pdas_client import MintAddressPdaInput
from .create_sft import CreateSftBuilderParams


@dataclass
class CreateNftBuilderParams:
    uri: str
    name: str
    seller_fee_basis_points: int
    update_authority: Optional[Signer] = None
    mint_authority: Optional[Signer] = None
    use_new_mint: Optional[Keypair] = None
    use_existing_mint: Optional[Pubkey] = None
    mint_tokens: Optional[bool] = None
    token_owner: Optional[Pubkey] = None
    token_address: Optional[Pubkey] = None
    token_standard: Optional[TokenStandardKind] = None
    symbol: Optional[str] = None
    creators: Optional[list[CreatorInput]] = None
    is_mutable: Optional[bool] = None
    primary_sale_happened: Optional[bool] = None
    max_supply: Optional[tuple[int]] = None
    uses: Optional[Uses] = None
    is_collection: Optional[bool] = None
    collection: Optional[Pubkey] = None
    collection_authority: Optional[Signer] = None
    collection_authority_is_delegated: Optional[bool] = None
    collection_is_sized: Optional[bool] = None
    rule_set: Optional[Pubkey] = None
    tree: Optional[Pubkey] = None
    token_exists: Optional[bool] = None
    create_mint_account_instruction_key: Optional[str] = None
    initialize_mint_instruction_key: Optional[str] = None
    create_associated_token_account_instruction_key: Optional[str] = None
    create_token_account_instruction_key: Optional[str] = None
    initialize_token_instruction_key: Optional[str] = None
    mint_tokens_instruction_key: Optional[str] = None
    create_metadata_instruction_key: Optional[str] = None
    create_master_edition_instruction_key: Optional[str] = None


def create_nft_builder(
    metaplex,
    params: CreateNftBuilderParams,
    options: Optional[TransactionBuilderOptions | None] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    use_new_mint = params.use_new_mint  # TODO_ORIGINAL Added - or Keypair()
    update_authority = params.update_authority or metaplex.identity()
    mint_authority = params.mint_authority or metaplex.identity()
    token_owner = params.token_owner or metaplex.identity().public_key
    mint_tokens = params.mint_tokens or True

    # TODO_ORIGINAL: Unused
    # tree = params.get("tree", None)
    #
    # if tree:
    #     return create_compressed_nft_builder(
    #         metaplex,
    #         params,
    #         options
    #     )

    sft_builder = (
        metaplex.nfts()
        .builders()
        .create_sft(
            CreateSftBuilderParams(
                token_standard=params.token_standard
                or cast(TokenStandardKind, NonFungible),
                update_authority=update_authority,
                mint_authority=mint_authority,
                use_new_mint=use_new_mint,
                token_owner=token_owner,
                token_amount=token(1) if mint_tokens else None,
                decimals=0,
                uri=params.uri,
                name=params.name,
                seller_fee_basis_points=params.seller_fee_basis_points,
                use_existing_mint=params.use_existing_mint,
                token_address=params.token_address,
                symbol=params.symbol,
                creators=params.creators,
                is_mutable=params.is_mutable,
                max_supply=params.max_supply,
                primary_sale_happened=params.primary_sale_happened,
                uses=params.uses,
                is_collection=params.is_collection,
                collection=params.collection,
                collection_authority=params.collection_authority,
                collection_authority_is_delegated=params.collection_authority_is_delegated,
                collection_is_sized=params.collection_is_sized,
                rule_set=params.rule_set,
            ),
            TransactionBuilderOptions(
                programs=programs,
                payer=payer,
            ),
        )
    )

    context = sft_builder.get_context()
    mint_address = context.get("mintAddress")
    metadata_address = context.get("metadataAddress")
    token_address = context.get("tokenAddress")

    master_edition_address = (
        metaplex.nfts()
        .pdas()
        .master_edition(MintAddressPdaInput(mint=mint_address, programs=programs))
    )

    return (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .set_context(
            {
                "mintAddress": mint_address,
                "metadataAddress": metadata_address,
                "masterEditionAddress": master_edition_address,
                "tokenAddress": token_address,
            }
        )
        .add(sft_builder)
    )
