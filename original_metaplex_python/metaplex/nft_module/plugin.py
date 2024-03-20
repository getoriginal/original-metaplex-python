from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.nft_client import NftClient
from original_metaplex_python.metaplex.nft_module.operations.find_nft_by_mint import (
    FindNftByMintOperationHandler,
    find_nft_by_mint_operation,
)
from original_metaplex_python.metaplex.types.program import Program

token_metadata_program = Program()
token_metadata_program.name = "TokenMetadataProgram"
token_metadata_program.address = Pubkey.from_string(
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
)
token_metadata_program.error_resolver = lambda error: print(error)


def nft_module():
    def install(metaplex):
        metaplex.programs().register(token_metadata_program)
        metaplex.programs().get_token_metadata = (
            lambda programs: metaplex.programs().get(
                token_metadata_program.name, programs
            )
        )

        nft_client = NftClient(metaplex)
        metaplex.nfts = lambda: nft_client

        op = metaplex.operations()

        op.register(find_nft_by_mint_operation, FindNftByMintOperationHandler)

    return install
