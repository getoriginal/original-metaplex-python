from original_metaplex_python.metaplex.token_module.program import (
    associated_token_program,
    token_program,
)
from original_metaplex_python.metaplex.token_module.token_client import TokenClient


def token_module():
    def install(metaplex):
        metaplex.programs().register(token_program)
        metaplex.programs().register(associated_token_program)
        metaplex.programs().get_token = lambda programs: metaplex.programs().get(
            token_program.name, programs
        )
        metaplex.programs().get_associated_token = (
            lambda programs: metaplex.programs().get(
                associated_token_program.name, programs
            )
        )

        token_client = TokenClient(metaplex)
        metaplex.tokens = lambda: token_client

    return install
