from enum import Enum
from urllib.parse import urlparse

from solana.rpc.api import Client


class Cluster(Enum):
    MAINNET_BETA = "mainnet-beta"
    DEVNET = "devnet"
    TESTNET = "testnet"
    LOCALNET = "localnet"
    CUSTOM = "custom"


MAINNET_BETA_DOMAINS = [
    "api.mainnet-beta.solana.com",
    "ssc-dao.genesysgo.net",
]
DEVNET_DOMAINS = [
    "api.devnet.solana.com",
    "psytrbhymqlkfrhudd.dev.genesysgo.net",
]
TESTNET_DOMAINS = ["api.testnet.solana.com"]
LOCALNET_DOMAINS = ["localhost", "127.0.0.1"]


def resolve_cluster_from_connection(connection: Client):
    return resolve_cluster_from_endpoint(connection._provider.endpoint_uri)


def resolve_cluster_from_endpoint(endpoint):
    domain = urlparse(endpoint).hostname
    if domain in MAINNET_BETA_DOMAINS:
        return "mainnet-beta"
    if domain in DEVNET_DOMAINS:
        return "devnet"
    if domain in TESTNET_DOMAINS:
        return "testnet"
    if domain in LOCALNET_DOMAINS:
        return "localnet"
    return "custom"
