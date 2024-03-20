from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.types.pda import Pda
from original_metaplex_python.metaplex.types.program import Program


@dataclass
class AssociatedTokenAccountOptions:
    mint: Pubkey
    owner: Pubkey
    programs: Optional[list[Program]] = None


class TokenPdasClient:
    """
    This client allows you to build PDAs related to the Token module.

    See: TokenClient
    Group: Module Pdas
    """

    def __init__(self, metaplex):
        self.metaplex = metaplex

    def associated_token_account(self, options: AssociatedTokenAccountOptions):
        """
        Finds the address of the Associated Token Account.

        Parameters:
        mint: PublicKey - The address of the mint account.
        owner: PublicKey - The address of the owner account.
        programs: list[Program] (optional) - A set of programs that override the registered ones.
        """

        mint = options.mint
        owner = options.owner
        programs = options.programs

        token_program = self.metaplex.programs().get_token(programs)
        associated_token_program = self.metaplex.programs().get_associated_token(
            programs
        )

        return Pda.find(
            associated_token_program.address,
            [
                bytes(owner),
                bytes(token_program.address),
                bytes(mint),
            ],
        )
