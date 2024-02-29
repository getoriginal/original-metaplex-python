from src.metaplex.identity_module.plugin import identity_module
from src.metaplex.irys_storage.plugin import irys_storage
from src.metaplex.nft_module.plugin import nft_module
from src.metaplex.operation_module.plugin import operation_module
from src.metaplex.program_module.plugin import program_module
from src.metaplex.rpc_module.plugin import rpc_module
from src.metaplex.storage_module.plugin import storage_module
from src.metaplex.system_module.plugin import system_module
from src.metaplex.token_module.plugin import token_module


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
