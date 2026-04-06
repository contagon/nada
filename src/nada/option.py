from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Final,
    Literal,
    Never,
    Protocol,
    Self,
    final,
    reveal_type,
    Any,
)
from typing_extensions import TypeIs


class Optionable[T](Protocol):
    @property
    def is_some(self) -> bool: ...

    @property
    def is_none(self) -> bool: ...

    def expect(self, msg: str) -> T: ...

    def unwrap(self) -> T: ...

    def unwrap_or(self, default: T) -> T: ...


@final
class Some[T]:
    def __init__(self, val: T) -> None:
        self.val = val
        # Had to move these here to avoid pyright interpreting them as class variables 
        # which is a mismatch with the Protocol
        # Alternative options which aren't yet available:
        # 1. Make the Protocol have readonly class properties. Requires metaclass or ReadOnly
        self.is_some: Final[Literal[True]] = True
        self.is_none: Final[Literal[False]] = False

    def expect(self, msg: str) -> Self:
        return self

    def unwrap(self) -> T:
        return self.val

    def unwrap_or(self, default: T) -> T:
        return self.val


class SomeBase:
    # Not sure why these work here, but not in Some
    is_some: Final[Literal[True]] = True
    is_none: Final[Literal[False]] = False

    def expect(self, msg: str) -> Self:
        return self

    def unwrap(self) -> Self:
        return self

    def unwrap_or(self, default: Self) -> Self:
        return self




class NothingType:
    is_some: Final[Literal[False]] = False
    is_none: Final[Literal[True]] = True

    def expect(self, msg: str) -> Never:
        raise ValueError(msg)

    def unwrap(self) -> Never:
        raise ValueError("Unwrapped a None")

    def unwrap_or[T](self, default: T) -> T:
        return default


Nothing = NothingType()
type Option[T: Optionable[Any]] = NothingType | T


def is_some[T: Optionable[Any]](x: Option[T]) -> TypeIs[T]:
    return x.is_some


def is_none[T: Optionable[Any]](x: Option[T]) -> TypeIs[NothingType]:
    return x.is_none


# ------------------------- Test things ------------------------- #
@dataclass
class Test(SomeBase):
    val: int


def my_test() -> Option[Some[int]]:
    return Nothing


def make_test() -> Option[Test]:
    # return Test(5)
    return Nothing


x = my_test()
t = make_test()

# m = my_test().unwrap_or(Test(5))

if is_some(t):
    reveal_type(t)

if t.is_some is True:
    reveal_type(t)

match x:
    case Some(val=v):
        reveal_type(x)
        reveal_type(v)
    case NothingType():
        reveal_type(x)
