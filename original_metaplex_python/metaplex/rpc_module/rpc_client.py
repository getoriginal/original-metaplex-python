import re
import urllib
from dataclasses import dataclass
from typing import Dict, Optional, Union, cast

from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.rpc.responses import SendTransactionResp

from original_metaplex_python.metaplex.errors.program_error import (
    ParsedProgramError,
    UnknownProgramError,
)
from original_metaplex_python.metaplex.errors.rpc_error import (
    FailedToConfirmTransactionError,
    FailedToConfirmTransactionWithResponseError,
    FailedToSendTransactionError,
    RpcError,
)
from original_metaplex_python.metaplex.types.account import (
    UnparsedAccount,
    UnparsedMaybeAccount,
)
from original_metaplex_python.metaplex.types.amount import lamports
from original_metaplex_python.metaplex.types.program import is_error_with_logs
from original_metaplex_python.metaplex.types.signer import (
    Signer,
    get_public_key,
    get_signer_histogram,
)
from original_metaplex_python.metaplex.utils.common import zip_map
from original_metaplex_python.metaplex.utils.read_api_connection import (
    ReadApiConnection,
)
from original_metaplex_python.metaplex.utils.transaction_builder import (
    TransactionBuilder,
)


@dataclass
class Context:
    slot: int


@dataclass
class TransactionError:
    error: Union[Dict, str, None]


@dataclass
class SignatureResult:
    err: Optional[TransactionError] = None


@dataclass
class RpcResponseAndContext:
    context: Context
    value: SignatureResult


@dataclass
class ConfirmTransactionResponse(RpcResponseAndContext):
    pass


@dataclass
class SendAndConfirmTransactionResponse:
    signature: str
    confirm_response: ConfirmTransactionResponse
    blockhash: str
    last_valid_block_height: int


