from dataclasses import dataclass
from typing import Optional, Union

from solders.instruction import AccountMeta
from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    CollectionAuthorityRecordPdaInput,
    MetadataDelegateRecordPdaInput,
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    VerifyAccounts,
    VerifyArgs,
    VerifyCollectionAccounts,
    VerifySizedCollectionItemAccounts,
    verify,
    verify_collection,
    verify_sized_collection_item,
)
from original_metaplex_python.token_metadata.generated.types.verification_args import (
    from_decoded,
)


@dataclass
class VerifyNftCollectionBuilderParams:
    mint_address: Pubkey
    collection_mint_address: Pubkey
    collection_authority: Optional[Signer] = None
    is_sized_collection: Optional[bool] = None
    is_delegated: Optional[Union[bool, str]] = None
    collection_update_authority: Optional[Pubkey] = None
    instruction_key: Optional[str] = None


def verify_nft_collection_builder(
    metaplex,
    params: VerifyNftCollectionBuilderParams,
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
    is_sized_collection = params.is_sized_collection
    is_delegated = params.is_delegated or False
    collection_authority = params.collection_authority or metaplex.identity()
    collection_update_authority = (
        params.collection_update_authority or metaplex.identity().public_key
    )

    # Programs
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    # Accounts
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

    if is_delegated == "legacy_delegate" or is_delegated is True:
        if is_sized_collection:
            instruction = verify_sized_collection_item(
                accounts=VerifySizedCollectionItemAccounts(
                    metadata=metadata,
                    collection_authority=get_public_key(collection_authority),
                    payer=get_public_key(payer),
                    collection_mint=collection_mint_address,
                    collection=collection_metadata,
                    collection_master_edition_account=collection_edition,
                    collection_authority_record=None,
                ),
                program_id=token_metadata_program.address,
            )
        else:
            instruction = verify_collection(
                accounts=VerifyCollectionAccounts(
                    metadata=metadata,
                    collection_authority=get_public_key(collection_authority),
                    payer=get_public_key(payer),
                    collection_mint=collection_mint_address,
                    collection=collection_metadata,
                    collection_master_edition_account=collection_edition,
                    collection_authority_record=None,
                ),
                program_id=token_metadata_program.address,
            )

        instruction.accounts.append(
            AccountMeta(
                pubkey=metaplex.nfts()
                .pdas()
                .collection_authority_record(
                    CollectionAuthorityRecordPdaInput(
                        mint=collection_mint_address,
                        collection_authority=get_public_key(collection_authority),
                        programs=programs,
                    )
                ),
                is_writable=False,
                is_signer=False,
            )
        )

        return (
            TransactionBuilder.make()
            .set_fee_payer(payer)
            .add(
                InstructionWithSigners(
                    instruction=instruction,
                    signers=[payer, collection_authority],
                    key=params.instruction_key or "verify_collection",
                )
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
                delegate=get_public_key(collection_authority),
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
            InstructionWithSigners(
                instruction=verify(
                    accounts=VerifyAccounts(
                        authority=get_public_key(collection_authority),
                        delegate_record=delegate_record,
                        metadata=metadata,
                        collection_mint=collection_mint_address,
                        collection_metadata=collection_metadata,
                        collection_master_edition=collection_edition,
                        sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                    ),
                    args=VerifyArgs(
                        verification_args=from_decoded({"CollectionV1": {}})
                    ),
                    program_id=token_metadata_program.address,
                ),
                signers=[collection_authority],
                key=params.instruction_key or "verify_collection",
            )
        )
    )
