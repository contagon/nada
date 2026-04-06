"""Type tests for combined Option and Result types using assert_type.

Tests types that inherit from both IsSome and IsOk, allowing them
to be used in both Option and Result contexts.
"""

# pyright: reportUnusedCallResult=none
from typing import assert_type, Literal
from dataclasses import dataclass

from nada import (
    Option,
    Result,
    Nada,
    NadaType,
    is_some,
    is_none,
    is_ok,
    is_err,
    IsSome,
    IsOk,
    IsErr,
)


# ----------------------- Combined Type Definition ----------------------- #
@dataclass
class Data(IsSome, IsOk):
    """A type that can be used as both Option and Result Ok value."""

    value: int


class DataErr(IsSome, IsErr):
    """Error type for Data results."""

    message: str

    def __init__(self, message: str) -> None:
        super().__init__(f"DataErr: {message}")
        self.message = message


# ----------------------- Using Combined Type in Option ----------------------- #
def test_combined_type_in_option() -> None:
    """Test combined type works as Option."""

    def get_data() -> Option[Data]:
        return Data(value=5)

    x = get_data()
    assert_type(x, Data | NadaType)


def test_combined_type_option_narrowing_is_some() -> None:
    """Test is_some narrows combined type in Option context."""

    def get_data() -> Option[Data]:
        return Data(value=5)

    x = get_data()
    if is_some(x):
        assert_type(x, Data)


def test_combined_type_option_narrowing_is_none() -> None:
    """Test is_none narrows to NadaType in Option context."""

    def get_data() -> Option[Data]:
        return Nada

    x = get_data()
    if is_none(x):
        assert_type(x, NadaType)


def test_combined_type_option_property_narrowing() -> None:
    """Test .is_some property narrows combined type."""

    def get_data() -> Option[Data]:
        return Data(value=5)

    x = get_data()
    if x.is_some is True:
        assert_type(x, Data)


# ----------------------- Using Combined Type in Result ----------------------- #
def test_combined_type_in_result() -> None:
    """Test combined type works as Result Ok value."""

    def get_result() -> Result[Data, DataErr]:
        return Data(value=5)

    x = get_result()
    assert_type(x, Data | DataErr)


def test_combined_type_result_narrowing_is_ok() -> None:
    """Test is_ok narrows combined type in Result context."""

    def get_result() -> Result[Data, DataErr]:
        return Data(value=5)

    x = get_result()
    if is_ok(x):
        assert_type(x, Data)


def test_combined_type_result_narrowing_is_err() -> None:
    """Test is_err narrows to error type in Result context."""

    def get_result() -> Result[Data, DataErr]:
        return DataErr(message="error")

    x = get_result()
    if is_err(x):
        assert_type(x, DataErr)


def test_combined_type_result_property_narrowing() -> None:
    """Test .is_ok property narrows combined type."""

    def get_result() -> Result[Data, DataErr]:
        return Data(value=5)

    x = get_result()
    if x.is_ok is True:
        assert_type(x, Data)


# ----------------------- Combined Type Methods ----------------------- #
def test_combined_type_option_methods() -> None:
    """Test Option methods work on combined type."""
    d = Data(value=5)
    assert_type(d.unwrap(), Data)
    assert_type(d.expect("error"), Data)
    assert_type(d.unwrap_or(Data(value=0)), Data)


def test_combined_type_result_methods() -> None:
    """Test Result methods work on combined type (same as Option for IsOk)."""
    d = Data(value=5)
    # IsOk provides these methods that return Self
    assert_type(d.unwrap(), Data)
    assert_type(d.expect("error"), Data)


# ----------------------- Match Statement with Combined Type ----------------------- #
def test_combined_type_option_match() -> None:
    """Test match statement with combined type in Option context."""

    def get_data() -> Option[Data]:
        return Data(value=5)

    x = get_data()
    match x:
        case Data(value=v):
            assert_type(x, Data)
            assert_type(v, int)
        case NadaType():
            assert_type(x, NadaType)


def test_combined_type_result_match() -> None:
    """Test match statement with combined type in Result context."""

    def get_result() -> Result[Data, DataErr]:
        return Data(value=5)

    x = get_result()
    match x:
        case Data(value=v):
            assert_type(x, Data)
            assert_type(v, int)
        case DataErr(message=m):
            assert_type(x, DataErr)
            assert_type(m, str)


# ----------------------- unwrap_or with Different Types ----------------------- #
def test_nada_unwrap_or_with_combined_type() -> None:
    """Test Nada.unwrap_or returns the combined type default."""
    result = Nada.unwrap_or(Data(value=42))
    assert_type(result, Data)


def test_err_unwrap_or_with_combined_type() -> None:
    """Test IsErr.unwrap_or returns the combined type default."""
    e = DataErr(message="error")
    result = e.unwrap_or(DataErr(message="warning"))
    assert_type(result, DataErr)


# ----------------------- Property Types on Combined ----------------------- #
def test_combined_type_properties() -> None:
    """Test combined type has correct property types."""
    d = Data(value=5)
    # Both is_some and is_ok should be Literal[True]
    assert_type(d.is_some, Literal[True])
    assert_type(d.is_none, Literal[False])
    assert_type(d.is_ok, Literal[True])
    assert_type(d.is_err, Literal[False])
