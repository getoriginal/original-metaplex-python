from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, TypeVar, Union


class BigNumber(Decimal):
    pass


@dataclass
class Currency:
    symbol: str
    decimals: int
    namespace: Optional[str] = None


@dataclass
class SplTokenCurrency(Currency):
    namespace: str = "spl-token"


# Specific Currency Instances
SOL = Currency(symbol="SOL", decimals=9)
USD = Currency(symbol="USD", decimals=2)

T = TypeVar("T", bound=Currency)


@dataclass
class Amount:
    basis_points: BigNumber
    currency: Currency


@dataclass
class SplTokenAmount:
    basis_points: BigNumber
    currency: SplTokenCurrency


@dataclass
class SolAmount:
    basis_points: BigNumber
    currency: Currency = SOL


@dataclass
class UsdAmount:
    basis_points: BigNumber
    currency: Currency = USD


# Helper functions
def to_big_number(value: Union[int, float, str]) -> BigNumber:
    return BigNumber(value)


def amount(currency: Currency, basis_points: Union[int, float, str]) -> Amount:
    return Amount(basis_points=to_big_number(basis_points), currency=currency)


def spl_token_amount(
    basis_points: Union[int, float, str], currency: SplTokenCurrency
) -> SplTokenAmount:
    return SplTokenAmount(basis_points=to_big_number(basis_points), currency=currency)


def lamports(lamports: Union[int, float, str]) -> SolAmount:
    returned_amount = amount(SOL, lamports)
    return SolAmount(
        basis_points=returned_amount.basis_points, currency=returned_amount.currency
    )


def sol(sol: Union[int, float]) -> SolAmount:
    LAMPORTS_PER_SOL = 10**SOL.decimals
    return lamports(sol * LAMPORTS_PER_SOL)


def usd(usd: Union[int, float]) -> UsdAmount:
    returned_amount = amount(USD, usd * 100)
    return UsdAmount(
        basis_points=returned_amount.basis_points, currency=returned_amount.currency
    )


def token(
    amount: Union[int, float, str], decimals: int = 0, symbol: str = "Token"
) -> SplTokenAmount:
    basis_points = to_big_number(amount) * (10**decimals)
    currency = SplTokenCurrency(symbol=symbol, decimals=decimals)
    return SplTokenAmount(basis_points=basis_points, currency=currency)


def is_sol(currency_or_amount: Union[Currency, Amount]) -> bool:
    return (
        currency_or_amount.currency.symbol == SOL.symbol
        if isinstance(currency_or_amount, Amount)
        else currency_or_amount.symbol == SOL.symbol
    )


def same_currencies(
    left: Union[Currency, Amount], right: Union[Currency, Amount]
) -> bool:
    if isinstance(left, Amount):
        left = left.currency
    if isinstance(right, Amount):
        right = right.currency
    return (
        left.symbol == right.symbol
        and left.decimals == right.decimals
        and left.namespace == right.namespace
    )


def same_amounts(left: Amount, right: Amount) -> bool:
    return same_currencies(left, right) and left.basis_points == right.basis_points


def assert_currency(actual: Union[Currency, Amount], expected: Currency):
    if isinstance(actual, Amount):
        actual = actual.currency
    if not same_currencies(actual, expected):
        raise ValueError("Unexpected currency")


def assert_sol(actual: Union[Currency, Amount]):
    assert_currency(actual, SOL)


def assert_same_currencies(
    left: Union[Currency, Amount],
    right: Union[Currency, Amount],
    operation: Optional[str] = None,
):
    if not same_currencies(left, right):
        raise ValueError(
            f"Currency mismatch in operation '{operation}'"
            if operation
            else "Currency mismatch"
        )


def add_amounts(left: Amount, right: Amount) -> Amount:
    assert_same_currencies(left, right, "add")
    new_basis_points = left.basis_points + right.basis_points
    return Amount(basis_points=BigNumber(new_basis_points), currency=left.currency)


def subtract_amounts(left: Amount, right: Amount) -> Amount:
    assert_same_currencies(left, right, "subtract")
    new_basis_points = left.basis_points - right.basis_points
    return Amount(basis_points=BigNumber(new_basis_points), currency=left.currency)


def multiply_amount(left: Amount, multiplier: int) -> Amount:
    new_basis_points = left.basis_points * multiplier
    return Amount(basis_points=BigNumber(new_basis_points), currency=left.currency)


def divide_amount(left: Amount, divisor: int) -> Amount:
    new_basis_points = left.basis_points / divisor
    return Amount(basis_points=BigNumber(new_basis_points), currency=left.currency)


def absolute_amount(value: Amount) -> Amount:
    new_basis_points = abs(value.basis_points)
    return Amount(basis_points=BigNumber(new_basis_points), currency=value.currency)


def compare_amounts(left: Amount, right: Amount) -> int:
    assert_same_currencies(left, right, "compare")
    if left.basis_points < right.basis_points:
        return -1
    elif left.basis_points > right.basis_points:
        return 1
    else:
        return 0


def is_equal_to_amount(
    left: Amount, right: Amount, tolerance: Optional[Amount] = None
) -> bool:
    if tolerance is None:
        tolerance = Amount(basis_points=BigNumber(0), currency=left.currency)
    assert_same_currencies(left, right, "isEqualToAmount")
    assert_same_currencies(left, tolerance, "isEqualToAmount")
    delta = absolute_amount(subtract_amounts(left, right))
    return is_less_than_or_equal_to_amount(delta, tolerance)


def is_less_than_amount(left: Amount, right: Amount) -> bool:
    return compare_amounts(left, right) < 0


def is_less_than_or_equal_to_amount(left: Amount, right: Amount) -> bool:
    return compare_amounts(left, right) <= 0


def is_greater_than_amount(left: Amount, right: Amount) -> bool:
    return compare_amounts(left, right) > 0


def is_greater_than_or_equal_to_amount(left: Amount, right: Amount) -> bool:
    return compare_amounts(left, right) >= 0


def is_zero_amount(value: Amount) -> bool:
    zero_amount = Amount(basis_points=BigNumber(0), currency=value.currency)
    return compare_amounts(value, zero_amount) == 0


def is_positive_amount(value: Amount) -> bool:
    zero_amount = Amount(basis_points=BigNumber(0), currency=value.currency)
    return compare_amounts(value, zero_amount) >= 0


def is_negative_amount(value: Amount) -> bool:
    zero_amount = Amount(basis_points=BigNumber(0), currency=value.currency)
    return compare_amounts(value, zero_amount) < 0


def format_amount(value: Amount) -> str:
    if value.currency.decimals == 0:
        return f"{value.currency.symbol} {value.basis_points}"
    power = 10**value.currency.decimals
    div, mod = divmod(value.basis_points, power)
    units = f"{div}.{mod:0{value.currency.decimals}d}"
    return f"{value.currency.symbol} {units}"
