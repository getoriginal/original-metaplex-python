from typing import Optional

from ..types.operation import OperationOptions
from .nft_builders_client import NftBuildersClient
from .nft_pdas_client import NftPdasClient
from .operations.find_nft_by_mint import FindNftByMintInput, find_nft_by_mint_operation


class NftClient:
    def __init__(self, metaplex):
        self.metaplex = metaplex

    def builders(self):
        return NftBuildersClient(self.metaplex)

    def pdas(self):
        return NftPdasClient(self.metaplex)

    def find_by_mint(
        self, input: FindNftByMintInput, options: Optional[OperationOptions] = None
    ):
        return self.metaplex.operations().execute(
            find_nft_by_mint_operation(input), options
        )
