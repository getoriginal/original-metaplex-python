from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.delegate_type import (
    get_metadata_delegate_role_seed,
)
from original_metaplex_python.metaplex.types.pda import Pda
from original_metaplex_python.metaplex.types.program import Program


@dataclass
class MintAddressPdaInput:
    mint: Pubkey
    programs: Optional[list[Program]] = None


@dataclass
class TokenRecordPdaInput:
    mint: Pubkey
    token: Pubkey
    programs: Optional[list[Program]] = None


@dataclass
class CollectionAuthorityRecordPdaInput:
    mint: Pubkey
    collection_authority: Pubkey
    programs: Optional[list[Program]] = None


@dataclass
class MetadataDelegateRecordPdaInput:
    mint: Pubkey
    type: str
    update_authority: Pubkey
    delegate: Pubkey
    programs: Optional[list[Program]] = None


class NftPdasClient:
    def __init__(self, metaplex):
        self.metaplex = metaplex

    def metadata(self, params: MintAddressPdaInput):
        mint = params.mint
        programs = params.programs

        program_id = self.program_id(programs)
        return Pda.find(
            program_id,
            [
                bytes("metadata", "utf-8"),
                bytes(program_id),
                bytes(mint),
            ],
        )

    def master_edition(self, input: MintAddressPdaInput):
        mint = input.mint
        programs = input.programs

        program_id = self.program_id(programs)
        return Pda.find(
            program_id,
            [
                bytes("metadata", "utf-8"),
                bytes(program_id),
                bytes(mint),
                bytes("edition", "utf-8"),
            ],
        )

    def edition(self, input: MintAddressPdaInput):
        return self.master_edition(input)

    # TODO_ORIGINAL: Not used
    # def edition_marker(self, params: dict):
    #     mint = params.get('mint')
    #     programs = params.get('programs')
    #     edition = params.get('edition')
    #
    #     program_id = self.program_id(programs)
    #     return Pda.find(program_id, [
    #         bytes('metadata', 'utf-8'),
    #         bytes(program_id),
    #         bytes(mint),
    #         bytes('edition', 'utf-8'),
    #         bytes(str(edition // 248)),  # TODO: Check - Adjust division and conversion to string as per Python syntax
    #     ])

    def collection_authority_record(self, params: CollectionAuthorityRecordPdaInput):
        mint = params.mint
        programs = params.programs
        collection_authority = params.collection_authority

        program_id = self.program_id(programs)
        return Pda.find(
            program_id,
            [
                bytes("metadata", "utf-8"),
                bytes(program_id),
                bytes(mint),
                bytes("collection_authority", "utf-8"),
                bytes(collection_authority),
            ],
        )

    # TODO_ORIGINAL: Not used
    # def use_authority_record(self, params: dict):
    #     mint = params.get('mint')
    #     programs = params.get('programs')
    #     use_authority = params.get('use_authority')
    #
    #     program_id = self.program_id(programs)
    #     return Pda.find(program_id, [
    #         bytes('metadata', 'utf-8'),
    #         bytes(program_id),
    #         bytes(mint),
    #         bytes('user', 'utf-8'),
    #         bytes(use_authority),
    #     ])
    #
    # def burner(self, params: dict):
    #     programs = params.get('programs')
    #
    #     program_id = self.program_id(programs)
    #     return Pda.find(program_id, [
    #         bytes('metadata', 'utf-8'),
    #         bytes(program_id),
    #         bytes('burn', 'utf-8'),
    #     ])

    def token_record(self, params: TokenRecordPdaInput):
        mint = params.mint
        programs = params.programs
        token = params.token

        program_id = self.program_id(programs)
        return Pda.find(
            program_id,
            [
                bytes("metadata", "utf-8"),
                bytes(program_id),
                bytes(mint),
                bytes("token_record", "utf-8"),
                bytes(token),
            ],
        )

    def metadata_delegate_record(self, params: MetadataDelegateRecordPdaInput):
        mint = params.mint
        type = params.type
        update_authority = params.update_authority
        delegate = params.delegate
        programs = params.programs or None

        program_id = self.program_id(programs)
        return Pda.find(
            program_id,
            [
                bytes("metadata", "utf-8"),
                bytes(program_id),
                bytes(mint),
                bytes(get_metadata_delegate_role_seed(type), "utf-8"),
                bytes(update_authority),
                bytes(delegate),
            ],
        )

    def program_id(self, programs=None):
        return self.metaplex.programs().get_token_metadata(programs).address
