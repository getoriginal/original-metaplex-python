from dataclasses import dataclass
from typing import Optional

from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    CollectionAuthorityRecordPdaInput,
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.types.signer import Signer
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    RevokeCollectionAuthorityAccounts,
    revoke_collection_authority,
)


@dataclass
class RevokeNftCollectionAuthorityInput:
    mint_address: Pubkey
    collection_authority: Pubkey
    revoke_authority: Optional[Signer] = None


@dataclass
class RevokeNftCollectionAuthorityBuilderParams(RevokeNftCollectionAuthorityInput):
    instruction_key: Optional[str] = None


def revoke_nft_collection_authority_builder(
    metaplex,
    params: RevokeNftCollectionAuthorityBuilderParams,
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
    revoke_authority = params.revoke_authority or metaplex.identity()

    # Get the token metadata program
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    # Generate PDAs
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

    # Create the instruction for revoking the collection authority
    instruction = revoke_collection_authority(
        accounts=RevokeCollectionAuthorityAccounts(
            collection_authority_record=collection_authority_record,
            delegate_authority=collection_authority,
            revoke_authority=revoke_authority.public_key,
            metadata=metadata,
            mint=mint_address,
        ),
        program_id=token_metadata_program.address,
    )

    old_accounts = instruction.accounts

    # Temporary fix. The Shank macro wrongfully ask for the delegateAuthority to be a signer.
    # https://github.com/metaplex-foundation/metaplex-program-library/pull/639
    new_delegate_authority_account = AccountMeta(
        pubkey=collection_authority, is_signer=False, is_writable=True
    )
    instruction.accounts = (
        old_accounts[:1] + [new_delegate_authority_account] + old_accounts[2:]
    )

    # Building the transaction
    transaction_builder = TransactionBuilder.make().set_fee_payer(payer)

    transaction_builder.add(
        InstructionWithSigners(
            instruction=instruction,
            signers=[revoke_authority],
            key=params.instruction_key or "revoke_collection_authority",
        )
    )

    return transaction_builder
