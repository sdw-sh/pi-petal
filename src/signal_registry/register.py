from typing import Generic, NamedTuple, Type, Any, TypeVar

T = TypeVar("T")


class Register(Generic[T]):
    def __init__(self, signal: str, event: T) -> None:
        super().__init__()
        self.signal: str = signal
        self.event: T = event
