from dataclasses import dataclass
from typing import Any, Optional

from solana.rpc.types import TxOpts

from original_metaplex_python.metaplex.types.signer import Signer


def make_confirm_options_finalized_on_mainnet(metaplex, options=None):
    if metaplex.cluster == "mainnet-beta":
        if options is None:
            options = {}
        options["commitment"] = "finalized"
    return options


@dataclass
class Operation:
    key: str
    input: Any


@dataclass
class OperationOptions:
    payer: Optional[Signer] = None
    commitment: Optional[str] = None
    confirm_options: Optional[TxOpts] = None
    programs: Optional[Any] = None
    signal: Optional[Any] = None


def use_operation(key):
    def constructor(input):
        return Operation(
            key=key,
            input=input,
        )

    constructor.key = key
    return constructor
