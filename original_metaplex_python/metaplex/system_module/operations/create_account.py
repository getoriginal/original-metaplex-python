# from solders import system_program
# from solders.keypair import Keypair
# from solders.system_program import CreateAccountParams
#
# from original_metaplex_python.metaplex.types.amount import assert_sol
# from original_metaplex_python.metaplex.utils.transaction_builder import TransactionBuilder

# TODO_ORIGINAL: This flow is not used

# class CreateAccountOperationHandler:
#     def handle(self, operation, metaplex, scope
#     ):
#       builder = create_account_builder(
#         metaplex,
#         operation.input,
#         scope
#       );
#       scope.throwIfCanceled()
#       return builder.send_and_confirm(metaplex, scope.confirmOptions);


# class CreateAccountParams(TypedDict):
#     """Create account system transaction params."""
#
#     from_pubkey: Pubkey
#     """The account that will transfer lamports to the created account."""
#     to_pubkey: Pubkey
#     """Pubkey of the created account."""
#     lamports: int
#     """Amount of lamports to transfer to the created account."""
#     space: int
#     """Amount of space in bytes to allocate to the created account."""
#     owner: Pubkey
#     """Pubkey of the program to assign as the owner of the created account."""


# def create_account_builder(metaplex, params: CreateAccountParams, options=None):
#     """
#     Creates a new uninitialized Solana account.
#
#     Example:
#         transaction_builder = await metaplex.system().builders().create_account({'space': 100})
#
#     Note that accessing this transaction builder is asynchronous
#     because we may need to contact the cluster to get the
#     rent-exemption for the provided space.
#
#     Group: Transaction Builders
#     Category: Constructors
#     """
#     options = options or {}
#     payer = options.get('payer', metaplex.rpc().get_default_fee_payer())
#     space = params.get('space')
#     new_account = params.get('newAccount', Keypair())
#     program = params.get('program', system_program.ID)
#
#     lamports = params.get('lamports')
#     if lamports is None:
#         lamports = metaplex.rpc().get_rent(space)
#
#     # Replace assertSol with appropriate validation in Python
#     assert_sol(lamports)
#
#     transaction_builder = TransactionBuilder.make().set_fee_payer(payer).set_context({
#         'newAccount': new_account,
#         'lamports': lamports
#     })
#
#     CreateAccountParams(
#         from_pubkey=payer.publicKey,
#         to_pubkey=newAccount.publicKey,
#         space=space,
#         lamports=lamports,
#         owner=program
#     )
#     transaction_builder.add({
#         'instruction': system_program.create_account({
#             'fromPubkey': payer.publicKey,
#             'newAccountPubkey': newAccount.publicKey,
#             'space': space,
#             'lamports': lamports,  # Adjust this if lamports is not a direct number
#             'programId': program,
#         }),
#         'signers': [payer, newAccount],
#         'key': params.get('instructionKey', 'createAccount'),
#     })
#
#     return transaction_builder
