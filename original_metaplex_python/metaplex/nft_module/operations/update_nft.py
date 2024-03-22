from dataclasses import asdict, dataclass
from typing import Optional, cast

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.authorization import (
    ParsedTokenMetadataAuthorization,
    TokenMetadataAuthority,
    TokenMetadataAuthorityMetadata,
    TokenMetadataAuthorization,
    TokenMetadataAuthorizationDetails,
    parse_token_metadata_authorization,
)
from original_metaplex_python.metaplex.nft_module.models.metadata import (
    Collection,
    is_non_fungible,
)
from original_metaplex_python.metaplex.nft_module.models.sft import Sft
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.nft_module.operations.unverify_nft_collection import (
    UnverifyNftCollectionBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.verify_nft_collection import (
    VerifyNftCollectionBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.verify_nft_creator import (
    VerifyNftCreatorBuilderParams,
)
from original_metaplex_python.metaplex.types.creator import CreatorInput
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    UpdateAccounts,
    UpdateArgs,
    update,
)
from original_metaplex_python.token_metadata.generated.types import (
    Collection as TokenMetadataCollection,
)
from original_metaplex_python.token_metadata.generated.types import Data
from original_metaplex_python.token_metadata.generated.types.update_args import (
    from_decoded,
)

TOKEN_AUTH_RULES_ID = Pubkey.from_string("auth9SigNpDKz4sJJ1DfCTuZrZNSAgh9sFD3rboVmgg")


@dataclass
class NftOrSft(Sft):
    pass


@dataclass
class UpdateNftBuilderParams:
    nft_or_sft: NftOrSft
    update_authority: Optional[Signer] = None
    authority: Optional[Signer | TokenMetadataAuthority] = None
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None
    new_update_authority: Optional[Pubkey] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    uri: Optional[str] = None
    seller_fee_basis_points: Optional[int] = None
    creators: Optional[list[CreatorInput]] = None
    primary_sale_happened: Optional[bool] = None
    is_mutable: Optional[bool] = None
    uses: Optional[str] = None
    collection: Optional[Pubkey] = None
    rule_set: Optional[str] = None
    collection_authority: Optional[Signer] = None
    collection_authority_is_delegated: Optional[bool] = None
    collection_is_sized: Optional[bool] = None
    old_collection_authority: Optional[Signer] = None
    old_collection_is_sized: Optional[bool] = None
    collection_details: Optional[str] = None
    update_metadata_instruction_key: Optional[str] = None


def update_nft_builder(
    metaplex,
    params: UpdateNftBuilderParams,
    options: Optional[TransactionBuilderOptions] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    nft_or_sft = params.nft_or_sft
    authority = params.authority or metaplex.identity().public_key
    authorization_details = params.authorization_details

    # Programs
    token_metadata_program = metaplex.programs().get_token_metadata(programs)

    update_instruction_data_without_changes = to_instruction_data(nft_or_sft)
    update_instruction_data = to_instruction_data(nft_or_sft, params)
    should_send_update_instruction = (
        update_instruction_data != update_instruction_data_without_changes
    )

    is_removing_verified_collection = bool(
        nft_or_sft.collection
        and nft_or_sft.collection.verified
        and params.collection
        == "Clear"  # TODO_ORIGINAL - In JS, we check against null. Check against Clear so its explicit
    )
    is_overriding_verified_collection = bool(
        nft_or_sft.collection
        and nft_or_sft.collection.verified
        and params.collection
        and params.collection != nft_or_sft.collection.address
    )
    should_unverify_current_collection = (
        is_removing_verified_collection or is_overriding_verified_collection
    )

    authority = (
        authority
        if isinstance(authority, TokenMetadataAuthorityMetadata)
        else TokenMetadataAuthorityMetadata(update_authority=cast(Signer, authority))
    )

    # Auth
    auth: ParsedTokenMetadataAuthorization = parse_token_metadata_authorization(
        metaplex,
        TokenMetadataAuthorization(
            mint=nft_or_sft.address,
            authority=authority,
            authorization_details=authorization_details,
            programs=programs,
        ),
    )

    creators_input: list[CreatorInput] = params.creators if params.creators else []
    if not creators_input:
        for creator in nft_or_sft.creators:
            creators_input.append(
                CreatorInput(
                    address=creator.address,
                    share=creator.share,
                    verified=creator.verified,
                    authority=None,
                )
            )

    filtered_creators_input: list[CreatorInput] = []
    for creator_input in creators_input:
        current_creator = next(
            (c for c in nft_or_sft.creators if c.address == creator_input.address), None
        )
        currently_verified = current_creator.verified if current_creator else False
        if creator_input.authority and not currently_verified:
            filtered_creators_input.append(creator_input)

    verify_additional_creator_instructions = []
    for creator_input in filtered_creators_input:
        verify_additional_creator_instructions.append(
            metaplex.nfts()
            .builders()
            .verify_creator(
                VerifyNftCreatorBuilderParams(
                    mint_address=nft_or_sft.address,
                    creator=creator_input.authority,
                ),
                TransactionBuilderOptions(payer=payer, programs=programs),
            )
        )

    return (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .when(
            should_unverify_current_collection,
            lambda builder: builder.add(
                metaplex.nfts()
                .builders()
                .unverify_collection(
                    UnverifyNftCollectionBuilderParams(
                        mint_address=nft_or_sft.address,
                        collection_mint_address=cast(
                            Collection, nft_or_sft.collection
                        ).address,
                        collection_authority=params.old_collection_authority or payer,
                        is_sized_collection=params.old_collection_is_sized or True,
                    ),
                    TransactionBuilderOptions(payer=payer, programs=programs),
                )
            ),
        )
        .when(
            should_send_update_instruction,
            lambda builder: builder.add(
                # Update the metadata account.
                InstructionWithSigners(
                    instruction=update(
                        accounts=UpdateAccounts(
                            authority=auth.accounts.authority,
                            delegate_record=auth.accounts.delegate_record,
                            token=auth.accounts.token,
                            mint=nft_or_sft.address,
                            metadata=metaplex.nfts()
                            .pdas()
                            .metadata(
                                MintAddressPdaInput(
                                    mint=nft_or_sft.address, programs=programs
                                )
                            ),
                            edition=(
                                metaplex.nfts()
                                .pdas()
                                .master_edition(
                                    MintAddressPdaInput(
                                        mint=nft_or_sft.address, programs=programs
                                    )
                                )
                                if is_non_fungible(nft_or_sft)
                                else None
                            ),
                            payer=get_public_key(payer),
                            sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                            authorization_rules=auth.accounts.authorization_rules,
                            authorization_rules_program=TOKEN_AUTH_RULES_ID,
                        ),
                        args=UpdateArgs(
                            update_args=from_decoded(
                                {"V1": {**update_instruction_data, **asdict(auth.data)}}
                            )
                        ),
                        program_id=token_metadata_program.address,
                    ),
                    signers=[payer, *auth.signers],
                    key=params.update_metadata_instruction_key or "update_metadata",
                )
            ),
        )
        .add(*verify_additional_creator_instructions)
        .when(
            # Verify collection.
            params.collection and params.collection_authority,
            lambda builder: builder.add(
                metaplex.nfts()
                .builders()
                .verify_collection(
                    VerifyNftCollectionBuilderParams(
                        mint_address=nft_or_sft.address,
                        collection_mint_address=cast(Pubkey, params.collection),
                        collection_authority=params.collection_authority,
                        is_delegated=params.collection_authority_is_delegated or False,
                        is_sized_collection=params.collection_is_sized or True,
                    ),
                    TransactionBuilderOptions(payer=payer, programs=programs),
                )
            ),
        )
    )


def to_instruction_data(nft_or_sft, input: Optional[UpdateNftBuilderParams] = None):
    if input is None:
        input = UpdateNftBuilderParams(nft_or_sft=nft_or_sft)

    if input.creators is None:
        creators = nft_or_sft.creators
    else:
        mapped_creators = []
        for creator in input.creators:
            current_creator = next(
                (c for c in nft_or_sft.creators if c.address == creator.address), None
            )
            verified = current_creator.verified if current_creator else False
            mapped_creator = CreatorInput(
                address=creator.address, share=creator.share, verified=verified
            )
            mapped_creators.append(mapped_creator)
        creators = mapped_creators

    return {
        "__kind": "V1",
        "new_update_authority": input.new_update_authority,
        "data": Data(
            name=input.name or nft_or_sft.name,
            symbol=input.symbol or nft_or_sft.symbol,
            uri=input.uri or nft_or_sft.uri,
            seller_fee_basis_points=input.seller_fee_basis_points
            or nft_or_sft.seller_fee_basis_points,
            creators=creators if creators else None,
        ),
        "primary_sale_happened": input.primary_sale_happened,
        "is_mutable": input.is_mutable,
        "collection": (
            {
                "__kind": "Set",
                "Set": {
                    "item_0": TokenMetadataCollection(
                        key=input.collection, verified=False
                    )
                },
            }
            if input.collection
            else {"Clear": ""} if input.collection == "Clear" else {"None": ""}
        ),  # TODO_ORIGINAL: Added explicit check for Clear
        "collection_details": (
            {"__kind": "Set", "fields": [input.collection_details]}
            if input.collection_details
            else {"None": ""}
        ),
        "uses": (
            {"__kind": "Set", "fields": [input.uses]}
            if input.uses
            else {"None": ""} if input.uses is None else {"Clear": ""}
        ),
        "rule_set": (
            {"__kind": "Set", "fields": [input.rule_set]}
            if input.rule_set
            else {"None": ""} if input.rule_set is None else {"Clear": ""}
        ),
    }
