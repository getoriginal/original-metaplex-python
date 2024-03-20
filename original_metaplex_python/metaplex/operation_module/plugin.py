from original_metaplex_python.metaplex.operation_module.operation_client import (
    OperationClient,
)


def operation_module():
    def install(metaplex):
        operation_client = OperationClient(metaplex)
        metaplex.operations = lambda: operation_client

    return install
