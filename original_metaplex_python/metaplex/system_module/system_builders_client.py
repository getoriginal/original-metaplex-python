# from original_metaplex_python.metaplex.system_module.operations.create_account import create_account_builder


class SystemBuildersClient:
    """
    This client allows you to access the underlying Transaction Builders
    for the write operations of the System module.

    See: SystemClient
    Group: Module Builders
    """

    def __init__(self, metaplex):
        self.metaplex = metaplex

    def create_account(self, input, options=None):
        raise NotImplementedError("create_account")
        """
        Access the createAccountBuilder.

        :param input: CreateAccountBuilderParams
        :param options: TransactionBuilderOptions (optional)
        :return: Result of the create account builder
        """
        # TODO_ORIGINAL: This flow is not used
        # return create_account_builder(self.metaplex, input, options)

    def transfer_sol(self, input, options=None):
        """
        Access the transferSolBuilder.

        :param input: TransferSolBuilderParams
        :param options: TransactionBuilderOptions (optional)
        :return: Result of the transfer SOL builder
        """
        raise NotImplementedError("transfer_sol")
        # TODO_ORIGINAL: This flow is not used
        # return transfer_sol_builder(self.metaplex, input, options)
