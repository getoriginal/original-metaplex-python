from typing import Optional

from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts

from original_metaplex_python.metaplex.types.operation import OperationOptions


class OperationClient:
    def __init__(self, metaplex):
        self.metaplex = metaplex
        self.operation_handlers = {}

    def register(self, operation_constructor, operation_handler):
        self.operation_handlers[operation_constructor.key] = operation_handler()
        return self

    def get(self, operation):
        operation_handler = self.operation_handlers[operation.key]
        return operation_handler

    def execute(self, operation, options=None):
        operation_handler = self.get(operation)

        # TODO_ORIGINAL scope not required. Used for JS async operations
        scope = {}

        return operation_handler.handle(
            operation, self.metaplex, self.get_operation_scope(options, scope)
        )

    def get_operation_scope(self, options: Optional[OperationOptions], scope):
        if options is None:
            options = OperationOptions()

        if options.commitment and not options.confirm_options:
            options.confirm_options = TxOpts(
                preflight_commitment=Commitment(options.commitment)
            )

        options.payer = options.payer or self.metaplex.rpc().get_default_fee_payer()

        return options
