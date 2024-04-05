from dataclasses import dataclass
from typing import Optional, cast

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
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
    verify,
)
from original_metaplex_python.token_metadata.generated.types.verification_args import (
    CreatorV1,
    VerificationArgsKind,
)


@dataclass
class VerifyNftCreatorBuilderParams:
    mint_address: Pubkey
    creator: Optional[Signer] = None
    instruction_key: Optional[str] = None


def verify_nft_creator_builder(
    metaplex,
    params: VerifyNftCreatorBuilderParams,
    options: Optional[TransactionBuilderOptions] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    mint_address = params.mint_address
    creator = params.creator or metaplex.identity()

    # Programs
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    transaction_builder = TransactionBuilder.make().set_fee_payer(payer)
    transaction_builder.add(
        InstructionWithSigners(
            instruction=verify(
                accounts=VerifyAccounts(
                    authority=get_public_key(creator),
                    metadata=metaplex.nfts()
                    .pdas()
                    .metadata(
                        MintAddressPdaInput(mint=mint_address, programs=programs)
                    ),
                    sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                    delegate_record=None,
                    collection_mint=None,
                    collection_metadata=None,
                    collection_master_edition=None,
                ),
                args=VerifyArgs(
                    verification_args=cast(VerificationArgsKind, CreatorV1())
                ),
                program_id=token_metadata_program.address,
            ),
            signers=[creator],
            key=params.instruction_key or "verify_creator",
        )
    )

    return transaction_builder
