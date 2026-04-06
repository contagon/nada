from typing import Any, Final, Literal, Protocol, Self, final

from typing_extensions import TypeIs


# ------------------------- Protocol Definitions ------------------------- #
class Optionable[T](Protocol):
    @property
    def is_some(self) -> bool: ...

    @property
    def is_none(self) -> bool: ...

    def expect(self, msg: str) -> T: ...

    def unwrap(self) -> T: ...

    def unwrap_or(self, default: T) -> T: ...


class Resultable[T](Protocol):
    @property
    def is_ok(self) -> bool: ...

    @property
    def is_err(self) -> bool: ...

    def expect(self, msg: str) -> T: ...

    def unwrap(self) -> T: ...

    def unwrap_or(self, default: T) -> T: ...


# ------------------------- Option Implementations ------------------------- #
class NadaType:
    is_some: Final[Literal[False]] = False
    is_none: Final[Literal[True]] = True

    def expect(self, msg: str) -> None:
        raise ValueError(msg)

    def unwrap(self) -> None:
        raise ValueError("Called unwrap on a Nada")

    def unwrap_or[T](self, default: T) -> T:
        return default


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

    def expect(self, msg: str) -> Self: # pyright: ignore[reportUnusedParameter]
        return self

    def unwrap(self) -> T:
        return self.val

    def unwrap_or(self, default: T) -> T: # pyright: ignore[reportUnusedParameter]
        return self.val


Nada = NadaType()

type Option[T: Optionable[Any]] = NadaType | T


def is_some[T: Optionable[Any]](x: Option[T]) -> TypeIs[T]:
    return x.is_some


def is_none[T: Optionable[Any]](x: Option[T]) -> TypeIs[NadaType]:
    return x.is_none


# ------------------------- Result Implementations ------------------------- #
@final
class Ok[T]:
    def __init__(self, val: T) -> None:
        self.is_ok: Final[Literal[True]] = True
        self.is_err: Final[Literal[False]] = False
        self.val = val

    def expect(self, msg: str) -> T: # pyright: ignore[reportUnusedParameter]
        return self.val

    def unwrap(self) -> T:
        return self.val

    def unwrap_or(self, default: T) -> T: # pyright: ignore[reportUnusedParameter]
        return self.val


@final
class Err[E: Exception]:
    def __init__(self, err: E) -> None:
        self.is_ok: Final[Literal[False]] = False
        self.is_err: Final[Literal[True]] = True
        self.err = err

    def expect(self, msg: str) -> None:
        raise ValueError(msg)

    def unwrap(self) -> None:
        raise ValueError("Called unwrap on an Err")

    def unwrap_or[T](self, default: T) -> T:
        return default


type Result[T: Resultable[Any], E: Resultable[Any]] = T | E


def is_ok[T: Resultable[Any], E: Resultable[Any]](x: Result[T, E]) -> TypeIs[T]:
    return x.is_ok


def is_err[T: Resultable[Any], E: Resultable[Any]](x: Result[T, E]) -> TypeIs[E]:
    return x.is_err


# ------------------------- For Inheritance ------------------------- #
class NadaBase:
    is_some: Final[Literal[True]] = True
    is_none: Final[Literal[False]] = False

    is_ok: Final[Literal[True]] = True
    is_err: Final[Literal[False]] = False

    def expect(self, msg: str) -> Self: # pyright: ignore[reportUnusedParameter]
        return self

    def unwrap(self) -> Self:
        return self

    def unwrap_or(self, default: Self) -> Self: # pyright: ignore[reportUnusedParameter]
        return self


class ErrBase(Exception):
    is_ok: Final[Literal[False]] = False
    is_err: Final[Literal[True]] = True

    def expect(self, msg: str) -> Self:
        raise ValueError(msg)

    def unwrap(self) -> Self:
        raise ValueError("Called unwrap on an Err")

    def unwrap_or[T](self, default: T) -> T:
        return default


# ------------------------- Test things ------------------------- #
from dataclasses import dataclass
from typing import reveal_type


@dataclass
class Test(NadaBase):
    val: int


@dataclass
class TestErr(ErrBase):
    err: str


def some_int() -> Option[Some[int]]:
    return Nada


def some_test() -> Option[Test]:
    # return Test(5)
    return Nada


x = some_int()
t = some_test()

m = some_test().unwrap_or(Test(5))

if is_some(t):
    reveal_type(t)

if t.is_some is True:
    reveal_type(t)

match x:
    case Some(val=v):
        reveal_type(x)
    case NadaType():
        reveal_type(x)


def result_int() -> Result[Ok[int], Err[ValueError]]:
    return Err(ValueError("An error occurred"))


def result_test() -> Result[Test, TestErr]:
    # return Ok(Test(5))
    return TestErr("An error occurred")


x = result_int()
t = result_test()

if is_ok(t):
    reveal_type(t)

if t.is_ok is True:
    reveal_type(t)

match x:
    case Ok(val=v):
        reveal_type(x)
    case Err(err=e):
        reveal_type(x)
