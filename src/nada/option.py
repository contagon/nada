from typing import Any, Literal, Never, Self, final, override
from abc import ABC, abstractmethod

from typing_extensions import TypeIs


# ------------------------- Base Classes ------------------------- #
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


# ------------------------- Default Implementations ------------------------- #
class NadaType(Optionable[None]):
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
        raise ValueError("Called unwrap on a Nada")

    @override
    def unwrap_or[T](self, default: T) -> T:
        return default


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


Nada = NadaType()

type Option[T: Optionable[Any]] = NadaType | T


def is_some[T: Optionable[Any]](x: Option[T]) -> TypeIs[T]:
    return x.is_some


def is_none[T: Optionable[Any]](x: Option[T]) -> TypeIs[NadaType]:
    return x.is_none


# ------------------------- For Downstream Inheritance ------------------------- #
class IsSome(Optionable["IsSome"]):
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
