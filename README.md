# nada

nada is Spanish for "nothing". It contains a small pythonic implementation of rust's `Option` and `Result` types.

In constrast to other similar python libraries, nada's `Option` and `Result` types are always just `Union`s with no additional wrapper for `Some`, `Ok`, or `Err` (although those can be used as well). Simply add `IsSome` or `IsOk` as base methods and enjoy your guardrails! This makes it slightly more pythonic and easier for those unfamiliar with functional programming to grasp the concepts.

## Installation

```bash
pip install nada
uv add nada
```

Requires Python 3.12 or later.

## Usage

### Option Types

`Option` can be used with the `IsSome` base class or with the `Some` wrapper 

```python
from nada import Some, Nada, Option, IsSome, is_some, is_none
from dataclasses import dataclass

@dataclass
class User(IsSome):
    name: str

# The Option type is an alias for User | Nada
def find_user(user_id: int) -> Option[User]:
    if user_id == 1:
        return User("Alice")
    return Nada

# Type narrowing with guard functions
user = find_user(1)
if is_some(user):
    # Type checker knows this is User
    # Access User fields directly, no unwrapping needed
    print(user.name)

if is_none(user):
    print("User not found")  # Type checker knows this is NadaType

# Unwrapping values
name = Some("Alice").unwrap()           # Returns User("Alice")
name = Nada.unwrap_or("Unknown")        # Returns User("Unknown")
name = Some("Alice").expect("Missing")  # Returns User("Alice")

# Pattern matching
match find_user(1):
    case User(name=name):
        print(f"Found: {name}")
    case NadaType():
        print("Not found")
```

You can also use the `Some` wrapper for builtin or external types

```python
from dataclasses import dataclass
from nada import Option, Nada, Some, is_some

def get_user(user_id: int) -> Option[Some[str]]:
    if user_id == 1:
        return Some("Alice")
    return Nada

user = get_user(1)
if is_some(user):
    print(user)  
```

### Result Types

Use `Result` when an operation may fail. Create custom success and error types by inheriting from `IsOk` and `IsErr`:

```python
from dataclasses import dataclass
from nada import Result, IsOk, IsErr, is_ok, is_err

@dataclass
class ParsedData(IsOk):
    value: dict

class ParseError(IsErr, Exception):
    def __init__(self, line: int, message: str):
        super().__init__(f"Line {line}: {message}")
        self.line = line

# The result type is an alias for ParsedData | ParseError
def parse(text: str) -> Result[ParsedData, ParseError]:
    if not text:
        return ParseError(line=0, message="Empty input")
    return ParsedData(value={"text": text})

# Type narrowing with guard functions
result = parse("")
if is_ok(result):
    print(result.value)  # Type checker knows this is ParsedData

if is_err(result):
    print(f"Error at line {result.line}")  # Type checker knows this is ParseError

# Pattern matching
match parse("hello"):
    case ParsedData(value=v):
        print(f"Result: {v}")
    case ParseError() as e:
        print(f"Error: {e}")
```

You can also use the `Ok` and `Err` wrappers for builtin or external types:

```python
from nada import Ok, Err, Result, is_ok, is_err

def divide(a: int, b: int) -> Result[Ok[float], Err[ZeroDivisionError]]:
    if b == 0:
        return Err(ZeroDivisionError("Cannot divide by zero"))
    return Ok(a / b)

result = divide(10, 2)
if is_ok(result):
    print(result.val)  # Type checker knows this is Ok[float]

if is_err(result):
    print(result.err)  # Type checker knows this is Err[ZeroDivisionError]

# Unwrapping values
value = Ok(42).unwrap()              # Returns 42
value = Err(ValueError()).unwrap_or(0)  # Returns 0
```

### Type Narrowing with Properties

In addition to guard functions, you can use literal-typed properties with `is True` checks:

```python
from nada import Some, Nada

value = Some(42)

if value.is_some is True:
    print(value.val)  # Type is narrowed

if value.is_none is True:
    print("No value")
```

## API Reference

### Option Types

| Type        | Description                               |
|-------------|-------------------------------------------|
| `IsSome`    | Base class for custom "some" types        |
| `Some[T]`   | Wraps a value of type T                   |
| `Nada`      | Singleton representing absence of a value |
| `NadaType`  | The type of `Nada`                        |
| `Option[T]` | Type alias for `T \| NadaType`            |

### Result Types

| Type           | Description                                        |
|----------------|----------------------------------------------------|
| `IsOk`         | Base class for custom success types                |
| `IsErr`        | Base class for custom error types                  |
| `Ok[T]`        | Wraps a successful value                           |
| `Err[E]`       | Wraps an exception (E must inherit from Exception) |
| `Result[T, E]` | Type alias for `T \| E`                            |

### Type Guards

| Function       | Narrows to                     |
|----------------|--------------------------------|
| `is_some(val)` | Types inheriting from `IsSome` |
| `is_none(val)` | `NadaType`                     |
| `is_ok(val)`   | Types inheriting from `IsOk`   |
| `is_err(val)`  | Types inheriting from `IsErr`  |

### Common Methods

All `Some`, `Ok`, and `Err` types provide:

- `unwrap()` - Returns the inner value, raises if not present
- `expect(msg)` - Like `unwrap()` but with a custom error message
- `unwrap_or(default)` - Returns the inner value or the provided default

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
