#!/usr/bin/python3

from decimal import Decimal
from typing import Any, Final, Union

import faster_eth_utils
import hexbytes
from eth_typing import ChecksumAddress

from .datatypes import EthAddress, Fixed, HexString, Wei
from .utils import get_int_bounds


HexBytes: Final = hexbytes.HexBytes

is_hex: Final = faster_eth_utils.is_hex
to_text: Final = faster_eth_utils.to_text

_TEN_DECIMALS: Final = Decimal("1.0000000000")


def to_uint(value: Any, type_str: str = "uint256") -> Wei:
    """Convert a value to an unsigned integer"""
    wei: Wei = Wei(value)
    lower, upper = get_int_bounds(type_str)
    if wei < lower or wei > upper:
        raise OverflowError(f"{value} is outside allowable range for {type_str}")
    return wei


def to_int(value: Any, type_str: str = "int256") -> Wei:
    """Convert a value to a signed integer"""
    wei = Wei(value)
    lower, upper = get_int_bounds(type_str)
    if wei < lower or wei > upper:
        raise OverflowError(f"{value} is outside allowable range for {type_str}")
    return wei


def to_decimal(value: Any) -> Fixed:
    """Convert a value to a fixed point decimal"""
    d: Fixed = Fixed(value)
    if d < -(2**127) or d >= 2**127:
        raise OverflowError(f"{value} is outside allowable range for decimal")
    if d.quantize(_TEN_DECIMALS) != d:
        raise ValueError("Maximum of 10 decimal points allowed")
    return d


def to_address(value: Union[str, bytes]) -> ChecksumAddress:
    """Convert a value to an address"""
    return str(EthAddress(value))  # type: ignore [return-value]


def to_bytes(value: Any, type_str: str = "bytes32") -> bytes:
    """Convert a value to bytes"""
    return bytes(HexString(value, type_str))


def to_bool(value: Any) -> bool:
    """Convert a value to a boolean"""
    if not isinstance(value, (int, float, bool, bytes, str)):
        raise TypeError(f"Cannot convert {type(value).__name__} '{value}' to bool")
    if isinstance(value, bytes):
        if not value:
            return False
        value = int(value.hex(), 16)
    if isinstance(value, str) and value.startswith("0x"):
        value = int(value, 16)
    if value not in (0, 1, True, False):
        raise ValueError(f"Cannot convert {type(value).__name__} '{value}' to bool")
    return bool(value)


def to_string(value: Any) -> str:
    """Convert a value to a string"""
    try:
        if isinstance(value, bytes):
            return to_text(hexstr=HexBytes(value).hex())  # type: ignore [arg-type]
        value = str(value)
        if value.startswith("0x") and is_hex(value):
            return to_text(hexstr=value)
        return value
    except UnicodeDecodeError as e:
        raise ValueError(e)


__all__ = ["to_uint", "to_int", "to_decimal", "to_address", "to_bytes", "to_bool", "to_string"]
