from typing import Any, Literal, Never, Self, final, override
from abc import ABC, abstractmethod

from typing_extensions import TypeIs


# ------------------------- Protocol Definitions ------------------------- #
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


# ------------------------- Option Implementations ------------------------- #
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
    def expect(self, msg: str) -> None:
        raise ValueError(msg)

    @override
    def unwrap(self) -> None:
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


# ------------------------- Result Implementations ------------------------- #
@final
class Ok[T](Resultable[T]):
    def __init__(self, val: T) -> None:
        self.val = val

    @property
    @override
    def is_ok(self) -> Literal[True]:
        return True

    @property
    @override
    def is_err(self) -> Literal[False]:
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


@final
class Err[E: Exception](Resultable[E]):
    def __init__(self, err: E) -> None:
        self.err = err

    @property
    @override
    def is_ok(self) -> Literal[False]:
        return False

    @property
    @override
    def is_err(self) -> Literal[True]:
        return True

    @override
    def expect(self, msg: str) -> Never:
        raise ValueError(msg)

    @override
    def unwrap(self) -> Never:
        raise ValueError("Called unwrap on an Err")

    @override
    def unwrap_or[T](self, default: T) -> T:
        return default


type Result[T: Resultable[Any], E: Resultable[Any]] = T | E


def is_ok[T: Resultable[Any], E: Resultable[Any]](x: Result[T, E]) -> TypeIs[T]:
    return x.is_ok


def is_err[T: Resultable[Any], E: Resultable[Any]](x: Result[T, E]) -> TypeIs[E]:
    return x.is_err


# ------------------------- For Inheritance ------------------------- #
class NadaBase(Optionable["NadaBase"], Resultable["NadaBase"]):
    @property
    @override
    def is_some(self) -> Literal[True]:
        return True

    @property
    @override
    def is_none(self) -> Literal[False]:
        return False

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


class ErrBase(Exception, Resultable["ErrBase"]):
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
