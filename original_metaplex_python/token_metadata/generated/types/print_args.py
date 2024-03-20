from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class V1JSONValue(typing.TypedDict):
    edition: int


class V1Value(typing.TypedDict):
    edition: int


class V1JSON(typing.TypedDict):
    value: V1JSONValue
    kind: typing.Literal["V1"]


@dataclass
class V1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "V1"
    value: V1Value

    def to_json(self) -> V1JSON:
        return V1JSON(
            kind="V1",
            value={
                "edition": self.value["edition"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "edition": self.value["edition"],
            },
        }


PrintArgsKind = typing.Union[V1]
PrintArgsJSON = typing.Union[V1JSON]


def from_decoded(obj: dict) -> PrintArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                edition=val["edition"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: PrintArgsJSON) -> PrintArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                edition=v1json_value["edition"],
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("V1" / borsh.CStruct("edition" / borsh.U64))
