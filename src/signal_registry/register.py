from typing import Generic, NamedTuple, Type, Any, TypeVar

T = TypeVar("T")


class Register(Generic[T], NamedTuple):
    signal: str
    event: T
