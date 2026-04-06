"""Type tests for Option types using assert_type."""
# pyright: reportUnusedCallResult=none

from typing import assert_type, Literal
from dataclasses import dataclass

from nada import (
    Option,
    Some,
    Nada,
    NadaType,
    is_some,
    is_none,
    IsSome,
)


# ----------------------- Basic Option Types ----------------------- #
def test_some_type() -> None:
    """Test that Some wraps a value with correct type."""
    s: Some[int] = Some(5)
    assert_type(s, Some[int])
    assert_type(s.val, int)


def test_nada_type() -> None:
    """Test that Nada is typed as NadaType."""
    assert_type(Nada, NadaType)


def test_option_union() -> None:
    """Test Option is a union of T and NadaType."""

    def get_option() -> Option[Some[int]]:
        return Nada

    x = get_option()
    assert_type(x, Some[int] | NadaType)


# ----------------------- Option Properties ----------------------- #
def test_some_properties() -> None:
    """Test Some has correct property types."""
    s = Some(5)
    assert_type(s.is_some, Literal[True])
    assert_type(s.is_none, Literal[False])


def test_nada_properties() -> None:
    """Test Nada has correct property types."""
    assert_type(Nada.is_some, Literal[False])
    assert_type(Nada.is_none, Literal[True])


# ----------------------- Option Methods ----------------------- #
def test_some_unwrap() -> None:
    """Test Some.unwrap returns the inner value."""
    s = Some(42)
    assert_type(s.unwrap(), int)


def test_some_expect() -> None:
    """Test Some.expect returns the inner value."""
    s = Some("hello")
    assert_type(s.expect("error"), str)


def test_some_unwrap_or() -> None:
    """Test Some.unwrap_or returns the inner value."""
    s = Some(10)
    assert_type(s.unwrap_or(0), int)


def test_nada_unwrap_or() -> None:
    """Test Nada.unwrap_or returns the default."""
    result = Nada.unwrap_or(100)
    assert_type(result, int)


# ----------------------- Type Narrowing with is_some ----------------------- #
def test_is_some_narrows_to_t() -> None:
    """Test is_some() narrows Option[T] to T."""

    def get_option() -> Option[Some[int]]:
        return Some(5)

    x = get_option()
    if is_some(x):
        assert_type(x, Some[int])


def test_is_some_property_narrows() -> None:
    """Test .is_some property narrows Option[T] to T."""

    def get_option() -> Option[Some[str]]:
        return Some("test")

    x = get_option()
    if x.is_some is True:
        assert_type(x, Some[str])


# ----------------------- Type Narrowing with is_none ----------------------- #
def test_is_none_narrows_to_nada() -> None:
    """Test is_none() narrows Option[T] to NadaType."""

    def get_option() -> Option[Some[int]]:
        return Nada

    x = get_option()
    if is_none(x):
        assert_type(x, NadaType)


def test_is_none_property_narrows() -> None:
    """Test .is_none property narrows Option[T] to NadaType."""

    def get_option() -> Option[Some[int]]:
        return Nada

    x = get_option()
    if x.is_none is True:
        assert_type(x, NadaType)


# ----------------------- Match Statement Narrowing ----------------------- #
def test_match_narrows_some() -> None:
    """Test match statement narrows to Some."""

    def get_option() -> Option[Some[int]]:
        return Some(5)

    x = get_option()
    match x:
        case Some(val=v):
            assert_type(x, Some[int])
            assert_type(v, int)
        case NadaType():
            assert_type(x, NadaType)


# ----------------------- IsSome Inheritance ----------------------- #
@dataclass
class CustomOption(IsSome):
    """Custom option type inheriting from IsSome."""

    value: str


def test_IsSome_inheritance() -> None:
    """Test custom types inheriting IsSome work with Option."""

    def get_custom() -> Option[CustomOption]:
        return Nada

    x = get_custom()
    assert_type(x, CustomOption | NadaType)


def test_IsSome_narrowing_with_is_some() -> None:
    """Test is_some narrows to custom IsSome type."""

    def get_custom() -> Option[CustomOption]:
        return CustomOption(value="test")

    x = get_custom()
    if is_some(x):
        assert_type(x, CustomOption)


def test_IsSome_narrowing_with_property() -> None:
    """Test .is_some property narrows to custom IsSome type."""

    def get_custom() -> Option[CustomOption]:
        return CustomOption(value="test")

    x = get_custom()
    if x.is_some is True:
        assert_type(x, CustomOption)


def test_IsSome_methods() -> None:
    """Test IsSome methods return Self."""
    c = CustomOption(value="test")
    assert_type(c.unwrap(), CustomOption)
    assert_type(c.expect("error"), CustomOption)
    assert_type(c.unwrap_or(CustomOption(value="default")), CustomOption)


# ----------------------- Nested Option Types ----------------------- #
def test_nested_some_types() -> None:
    """Test nested Some types."""
    nested: Some[Some[int]] = Some(Some(5))
    assert_type(nested, Some[Some[int]])
    assert_type(nested.val, Some[int])
    assert_type(nested.val.val, int)


def test_option_with_complex_inner_type() -> None:
    """Test Option with complex inner types."""

    def get_list_option() -> Option[Some[list[int]]]:
        return Some([1, 2, 3])

    x = get_list_option()
    if is_some(x):
        assert_type(x, Some[list[int]])
        assert_type(x.val, list[int])
