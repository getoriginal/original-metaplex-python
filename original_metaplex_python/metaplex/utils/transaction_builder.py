from dataclasses import dataclass
from typing import Optional

from solana.transaction import Transaction

from ..types.program import Program
from ..types.signer import Signer, get_public_key


class InstructionWithSigners:
    def __init__(self, instruction, signers, key=None):
        self.instruction = instruction
        self.signers = signers
        self.key = key


class TransactionOptions:
    def __init__(self, signatures=None):
        self.signatures = signatures or []


@dataclass
class TransactionBuilderOptions:
    programs: Optional[list[Program]] = None
    payer: Optional[Signer] = None


class TransactionBuilder:
    def __init__(self, transaction_options: Optional[TransactionOptions] = None):
        self.records: list[InstructionWithSigners] = []
        self.transaction_options: TransactionOptions = (
            transaction_options or TransactionOptions()
        )
        self.fee_payer: Signer | None = None
        self.context: dict = {}

    @staticmethod
    def make(transaction_options=None):
        return TransactionBuilder(transaction_options)

    def prepend(self, *txs):
        new_records = []
        for tx in txs:
            if isinstance(tx, TransactionBuilder):
                new_records.extend(tx.get_instruction_with_signers())
            else:
                new_records.append(tx)
        self.records = new_records + self.records
        return self

    def append(self, *txs):
        new_records = []
        for tx in txs:
            if isinstance(tx, TransactionBuilder):
                new_records.extend(tx.get_instruction_with_signers())
            else:
                new_records.append(tx)
        self.records.extend(new_records)
        return self

    def add(self, *txs):
        return self.append(*txs)

    def split_using_key(self, key, include=True):
        first_builder = TransactionBuilder(self.transaction_options)
        second_builder = TransactionBuilder(self.transaction_options)
        key_position = next(
            (i for i, record in enumerate(self.records) if record.key == key), -1
        )

        if key_position > -1:
            key_position += 1 if include else 0
            first_builder.add(*self.records[:key_position])
            second_builder.add(*self.records[key_position:])
        else:
            first_builder.add(self)

        return first_builder, second_builder

    def split_before_key(self, key):
        return self.split_using_key(key, False)

    def split_after_key(self, key):
        return self.split_using_key(key, True)

    def get_instruction_with_signers(self):
        return self.records

    def get_instructions(self):
        instructions = []
        for record in self.records:
            instruction = record.instruction
            if instruction is not None:
                instructions.append(instruction)

        return instructions

    def get_instruction_count(self):
        return len(self.records)

    def is_empty(self):
        return self.get_instruction_count() == 0

    def get_signers(self):
        fee_payer = [] if self.fee_payer is None else [self.fee_payer]
        signers = [record.signers for record in self.records]
        return fee_payer + signers

    def set_transaction_options(self, transaction_options):
        self.transaction_options = transaction_options
        return self

    def get_transaction_options(self):
        return self.transaction_options

    def set_fee_payer(self, fee_payer):
        self.fee_payer = fee_payer
        return self

    def get_fee_payer(self):
        return self.fee_payer

    def set_context(self, context):
        self.context = context
        return self

    def get_context(self):
        return self.context

    def when(self, condition, callback):
        if condition:
            return callback(self)
        return self

    def unless(self, condition, callback):
        return self.when(not condition, callback)

    def to_transaction(self, blockhash_with_expiry_block_height, options=None):
        if options is None:
            options = {"signatures": []}

        transaction_options = self.get_transaction_options()
        combined_signatures = transaction_options.signatures + options["signatures"]

        instructions = self.get_instructions()

        fee_payer = self.get_fee_payer()
        fee_payer_pub_key = get_public_key(fee_payer)
        transaction = Transaction(
            recent_blockhash=blockhash_with_expiry_block_height["blockhash"],
            fee_payer=fee_payer_pub_key,
        )
        transaction.add(*instructions)

        if combined_signatures:
            transaction.signatures = combined_signatures

        return transaction

    def send_and_confirm(self, metaplex, confirm_options=None):
        response = metaplex.rpc().send_and_confirm_transaction(self, confirm_options)
        return {"response": response, **self.get_context()}
