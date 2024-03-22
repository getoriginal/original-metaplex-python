from dataclasses import dataclass
from typing import Optional, Union, cast

from solders.instruction import AccountMeta
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.models.metadata import (
    is_non_fungible_token_standard,
)
from original_metaplex_python.metaplex.nft_module.models.sft import Sft, SftWithToken
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.nft_module.operations.mint_nft import (
    MintNftBuilderParams,
    NftOrSft,
)
from original_metaplex_python.metaplex.nft_module.operations.verify_nft_collection import (
    VerifyNftCollectionBuilderParams,
)
from original_metaplex_python.metaplex.rpc_module.rpc_client import (
    SendAndConfirmTransactionResponse,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.amount import SplTokenAmount
from original_metaplex_python.metaplex.types.creator import CreatorInput
from original_metaplex_python.metaplex.types.signer import (
    Signer,
    get_public_key,
    is_signer,
)
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    CreateAccounts,
    CreateArgs,
    create,
)
from original_metaplex_python.token_metadata.generated.types import (
    AssetData,
    Collection,
    Creator,
    Uses,
)
from original_metaplex_python.token_metadata.generated.types.collection_details import (
    V1 as CollectionDetailsV1,
)
from original_metaplex_python.token_metadata.generated.types.collection_details import (
    V1Value as CollectionDetailsV1Value,
)
from original_metaplex_python.token_metadata.generated.types.create_args import (
    V1 as CreateArgsV1,
)
from original_metaplex_python.token_metadata.generated.types.create_args import (
    V1Value as CreateArgsV1Value,
)
from original_metaplex_python.token_metadata.generated.types.print_supply import (
    Limited,
    PrintSupplyKind,
    Unlimited,
    Zero,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    ProgrammableNonFungible,
    TokenStandardKind,
)


@dataclass
class CreateSftInput:
    uri: str
    name: str
    seller_fee_basis_points: int
    update_authority: Optional[Signer] = None
    mint_authority: Optional[Signer] = None
    use_new_mint: Optional[Keypair] = None
    use_existing_mint: Optional[Pubkey] = None
    token_owner: Optional[Pubkey] = None
    token_address: Optional[Pubkey] = None
    token_amount: Optional[SplTokenAmount] = None
    decimals: Optional[int] = None
    token_standard: Optional[TokenStandardKind] = None
    symbol: Optional[str] = None
    creators: Optional[list[CreatorInput]] = None
    is_mutable: Optional[bool] = None
    max_supply: Optional[tuple[int]] = None
    primary_sale_happened: Optional[bool] = None
    uses: Optional[Uses] = None
    is_collection: Optional[bool] = None
    collection: Optional[Pubkey] = None
    collection_authority: Optional[Signer] = None
    collection_authority_is_delegated: Optional[bool] = None
    collection_is_sized: Optional[bool] = None
    rule_set: Optional[Pubkey] = None


@dataclass
class CreateSftOutput:
    response: SendAndConfirmTransactionResponse
    sft: Sft | SftWithToken
    mint_address: Pubkey
    metadata_address: Pubkey
    tokenAddress: Pubkey | None


@dataclass
class CreateSftBuilderParams(CreateSftInput):
    token_exists: Optional[bool] = True
    create_mint_account_instruction_key: Optional[str] = None
    initialize_mint_instruction_key: Optional[str] = None
    create_token_account_instruction_key: Optional[str] = None
    initialize_token_instruction_key: Optional[str] = None
    mint_tokens_instruction_key: Optional[str] = None
    create_instruction_key: Optional[str] = None


@dataclass
class CreateSftBuilderContext:
    mint_address: Pubkey
    metadata_address: Pubkey
    token_address: Union[Pubkey, None]


