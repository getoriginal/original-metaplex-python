from original_metaplex_python.metaplex.rpc_module.rpc_client import RpcClient


def rpc_module():
    def install(metaplex):
        rpc_client = RpcClient(metaplex)
        metaplex.rpc = lambda: rpc_client

    return install
