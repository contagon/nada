from typing import Any, Literal, Never, Self, final, override
from abc import ABC, abstractmethod

from typing_extensions import TypeIs


# ------------------------- Base Classes ------------------------- #
class Resultable[T](ABC):
    @property
    @abstractmethod
    def is_ok(self) -> bool: ...

    @property
    @abstractmethod
    def is_err(self) -> bool: ...

    @abstractmethod
    def expect(self, msg: str) -> T: ...

    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...


# Have to separate these to disambiguate the is_ok and is_err properties
class OkResultable[T](Resultable[T], ABC):
    @property
    @override
    def is_ok(self) -> Literal[True]:
        return True

    @property
    @override
    def is_err(self) -> Literal[False]:
        return False


class ErrResultable[T](Resultable[T], ABC):
    @property
    @override
    def is_ok(self) -> Literal[False]:
        return False

    @property
    @override
    def is_err(self) -> Literal[True]:
        return True


# ------------------------- Default Implementations ------------------------- #
@final
class Ok[T](OkResultable[T]):
    def __init__(self, val: T) -> None:
        self.val = val

    @override
    def expect(self, msg: str) -> T:
        return self.val

    @override
    def unwrap(self) -> T:
        return self.val

    @override
    def unwrap_or(self, default: T) -> T:
        return self.val


@final
class Err[E: Exception](ErrResultable[E]):
    def __init__(self, err: E) -> None:
        self.err = err

    @override
    def expect(self, msg: str) -> Never:
        raise ValueError(msg)

    @override
    def unwrap(self) -> Never:
        raise ValueError("Called unwrap on an Err")

    @override
    def unwrap_or[T](self, default: T) -> T:
        return default


type Result[T: OkResultable[Any], E: ErrResultable[Any]] = T | E


def is_ok[T: OkResultable[Any], E: ErrResultable[Any]](x: Result[T, E]) -> TypeIs[T]:
    return x.is_ok


def is_err[T: OkResultable[Any], E: ErrResultable[Any]](x: Result[T, E]) -> TypeIs[E]:
    return x.is_err


# ------------------------- For Downstream Inheritance ------------------------- #
class IsOk(OkResultable["IsOk"]):
    @property
    @override
    def is_ok(self) -> Literal[True]:
        return True

    @property
    @override
    def is_err(self) -> Literal[False]:
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


class IsErr(ErrResultable["IsErr"], Exception):
    @property
    @override
    def is_ok(self) -> Literal[False]:
        return False

    @property
    @override
    def is_err(self) -> Literal[True]:
        return True

    @override
    def expect(self, msg: str) -> Self:
        raise ValueError(msg)

    @override
    def unwrap(self) -> Self:
        raise ValueError("Called unwrap on an Err")

    @override
    def unwrap_or[T](self, default: T) -> T:
        return default
