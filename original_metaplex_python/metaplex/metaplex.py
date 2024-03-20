from dataclasses import dataclass
from typing import Optional

from solana.rpc.api import Client

from .core_plugins.plugin import core_plugins
from .types.cluster import Cluster, resolve_cluster_from_connection


@dataclass
class MetaplexOptions:
    cluster: Optional[Cluster]


class Metaplex:
    def __init__(self, connection: Client, options: Optional[MetaplexOptions] = None):
        self.connection = connection
        self.cluster = (
            options.cluster if options else resolve_cluster_from_connection(connection)
        )
        self.use(core_plugins())

    @staticmethod
    def make(connection: Client, options: Optional[MetaplexOptions] = None):
        return Metaplex(connection, options)

    def use(self, plugin):
        plugin(self)
        return self
