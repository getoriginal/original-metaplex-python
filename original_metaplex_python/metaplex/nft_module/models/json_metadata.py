from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from original_metaplex_python.token_metadata.generated.types import Creator


@dataclass
class Attribute:
    trait_type: Optional[str] = None
    value: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class File:
    type: Optional[str] = None
    uri: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Properties:
    creators: Optional[List[Creator]] = None
    files: Optional[List[File]] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectionInfo:
    name: Optional[str] = None
    family: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JsonMetadata:
    name: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    seller_fee_basis_points: Optional[int] = None
    image: Optional[str] = None
    animation_url: Optional[str] = None
    external_url: Optional[str] = None
    attributes: Optional[List[Attribute]] = None
    properties: Optional[Properties] = None
    collection: Optional[CollectionInfo] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)
