"""Type tests for Result types using assert_type."""
# pyright: reportUnusedCallResult=none

from typing import assert_type, Literal
from dataclasses import dataclass

from nada import (
    Result,
    Ok,
    Err,
    is_ok,
    is_err,
    IsOk,
    IsErr,
)


# ----------------------- Basic Result Types ----------------------- #
def test_ok_type() -> None:
    """Test that Ok wraps a value with correct type."""
    o: Ok[int] = Ok(5)
    assert_type(o, Ok[int])
    assert_type(o.val, int)


def test_err_type() -> None:
    """Test that Err wraps an exception with correct type."""
    e: Err[ValueError] = Err(ValueError("error"))
    assert_type(e, Err[ValueError])
    assert_type(e.err, ValueError)


def test_result_union() -> None:
    """Test Result is a union of T and E."""

    def get_result() -> Result[Ok[int], Err[ValueError]]:
        return Ok(5)

    x = get_result()
    assert_type(x, Ok[int] | Err[ValueError])


# ----------------------- Result Properties ----------------------- #
def test_ok_properties() -> None:
    """Test Ok has correct property types."""
    o = Ok(5)
    assert_type(o.is_ok, Literal[True])
    assert_type(o.is_err, Literal[False])


def test_err_properties() -> None:
    """Test Err has correct property types."""
    e = Err(ValueError("error"))
    assert_type(e.is_ok, Literal[False])
    assert_type(e.is_err, Literal[True])


# ----------------------- Result Methods ----------------------- #
def test_ok_unwrap() -> None:
    """Test Ok.unwrap returns the inner value."""
    o = Ok(42)
    assert_type(o.unwrap(), int)


def test_ok_expect() -> None:
    """Test Ok.expect returns the inner value."""
    o = Ok("hello")
    assert_type(o.expect("error"), str)


def test_ok_unwrap_or() -> None:
    """Test Ok.unwrap_or returns the inner value."""
    o = Ok(10)
    assert_type(o.unwrap_or(0), int)


def test_err_unwrap_or() -> None:
    """Test Err.unwrap_or returns the default."""
    e = Err(ValueError("error"))
    result = e.unwrap_or(100)
    assert_type(result, int)


# ----------------------- Type Narrowing with is_ok ----------------------- #
def test_is_ok_narrows_to_t() -> None:
    """Test is_ok() narrows Result[T, E] to T."""

    def get_result() -> Result[Ok[int], Err[ValueError]]:
        return Ok(5)

    x = get_result()
    if is_ok(x):
        assert_type(x, Ok[int])


def test_is_ok_property_narrows() -> None:
    """Test .is_ok property narrows Result[T, E] to T."""

    def get_result() -> Result[Ok[str], Err[ValueError]]:
        return Ok("test")

    x = get_result()
    if x.is_ok is True:
        assert_type(x, Ok[str])


# ----------------------- Type Narrowing with is_err ----------------------- #
def test_is_err_narrows_to_e() -> None:
    """Test is_err() narrows Result[T, E] to E."""

    def get_result() -> Result[Ok[int], Err[ValueError]]:
        return Err(ValueError("error"))

    x = get_result()
    if is_err(x):
        assert_type(x, Err[ValueError])


def test_is_err_property_narrows() -> None:
    """Test .is_err property narrows Result[T, E] to E."""

    def get_result() -> Result[Ok[int], Err[ValueError]]:
        return Err(ValueError("error"))

    x = get_result()
    if x.is_err is True:
        assert_type(x, Err[ValueError])


# ----------------------- Match Statement Narrowing ----------------------- #
def test_match_narrows_ok() -> None:
    """Test match statement narrows to Ok."""

    def get_result() -> Result[Ok[int], Err[ValueError]]:
        return Ok(5)

    x = get_result()
    match x:
        case Ok(val=v):
            assert_type(x, Ok[int])
            assert_type(v, int)
        case Err(err=e):
            assert_type(x, Err[ValueError])
            assert_type(e, ValueError)


# ----------------------- Custom Error Types ----------------------- #
class CustomError(Exception):
    """Custom exception for testing."""

    pass


def test_err_with_custom_exception() -> None:
    """Test Err with custom exception types."""

    def get_result() -> Result[Ok[str], Err[CustomError]]:
        return Err(CustomError("custom error"))

    x = get_result()
    if is_err(x):
        assert_type(x, Err[CustomError])
        assert_type(x.err, CustomError)


# ----------------------- IsOk and IsErr Inheritance ----------------------- #
@dataclass
class CustomOk(IsOk):
    """Custom Ok type inheriting from IsOk."""

    value: int


@dataclass
class CustomErr(IsErr):
    """Custom Err type inheriting from IsErr."""

    message: str


def test_IsOk_IsErr_inheritance() -> None:
    """Test custom types inheriting IsOk/IsErr work with Result."""

    def get_custom() -> Result[CustomOk, CustomErr]:
        return CustomOk(value=5)

    x = get_custom()
    assert_type(x, CustomOk | CustomErr)


def test_IsOk_narrowing_with_is_ok() -> None:
    """Test is_ok narrows to custom IsOk type."""

    def get_custom() -> Result[CustomOk, CustomErr]:
        return CustomOk(value=5)

    x = get_custom()
    if is_ok(x):
        assert_type(x, CustomOk)


def test_IsErr_narrowing_with_is_err() -> None:
    """Test is_err narrows to custom IsErr type."""

    def get_custom() -> Result[CustomOk, CustomErr]:
        return CustomErr(message="error")

    x = get_custom()
    if is_err(x):
        assert_type(x, CustomErr)


def test_IsOk_narrowing_with_property() -> None:
    """Test .is_ok property narrows to custom IsOk type."""

    def get_custom() -> Result[CustomOk, CustomErr]:
        return CustomOk(value=5)

    x = get_custom()
    if x.is_ok is True:
        assert_type(x, CustomOk)


def test_IsErr_narrowing_with_property() -> None:
    """Test .is_err property narrows to custom IsErr type."""

    def get_custom() -> Result[CustomOk, CustomErr]:
        return CustomErr(message="error")

    x = get_custom()
    if x.is_err is True:
        assert_type(x, CustomErr)


def test_IsOk_methods() -> None:
    """Test IsOk methods return Self."""
    c = CustomOk(value=5)
    assert_type(c.unwrap(), CustomOk)
    assert_type(c.expect("error"), CustomOk)
    assert_type(c.unwrap_or(CustomOk(value=0)), CustomOk)


def test_IsErr_unwrap_or() -> None:
    """Test IsErr.unwrap_or returns the default."""
    c = CustomErr(message="error")
    result = c.unwrap_or(42)
    assert_type(result, int)


# ----------------------- Nested Result Types ----------------------- #
def test_nested_ok_types() -> None:
    """Test nested Ok types."""
    nested: Ok[Ok[int]] = Ok(Ok(5))
    assert_type(nested, Ok[Ok[int]])
    assert_type(nested.val, Ok[int])
    assert_type(nested.val.val, int)


def test_result_with_complex_inner_type() -> None:
    """Test Result with complex inner types."""

    def get_dict_result() -> Result[Ok[dict[str, int]], Err[KeyError]]:
        return Ok({"a": 1, "b": 2})

    x = get_dict_result()
    if is_ok(x):
        assert_type(x, Ok[dict[str, int]])
        assert_type(x.val, dict[str, int])
