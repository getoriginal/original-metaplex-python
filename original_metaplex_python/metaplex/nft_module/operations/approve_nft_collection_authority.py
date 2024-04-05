from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    CollectionAuthorityRecordPdaInput,
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    ApproveCollectionAuthorityAccounts,
    approve_collection_authority,
)


@dataclass
class ApproveNftCollectionAuthorityInput:
    mint_address: Pubkey
    collection_authority: Pubkey
    update_authority: Optional[Signer] = None


@dataclass
class ApproveNftCollectionAuthorityBuilderParams(ApproveNftCollectionAuthorityInput):
    instruction_key: Optional[str] = None


def approve_nft_collection_authority_builder(
    metaplex,
    params: ApproveNftCollectionAuthorityBuilderParams,
    options: Optional[TransactionBuilderOptions | None] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    mint_address = params.mint_address
    collection_authority = params.collection_authority
    update_authority = params.update_authority or metaplex.identity()

    # Programs
    # system_program = metaplex.programs().get_system(programs)
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    # PDAs
    metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=mint_address, programs=programs))
    )
    collection_authority_record = (
        metaplex.nfts()
        .pdas()
        .collection_authority_record(
            CollectionAuthorityRecordPdaInput(
                mint=mint_address,
                collection_authority=collection_authority,
                programs=programs,
            )
        )
    )

    # Building the transaction
    transaction_builder = TransactionBuilder.make().set_fee_payer(payer)

    transaction_builder.add(
        InstructionWithSigners(
            instruction=approve_collection_authority(
                accounts=ApproveCollectionAuthorityAccounts(
                    collection_authority_record=collection_authority_record,
                    new_collection_authority=collection_authority,
                    update_authority=get_public_key(update_authority),
                    payer=get_public_key(payer),
                    metadata=metadata,
                    mint=mint_address,
                ),
                program_id=token_metadata_program.address,
            ),
            signers=[payer, update_authority],
            key=params.instruction_key or "approve_collection_authority",
        )
    )

    return transaction_builder
