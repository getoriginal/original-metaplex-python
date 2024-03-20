from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    TokenPdasClient,
)


class TokenClient:
    def __init__(self, metaplex):
        self.metaplex = metaplex

    def pdas(self):
        return TokenPdasClient(self.metaplex)
