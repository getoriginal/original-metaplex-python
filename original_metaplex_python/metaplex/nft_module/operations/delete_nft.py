from dataclasses import dataclass
from typing import Optional, cast

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.authorization import (
    ParsedTokenMetadataAuthorization,
    TokenMetadataAuthorityHolder,
    TokenMetadataAuthorityTokenDelegate,
    TokenMetadataAuthorization,
    get_signer_from_token_metadata_authority,
    parse_token_metadata_authorization,
)
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
    TokenRecordPdaInput,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.amount import SplTokenAmount, token
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    BurnAccounts,
    BurnArgs,
    burn,
)
from original_metaplex_python.token_metadata.generated.types.burn_args import (
    from_decoded,
)


@dataclass
class DeleteNftBuilderParams:
    mint_address: Pubkey
    authority: Optional[
        Signer | TokenMetadataAuthorityTokenDelegate | TokenMetadataAuthorityHolder
    ] = None
    owner: Optional[Signer] = None
    parent_edition_mint: Optional[Pubkey] = None
    parent_edition_token: Optional[Pubkey] = None
    edition_marker: Optional[Pubkey] = None
    owner_token_account: Optional[Pubkey] = None
    collection: Optional[Pubkey] = None
    amount: Optional[SplTokenAmount] = None
    instruction_key: Optional[str] = None


def delete_nft_builder(
    metaplex,
    params: DeleteNftBuilderParams,
    options: Optional[TransactionBuilderOptions] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    mint_address = params.mint_address
    owner_token_account = params.owner_token_account
    collection = params.collection
    parent_edition_mint = params.parent_edition_mint
    parent_edition_token = params.parent_edition_token
    edition_marker = params.edition_marker
    amount = params.amount or token(1)

    authority = params.authority or params.owner or metaplex.identity()

    token_program = metaplex.programs().get_token(programs)
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    owner = get_public_key(get_signer_from_token_metadata_authority(authority))
    metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=mint_address, programs=programs))
    )
    edition = (
        metaplex.nfts()
        .pdas()
        .master_edition(MintAddressPdaInput(mint=mint_address, programs=programs))
    )
    token_address = (
        owner_token_account
        if owner_token_account is not None
        else metaplex.tokens()
        .pdas()
        .associated_token_account(
            AssociatedTokenAccountOptions(
                mint=mint_address, owner=owner, programs=programs
            )
        )
    )

    token_record = (
        metaplex.nfts()
        .pdas()
        .token_record(
            TokenRecordPdaInput(
                mint=mint_address, token=token_address, programs=programs
            )
        )
    )

    authority = (
        authority
        if isinstance(authority, TokenMetadataAuthorityHolder)
        else TokenMetadataAuthorityHolder(
            owner=cast(Signer, authority),
            token=token_address,
        )
    )
    # Auth
    auth: ParsedTokenMetadataAuthorization = parse_token_metadata_authorization(
        metaplex,
        TokenMetadataAuthorization(
            mint=mint_address, authority=authority, programs=programs
        ),
    )

    transaction_builder = (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .add(
            InstructionWithSigners(
                instruction=burn(
                    accounts=BurnAccounts(
                        authority=auth.accounts.authority,
                        collection_metadata=(
                            metaplex.nfts()
                            .pdas()
                            .metadata(
                                MintAddressPdaInput(mint=collection, programs=programs)
                            )
                            if collection
                            else None
                        ),
                        metadata=metadata,
                        edition=edition,
                        mint=mint_address,
                        token=cast(Pubkey, auth.accounts.token),
                        master_edition=(
                            metaplex.nfts()
                            .pdas()
                            .metadata(
                                MintAddressPdaInput(
                                    mint=parent_edition_mint, programs=programs
                                )
                            )
                            if parent_edition_mint
                            else None
                        ),
                        master_edition_mint=parent_edition_mint,
                        master_edition_token=parent_edition_token,
                        edition_marker=edition_marker,
                        token_record=(
                            token_record
                            if token_record
                            else auth.accounts.delegate_record
                        ),
                        sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                        spl_token_program=token_program.address,
                    ),
                    args=BurnArgs(
                        burn_args=from_decoded(
                            {
                                "V1": {"amount": int(amount.basis_points)},
                            }
                        )
                    ),
                    program_id=token_metadata_program.address,
                ),
                signers=auth.signers,
                key=params.instruction_key or "delete_nft",
            )
        )
    )

    return transaction_builder
