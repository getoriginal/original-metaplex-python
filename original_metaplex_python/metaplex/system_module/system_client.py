# Assuming the necessary imports and dependencies are handled elsewhere
from original_metaplex_python.metaplex.system_module.system_builders_client import (
    SystemBuildersClient,
)


class SystemClient:
    """
    This is a client for the System module.

    It enables us to interact with the System program in order to
    create uninitialized accounts and transfer SOL.

    You may access this client via the `system()` method of your `Metaplex` instance.

    Example:
    You can create a new uninitialized account with a given space in bytes
    using the code below.

    Example Usage:
        system_client = metaplex.system()
        new_account = system_client.create_account({'space': 42})
    """

    def __init__(self, metaplex):
        self.metaplex = metaplex

    def builders(self):
        """
        You may use the `builders()` client to access the
        underlying Transaction Builders of this module.

        Example Usage:
            builders_client = metaplex.system().builders()
        """
        return SystemBuildersClient(self.metaplex)

    def create_account(self, input, options=None):
        """
        Create a new account.

        :param input: CreateAccountInput
        :param options: OperationOptions (optional)
        :return: Result of the create account operation
        """
        raise NotImplementedError("create_account")
        # TODO_ORIGINAL: This flow is not used
        # return self.metaplex.operations().execute(
        #     create_account_operation(input), options
        # )

    def transfer_sol(self, input, options=None):
        """
        Transfer SOL.

        :param input: TransferSolInput
        :param options: OperationOptions (optional)
        :return: Result of the transfer SOL operation
        """
        raise NotImplementedError("transfer_sol")
        # TODO_ORIGINAL: This flow is not used
        # return self.metaplex.operations().execute(
        #     transfer_sol_operation(input), options
        # )
