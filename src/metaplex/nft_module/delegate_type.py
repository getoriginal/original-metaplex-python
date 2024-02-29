from enum import Enum


class MetadataDelegateRole(Enum):
    AuthorityItem = 0
    Collection = 1
    Use = 2
    Data = 3
    ProgrammableConfig = 4
    DataItem = 5
    CollectionItem = 6
    ProgrammableConfigItem = 7


class TokenDelegateRole(Enum):
    StandardV1 = 0
    TransferV1 = 1
    LockedTransferV1 = 2
    SaleV1 = 3
    UtilityV1 = 4
    StakingV1 = 5


token_delegate_role_map = {
    "StandardV1": TokenDelegateRole.StandardV1,
    "TransferV1": TokenDelegateRole.TransferV1,
    "LockedTransferV1": TokenDelegateRole.LockedTransferV1,
    "SaleV1": TokenDelegateRole.SaleV1,
    "UtilityV1": TokenDelegateRole.UtilityV1,
    "StakingV1": TokenDelegateRole.StakingV1,
}

metadata_delegate_role_map = {
    "CollectionV1": MetadataDelegateRole.Collection,
    "DataV1": MetadataDelegateRole.Data,
    "ProgrammableConfigV1": MetadataDelegateRole.ProgrammableConfig,
}

metadata_delegate_seed_map = {
    MetadataDelegateRole.AuthorityItem: "authority_item_delegate",
    MetadataDelegateRole.Collection: "collection_delegate",
    MetadataDelegateRole.Use: "use_delegate",
    MetadataDelegateRole.Data: "data_delegate",
    MetadataDelegateRole.ProgrammableConfig: "programmable_config_delegate",
    MetadataDelegateRole.DataItem: "data_item_delegate",
    MetadataDelegateRole.CollectionItem: "collection_item_delegate",
    MetadataDelegateRole.ProgrammableConfigItem: "prog_config_item_delegate",
}


def get_metadata_delegate_role(type):
    role = metadata_delegate_role_map[type]
    if not role:
        raise ValueError(f"Invalid metadata delegate type: {type}")
    return role


def get_metadata_delegate_role_seed(type) -> str:
    return metadata_delegate_seed_map[get_metadata_delegate_role(type)]