def create_sft_builder(
    metaplex,
    params: CreateSftBuilderParams,
    options: Optional[TransactionBuilderOptions] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    use_new_mint = params.use_new_mint or Keypair()
    update_authority = params.update_authority or metaplex.identity()
    mint_authority = params.mint_authority or metaplex.identity()
    token_standard = params.token_standard or cast(
        TokenStandardKind, ProgrammableNonFungible
    )

    mint_address = params.use_existing_mint or get_public_key(use_new_mint)
    associated_token_address = None
    if params.token_owner:
        associated_token_address = (
            metaplex.tokens()
            .pdas()
            .associated_token_account(
                AssociatedTokenAccountOptions(
                    mint=mint_address, owner=params.token_owner, programs=programs
                )
            )
        )

    token_address = params.token_address or associated_token_address

    token_program = metaplex.programs().get_token(programs)
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=mint_address, programs=programs))
    )

    master_edition = (
        metaplex.nfts()
        .pdas()
        .master_edition(MintAddressPdaInput(mint=mint_address, programs=programs))
    )

    update_authority_pubkey = get_public_key(update_authority)
    mint_authority_pubkey = get_public_key(mint_authority)
    payer_pubkey = get_public_key(payer)

    creators_input: list[CreatorInput] = params.creators or [
        CreatorInput(
            address=update_authority_pubkey, authority=update_authority, share=100
        )
    ]

    creators = None
    if len(creators_input) > 0:
        creators = [
            Creator(
                address=creator.address,
                share=creator.share,
                verified=creator.address == update_authority_pubkey,
            )
            for creator in creators_input
        ]

    print_supply: PrintSupplyKind | None = None
    if is_non_fungible_token_standard(token_standard):
        # TODO_ORIGINAL: Note in JS they check if undefined, use Zero, or if null use Unlimited. We cannot do that in python so use -1.
        if params.max_supply is None:
            print_supply = Zero()
        elif params.max_supply == -1:
            print_supply = Unlimited()
        elif params.max_supply is not None:
            print_supply = Limited(value=params.max_supply)

    create_instruction = create(
        accounts=CreateAccounts(
            metadata=metadata,
            master_edition=(
                master_edition
                if is_non_fungible_token_standard(token_standard)
                else None
            ),
            mint=mint_address,
            authority=mint_authority_pubkey,
            payer=payer_pubkey,
            update_authority=update_authority_pubkey,
            sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
            spl_token_program=token_program.address,
        ),
        args=CreateArgs(
            create_args=CreateArgsV1(
                value=CreateArgsV1Value(
                    asset_data=AssetData(
                        name=params.name,
                        symbol=params.symbol or "",
                        uri=params.uri,
                        seller_fee_basis_points=params.seller_fee_basis_points,
                        creators=creators,
                        primary_sale_happened=params.primary_sale_happened or False,
                        is_mutable=params.is_mutable or True,
                        token_standard=token_standard,
                        collection=(
                            Collection(key=params.collection, verified=False)
                            if params.collection
                            else None
                        ),
                        uses=params.uses,
                        collection_details=(
                            CollectionDetailsV1(value=CollectionDetailsV1Value(size=0))
                            if params.is_collection
                            else None
                        ),
                        rule_set=params.rule_set or None,
                    ),
                    decimals=params.decimals or 0,
                    print_supply=print_supply if print_supply else None,
                )
            )
        ),
        program_id=token_metadata_program.address,
    )

    create_signers = [payer, mint_authority, update_authority]
    if not params.use_existing_mint:
        create_signers.append(use_new_mint)

        old_accounts = create_instruction.accounts
        # create the new accounts list from the existing accounts with the new mint account at index 2:
        new_mint_account = AccountMeta(
            pubkey=get_public_key(use_new_mint), is_signer=True, is_writable=True
        )
        create_instruction.accounts = (
            old_accounts[:2] + [new_mint_account] + old_accounts[3:]
        )

    # When the payer is different than the update authority, the latter will
    # not be marked as a signer and therefore signing as a creator will fail.
    old_accounts = create_instruction.accounts
    new_update_authority_account = AccountMeta(
        pubkey=update_authority_pubkey, is_signer=True, is_writable=False
    )
    create_instruction.accounts = (
        old_accounts[:5] + [new_update_authority_account] + old_accounts[6:]
    )

    create_non_ata_instruction = None
    if (
        not params.token_exists
        and params.token_address
        and is_signer(params.token_address)
    ):
        create_non_ata_instruction = (
            metaplex.tokens()
            .builders()
            .create_token(
                {
                    "mint": mint_address,
                    "owner": params.token_owner,
                    "token": params.token_address,
                    "create_account_instruction_key": params.create_token_account_instruction_key,
                    "initialize_token_instruction_key": params.initialize_token_instruction_key,
                },
                {"programs": programs, "payer": payer},
            )
        )

    mint_instruction = None
    if token_address and params.token_amount:
        mint_instruction = (
            metaplex.nfts()
            .builders()
            .mint(
                MintNftBuilderParams(
                    nft_or_sft=NftOrSft(
                        address=mint_address, token_standard=token_standard
                    ),
                    authority=(
                        update_authority
                        if is_non_fungible_token_standard(token_standard)
                        else mint_authority
                    ),
                    to_owner=params.token_owner,
                    to_token=token_address,
                    amount=params.token_amount,
                ),
                TransactionBuilderOptions(programs=programs, payer=payer),
            )
        )

    verify_additional_creator_instructions = [
        metaplex.nfts()
        .builders()
        .verify_creator(
            {"mintAddress": mint_address, "creator": creator.authority},
            {"programs": programs, "payer": payer},
        )
        for creator in creators_input
        if creator.authority and creator.address != update_authority_pubkey
    ]

    transaction_builder = (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .set_context(
            {
                "mintAddress": mint_address,
                "metadataAddress": metadata,
                "tokenAddress": token_address,
            }
        )
        .add(
            # Create metadata / edition accounts.
            InstructionWithSigners(
                instruction=create_instruction,
                signers=create_signers,
                key=params.create_instruction_key or "create_metadata",
            )
        )
    )

    # Create the non-associated token account if needed.
    if create_non_ata_instruction:
        transaction_builder.add(create_non_ata_instruction)

    # Mint provided amount to the token account, if any
    if mint_instruction:
        transaction_builder.add(mint_instruction)

    # Verify additional creators
    for instruction in verify_additional_creator_instructions:
        transaction_builder.add(instruction)

    # Verify collection
    should_verify_collection = params.collection and params.collection_authority
    transaction_builder.when(
        should_verify_collection,
        lambda builder: builder.add(
            metaplex.nfts()
            .builders()
            .verify_collection(
                VerifyNftCollectionBuilderParams(
                    mint_address=mint_address,
                    collection_mint_address=cast(Pubkey, params.collection),
                    collection_authority=params.collection_authority,
                    is_delegated=params.collection_authority_is_delegated or False,
                    is_sized_collection=params.collection_is_sized or True,
                ),
                TransactionBuilderOptions(programs=programs, payer=payer),
            )
        ),
    )

    return transaction_builder
