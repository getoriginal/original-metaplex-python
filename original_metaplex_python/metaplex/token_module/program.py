from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID

from original_metaplex_python.metaplex.types.program import Program

token_program: Program = Program()
token_program.name = "TokenProgram"
token_program.address = TOKEN_PROGRAM_ID

associated_token_program: Program = Program()
associated_token_program.name = "AssociatedTokenProgram"
associated_token_program.address = ASSOCIATED_TOKEN_PROGRAM_ID
