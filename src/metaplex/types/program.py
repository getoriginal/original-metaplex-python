from dataclasses import dataclass
from typing import Any, Callable

from solders.pubkey import Pubkey


@dataclass
class ErrorWithLogs:
    logs: list[str]


@dataclass
class ErrorWithCode:
    code: int


def is_error_with_logs(error):
    return isinstance(error, Exception) and hasattr(error, "logs")


class Program:
    name: str
    address: Pubkey
    error_resolver: Callable[[Any], None]

    # TODO_ORIGINAL These are interfaces that might be defined or not dynamically
    # def cluster_filter(self, cluster: Cluster) -> bool:
    #     pass
    #
    # def error_resolver(self, error: ErrorWithLogs) -> ErrorWithCode | None:
    #     pass
    #
    # def gpa_resolver(self, metaplex):  # -> GpaBuilder:
    #     pass
