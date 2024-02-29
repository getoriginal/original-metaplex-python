from typing import Any, Dict, TypeVar

import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey


class ReadApiError(Exception):
    pass


T = TypeVar("T")


class ReadApiConnection(Client):
    def __init__(self, endpoint: str, commitment: Any = None):
        super().__init__(endpoint, commitment)
        self.rpc_endpoint = endpoint

    def call_read_api(self, json_rpc_params: Dict[str, Any]) -> Dict[str, Any]:
        with requests.Session() as session:
            response = session.post(self.rpc_endpoint, json=json_rpc_params)
            return response.json()

    def get_asset(self, asset_id: Pubkey) -> Any:
        result = self.call_read_api(
            {
                "method": "getAsset",
                "params": {
                    "id": str(asset_id),  # TODO_ORIGINAL to_base58()
                },
            }
        )

        asset = result.get("result")
        if not asset:
            raise ReadApiError("No asset returned")
        return asset

    def get_asset_proof(self, asset_id: Pubkey) -> Any:
        result = self.call_read_api(
            {
                "method": "getAssetProof",
                "params": {
                    "id": str(asset_id),  # TODO_ORIGINAL to_base58()
                },
            }
        )

        proof = result.get("result")
        if not proof:
            raise ReadApiError("No asset proof returned")
        return proof

    def get_assets_by_group(
        self, group_key, group_value, page, limit, sort_by, before, after
    ) -> Any:
        if isinstance(page, int) and (before or after):
            raise ReadApiError(
                "Pagination Error. Only one pagination parameter supported per query."
            )

        result = self.call_read_api(
            {
                "method": "getAssetsByGroup",
                "params": {
                    "groupKey": group_key,
                    "groupValue": group_value,
                    "after": after if after else None,
                    "before": before if before else None,
                    "limit": limit if limit else None,
                    "page": page if page is not None else 0,
                    "sortBy": sort_by if sort_by else None,
                },
            }
        )

        if not result.get("result"):
            raise ReadApiError("No results returned")
        return result["result"]

    def get_assets_by_owner(
        self, owner_address, page, limit, sort_by, before, after
    ) -> Any:
        if isinstance(page, int) and (before or after):
            raise ReadApiError(
                "Pagination Error. Only one pagination parameter supported per query."
            )

        result = self.call_read_api(
            {
                "method": "getAssetsByOwner",
                "params": {
                    "ownerAddress": owner_address,
                    "after": after if after else None,
                    "before": before if before else None,
                    "limit": limit if limit else None,
                    "page": page if page is not None else 0,
                    "sortBy": sort_by if sort_by else None,
                },
            }
        )

        if not result.get("result"):
            raise ReadApiError("No results returned")
        return result["result"]
