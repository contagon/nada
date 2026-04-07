from .option import Optionable, NadaType, Nada, Some, Option, is_none, is_some, IsSome
from .result import (
    Resultable,
    OkResultable,
    ErrResultable,
    Ok,
    Err,
    Result,
    is_ok,
    is_err,
    IsErr,
    IsOk,
)

__all__ = [
    "Optionable",
    "NadaType",
    "Nada",
    "Some",
    "Option",
    "is_none",
    "is_some",
    "IsSome",
    "Resultable",
    "OkResultable",
    "ErrResultable",
    "Ok",
    "Err",
    "Result",
    "is_ok",
    "is_err",
    "IsErr",
    "IsOk",
]

__version__ = "0.0.1"  # x-release-please-version
