from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class TransferOutOfEscrowArgsJSON(typing.TypedDict):
    amount: int


@dataclass
class TransferOutOfEscrowArgs:
    layout: typing.ClassVar = borsh.CStruct("amount" / borsh.U64)
    amount: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "TransferOutOfEscrowArgs":
        return cls(amount=obj.amount)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"amount": self.amount}

    def to_json(self) -> TransferOutOfEscrowArgsJSON:
        return {"amount": self.amount}

    @classmethod
    def from_json(cls, obj: TransferOutOfEscrowArgsJSON) -> "TransferOutOfEscrowArgs":
        return cls(amount=obj["amount"])
