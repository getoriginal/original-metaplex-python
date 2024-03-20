from dataclasses import dataclass
from typing import Optional, Union

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    CollectionAuthorityRecordPdaInput,
    MetadataDelegateRecordPdaInput,
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.types.signer import Signer
from original_metaplex_python.metaplex.utils.transaction_builder import (
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    UnverifyAccounts,
    UnverifyArgs,
    UnverifyCollectionAccounts,
    UnverifySizedCollectionItemAccounts,
    unverify,
    unverify_collection,
    unverify_sized_collection_item,
)
from original_metaplex_python.token_metadata.generated.types.verification_args import (
    CollectionV1,
)


@dataclass
class UnverifyNftCollectionBuilderParams:
    mint_address: Pubkey
    collection_mint_address: Pubkey
    collection_authority: Optional[Signer] = None
    is_sized_collection: Optional[bool] = None
    is_delegated: Optional[Union[bool, str]] = None
    collection_update_authority: Optional[Pubkey] = None
    instruction_key: Optional[str] = None


def unverify_nft_collection_builder(
    metaplex,
    params: UnverifyNftCollectionBuilderParams,
    options: Optional[TransactionBuilderOptions] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    mint_address = params.mint_address
    collection_mint_address = params.collection_mint_address
    is_sized_collection = params.is_sized_collection or True
    is_delegated = params.is_delegated or False
    collection_authority = params.collection_authority or metaplex.identity()
    collection_update_authority = (
        params.collection_update_authority or metaplex.identity().public_key
    )

    # Programs.
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    # Accounts.
    metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=mint_address, programs=programs))
    )

    collection_metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=collection_mint_address, programs=programs))
    )

    collection_edition = (
        metaplex.nfts()
        .pdas()
        .master_edition(
            MintAddressPdaInput(mint=collection_mint_address, programs=programs)
        )
    )

    if is_delegated == "legacy_delegate" or is_delegated:
        instruction = (
            unverify_sized_collection_item(
                accounts=UnverifySizedCollectionItemAccounts(
                    metadata=metadata,
                    collection_authority=collection_authority.public_key,
                    payer=payer.public_key,
                    collection_mint=collection_mint_address,
                    collection=collection_metadata,
                    collection_master_edition_account=collection_edition,
                    collection_authority_record=metaplex.nfts()
                    .pdas()
                    .collection_authority_record(
                        CollectionAuthorityRecordPdaInput(
                            mint=collection_mint_address,
                            collection_authority=collection_authority.public_key,
                            programs=programs,
                        )
                    ),
                ),
                program_id=token_metadata_program.address,
            )
            if is_sized_collection
            else (
                unverify_collection(
                    accounts=UnverifyCollectionAccounts(
                        metadata=metadata,
                        collection_authority=collection_authority.public_key,
                        collection_mint=collection_mint_address,
                        collection=collection_metadata,
                        collection_master_edition_account=collection_edition,
                        collection_authority_record=metaplex.nfts()
                        .pdas()
                        .collection_authority_record(
                            CollectionAuthorityRecordPdaInput(
                                mint=collection_mint_address,
                                collection_authority=collection_authority.public_key,
                                programs=programs,
                            )
                        ),
                    ),
                    program_id=token_metadata_program.address,
                )
            )
        )

        return (
            TransactionBuilder.make()
            .set_fee_payer(payer)
            .add(
                {
                    "instruction": instruction,
                    "signers": [payer, collection_authority],
                    "key": params.instruction_key or "unverify_collection",
                }
            )
        )

    delegate_record = (
        metaplex.nfts()
        .pdas()
        .metadata_delegate_record(
            MetadataDelegateRecordPdaInput(
                mint=collection_mint_address,
                type="CollectionV1",
                update_authority=collection_update_authority,
                delegate=collection_authority.public_key,
                programs=programs,
            )
        )
        if is_delegated == "metadata_delegate"
        else None
    )

    return (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .add(
            {
                "instruction": unverify(
                    accounts=UnverifyAccounts(
                        authority=collection_authority.public_key,
                        delegate_record=delegate_record,
                        metadata=metadata,
                        collection_mint=collection_mint_address,
                        collection_metadata=collection_metadata,
                        sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                    ),
                    args=UnverifyArgs(verification_args=CollectionV1()),
                    program_id=token_metadata_program.address,
                ),
                "signers": [collection_authority],
                "key": params.instruction_key or "unverify_collection",
            }
        )
    )