from dataclasses import dataclass
from typing import (
    Literal,
    Never,
    Self,
    final,
    override,
    reveal_type,
    Any,
)
from typing_extensions import TypeIs
from abc import ABC, abstractmethod


class Optionable[T](ABC):
    @property
    @abstractmethod
    def is_some(self) -> bool: ...

    @property
    @abstractmethod
    def is_none(self) -> bool: ...

    @abstractmethod
    def expect(self, msg: str) -> T: ...

    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...


@final
class Some[T](Optionable[T]):
    def __init__(self, val: T) -> None:
        self.val = val

    @property
    @override
    def is_some(self) -> Literal[True]:
        return True

    @property
    @override
    def is_none(self) -> Literal[False]:
        return False

    @override
    def expect(self, msg: str) -> T:
        return self.val

    @override
    def unwrap(self) -> T:
        return self.val

    @override
    def unwrap_or(self, default: T) -> T:
        return self.val


class SomeBase(Optionable["SomeBase"]):
    @property
    @override
    def is_some(self) -> Literal[True]:
        return True

    @property
    @override
    def is_none(self) -> Literal[False]:
        return False

    @override
    def expect(self, msg: str) -> Self:
        return self

    @override
    def unwrap(self) -> Self:
        return self

    @override
    def unwrap_or(self, default: Self) -> Self:
        return self


class NothingType(Optionable[None]):
    @property
    @override
    def is_some(self) -> Literal[False]:
        return False

    @property
    @override
    def is_none(self) -> Literal[True]:
        return True

    @override
    def expect(self, msg: str) -> Never:
        raise ValueError(msg)

    @override
    def unwrap(self) -> Never:
        raise ValueError("Unwrapped a None")

    @override
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

m = make_test().unwrap_or(Test(5))

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
