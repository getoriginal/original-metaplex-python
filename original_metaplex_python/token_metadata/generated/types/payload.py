from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class PayloadJSON(typing.TypedDict):
    map: bool


@dataclass
class Payload:
    layout: typing.ClassVar = borsh.CStruct("map" / borsh.Bool)
    map: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "Payload":
        return cls(map=obj.map)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"map": self.map}

    def to_json(self) -> PayloadJSON:
        return {"map": self.map}

    @classmethod
    def from_json(cls, obj: PayloadJSON) -> "Payload":
        return cls(map=obj["map"])
