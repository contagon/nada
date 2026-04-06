from dataclasses import dataclass
from typing import Literal, Never, Protocol, Self, Any, TypeIs, reveal_type


class Resultable(Protocol):
    @property
    def is_ok(self) -> bool: ...

    @property
    def is_err(self) -> bool: ...

    def expect(self, msg: str) -> Self: ...

    def unwrap(self) -> Self: ...

    def unwrap_or(self, default: Self) -> Self: ...


class OkBase(Resultable):
    is_ok: Literal[True] = True
    is_err: Literal[False] = False

    def expect(self, msg: str) -> Self:
        return self

    def unwrap(self) -> Self:
        return self

    def unwrap_or(self, default: Self) -> Self:
        return self


class Ok[T](OkBase):
    def __init__(self, val: T) -> None:
        self.val = val


class ErrBase(Resultable, Exception):
    is_ok: Literal[False] = False
    is_err: Literal[True] = True

    def expect(self, msg: str) -> Never:
        raise ValueError(msg)

    def unwrap(self) -> Never:
        raise ValueError("Unwrapped an Err")

    def unwrap_or[T](self, default: T) -> T:
        return default

    def __eq__(self, other: Any) -> bool:
        if other is None:
            return True
        else:
            return False


type Result[T: OkBase, E: ErrBase] = T | E


def is_ok[T: OkBase, E: ErrBase](x: Result[T, E]) -> TypeIs[T]:
    return x.is_ok


def is_err[T: OkBase, E: ErrBase](x: Result[T, E]) -> TypeIs[E]:
    return x.is_err


# ------------------------- Test things ------------------------- #
@dataclass
class Test(OkBase):
    val: int


def my_test() -> Result[Ok[int], ErrBase]:
    return ErrBase()


def make_test() -> Result[Test, ErrBase]:
    # return Test(5)
    return ErrBase()


x = my_test()
t = make_test()

if is_ok(t):
    reveal_type(t)

if t.is_ok:
    reveal_type(t)

match x:
    case Ok(val=v):
        reveal_type(x)
    case ErrBase():
        reveal_type(x)
