from original_metaplex_python.metaplex.identity_module.plugin import identity_module
from original_metaplex_python.metaplex.irys_storage.plugin import irys_storage
from original_metaplex_python.metaplex.nft_module.plugin import nft_module
from original_metaplex_python.metaplex.operation_module.plugin import operation_module
from original_metaplex_python.metaplex.program_module.plugin import program_module
from original_metaplex_python.metaplex.rpc_module.plugin import rpc_module
from original_metaplex_python.metaplex.storage_module.plugin import storage_module
from original_metaplex_python.metaplex.system_module.plugin import system_module
from original_metaplex_python.metaplex.token_module.plugin import token_module


def core_plugins():
    def install(metaplex):
        # Low-level modules.
        metaplex.use(identity_module())
        metaplex.use(storage_module())
        metaplex.use(rpc_module())
        metaplex.use(operation_module())
        metaplex.use(program_module())
        # TODO_ORIGINAL - Commented out unused modules
        # metaplex.use(utilsModule())

        # Default drivers.
        # metaplex.use(guestIdentity())
        metaplex.use(irys_storage())

        # Verticals.
        metaplex.use(system_module())
        metaplex.use(token_module())
        metaplex.use(nft_module())
        # metaplex.use(candyMachineV2Module());
        # metaplex.use(candyMachineModule());
        # metaplex.use(auctionHouseModule());

    return install