class RpcClient:
    def __init__(self, metaplex):
        self.metaplex = metaplex
        self.default_fee_payer = None

    def prepare_transaction(
        self, transaction: Transaction | TransactionBuilder, signers: list[Signer]
    ):
        latest_block_hash_response = self.get_latest_blockhash().value

        blockhash_with_expiry_block_height = {
            "blockhash": latest_block_hash_response.blockhash,
            "last_valid_block_height": latest_block_hash_response.last_valid_block_height,
        }

        if isinstance(transaction, TransactionBuilder):
            signers = list(transaction.get_signers()) + signers
            transaction = transaction.to_transaction(blockhash_with_expiry_block_height)

        return transaction, signers, blockhash_with_expiry_block_height

    def _original_get_key_pairs(self, signers: list[Signer | Keypair]) -> list[Keypair]:
        key_pairs = []
        for signer in signers:
            if hasattr(signer, "driver") and callable(signer.driver):
                key_pairs.append(signer.driver().keypair)
            else:
                key_pairs.append(signer)
        return cast(list[Keypair], key_pairs)

    def sign_transaction(
        self, transaction: Transaction, signers: list[Signer]
    ) -> Transaction:
        signer_histogram = get_signer_histogram(signers)
        keypairs = self._original_get_key_pairs(signer_histogram.keypairs)

        if keypairs:
            transaction.sign_partial(*keypairs)

        for identity in signer_histogram.identities:
            transaction = identity.sign_transaction(transaction)

        return transaction

    def send_transaction(
        self,
        transaction_builder: Transaction | TransactionBuilder,
        send_options=TxOpts(),
        signers: list[Signer] = [],
    ) -> SendTransactionResp:

        transaction, signers, _ = self.prepare_transaction(transaction_builder, signers)
        default_fee_payer = self.get_default_fee_payer()

        if not transaction.fee_payer and default_fee_payer:
            transaction.fee_payer = get_public_key(default_fee_payer)
            signers = [default_fee_payer] + signers

        transaction = self.sign_transaction(transaction, signers)
        raw_transaction = transaction.serialize()

        try:
            return self.metaplex.connection.send_raw_transaction(
                raw_transaction, send_options
            )
        except Exception as error:
            raise self.parse_program_error(error, transaction)

    def confirm_transaction(
        self,
        signature: SendTransactionResp,
        blockhash_with_expiry_block_height,
        commitment=None,
    ) -> ConfirmTransactionResponse:
        try:
            tx_sig = signature.value
            last_valid_block_height = blockhash_with_expiry_block_height.get(
                "last_valid_block_height"
            )

            rpc_response = self.metaplex.connection.confirm_transaction(
                tx_sig=tx_sig,
                last_valid_block_height=last_valid_block_height,
                commitment=commitment,
            )
        except Exception as error:
            raise FailedToConfirmTransactionError(error)

        if rpc_response.value[0].err:
            raise FailedToConfirmTransactionWithResponseError(rpc_response)

        return rpc_response

    def send_and_confirm_transaction(
        self,
        transaction: TransactionBuilder | Transaction,
        confirm_options: Optional[TxOpts] = None,
        signers: list[Signer] = [],
    ):
        (
            transaction,
            signers,
            blockhash_with_expiry_block_height,
        ) = self.prepare_transaction(transaction, signers)

        signature = self.send_transaction(transaction, confirm_options, signers)
        confirm_response = self.confirm_transaction(
            signature,
            blockhash_with_expiry_block_height,
            confirm_options.preflight_commitment if confirm_options else None,
        )

        return {
            "signature": signature,
            "confirm_response": confirm_response,
            **blockhash_with_expiry_block_height,
        }

    def get_account(self, public_key, commitment=None):
        account_info = self.metaplex.connection.get_account_info(public_key, commitment)
        return self.get_unparsed_maybe_account(public_key, account_info)

    def account_exists(self, public_key, commitment=None):
        balance = self.metaplex.connection.get_balance(public_key, commitment)
        return balance > 0

    def get_multiple_accounts(self, public_keys, commitment=None):
        account_infos = self.metaplex.connection.get_multiple_accounts(
            public_keys, commitment
        )
        return zip_map(
            public_keys,
            account_infos.value,
            (
                lambda public_key, account_info: self.get_unparsed_maybe_account(
                    public_key, account_info
                )
            ),
        )

    def get_program_accounts(self, program_id, config_or_commitment=None):
        accounts = self.metaplex.connection.get_program_accounts(
            program_id, config_or_commitment
        )
        return [
            UnparsedAccount(public_key=account.pubkey, data=account.account_data)
            for account in accounts
        ]

    def airdrop(self, public_key, amount: Union[int, float, str], commitment=None):
        # assert_sol(Amount(amount))
        signature = self.metaplex.connection.request_airdrop(
            public_key, lamports(amount)
        )
        blockhash_with_expiry_block_height = self.get_latest_blockhash()
        confirm_response = self.confirm_transaction(
            signature, blockhash_with_expiry_block_height, commitment
        )
        return {
            "signature": signature,
            "confirm_response": confirm_response,
            **blockhash_with_expiry_block_height,
        }

    def get_balance(self, public_key, commitment=None):
        balance = self.metaplex.connection.get_balance(public_key, commitment)
        return lamports(balance)

    def get_rent(self, num_bytes, commitment=None):
        rent = self.metaplex.connection.get_minimum_balance_for_rent_exemption(
            num_bytes, commitment
        )
        return lamports(rent)

    def get_latest_blockhash(self, commitment_or_config="finalized"):
        return self.metaplex.connection.get_latest_blockhash(commitment_or_config)

    def get_solana_explorer_url(self, signature):
        cluster_param = ""
        cluster = self.metaplex.cluster
        if cluster == "devnet":
            cluster_param = "?cluster=devnet"
        elif cluster == "testnet":
            cluster_param = "?cluster=testnet"
        elif cluster in ["localnet", "custom"]:
            url = urllib.parse.quote_plus(self.metaplex.connection.rpc_endpoint)
            cluster_param = f"?cluster=custom&customUrl={url}"
        return f"https://explorer.solana.com/tx/{signature}{cluster_param}"

    def set_default_fee_payer(self, payer):
        self.default_fee_payer = payer
        return self

    def get_default_fee_payer(self):
        return (
            self.default_fee_payer
            if self.default_fee_payer
            else self.metaplex.identity()
        )

    def get_unparsed_maybe_account(self, public_key, account_info):
        if not account_info:
            return UnparsedMaybeAccount(public_key=public_key, exists=False)

        return UnparsedMaybeAccount(
            data=account_info.data,
            executable=account_info.executable,
            lamports=lamports(account_info.lamports),
            owner=account_info.owner,
            rent_epoch=account_info.rent_epoch,
            public_key=public_key,
            exists=True,
        )

    def get_asset(self, asset_id):
        if isinstance(self.metaplex.connection, ReadApiConnection):
            return self.metaplex.connection.get_asset(asset_id)

        return RpcError("Method not supported! Use a ReadApiConnection instead")

    def get_asset_proof(self, asset_id):
        if isinstance(self.metaplex.connection, ReadApiConnection):
            return self.metaplex.connection.get_asset_proof(asset_id)

        return RpcError("Method not supported! Use a ReadApiConnection instead")

    def get_assets_by_group(
        self, group_key, group_value, page, limit, sort_by, before, after
    ):
        if isinstance(self.metaplex.connection, ReadApiConnection):
            return self.metaplex.connection.get_assets_by_group(
                group_key=group_key,
                group_value=group_value,
                page=page,
                limit=limit,
                sort_by=sort_by,
                before=before,
                after=after,
            )

        return RpcError("Method not supported! Use a ReadApiConnection instead")

    def get_assets_by_owner(self, owner_address, page, limit, sort_by, before, after):
        if isinstance(self.metaplex.connection, ReadApiConnection):
            return self.metaplex.connection.get_assets_by_owner(
                owner_address=owner_address,
                page=page,
                limit=limit,
                sort_by=sort_by,
                before=before,
                after=after,
            )

        return RpcError("Method not supported! Use a ReadApiConnection instead")

    def parse_program_error(self, error, transaction):
        if not is_error_with_logs(error):
            return FailedToSendTransactionError(error)

        regex = r"Error processing Instruction (\d+):"
        matches = re.search(regex, str(error))
        instruction = matches.group(1) if matches else None

        if not instruction:
            return FailedToSendTransactionError(error)

        instruction_number = int(instruction)
        program_id = None

        if transaction.instructions and instruction_number < len(
            transaction.instructions
        ):
            program_id = transaction.instructions[instruction_number].program_id

        if not program_id:
            return FailedToSendTransactionError(error)

        try:
            program = self.metaplex.programs().get(program_id)
        except Exception as error:
            return FailedToSendTransactionError(error)

        if not hasattr(program, "error_resolver"):
            return UnknownProgramError(program, error)

        resolved_error = program.error_resolver(error)
        return (
            ParsedProgramError(program, resolved_error, error.logs)
            if resolved_error
            else UnknownProgramError(program, error)
        )
