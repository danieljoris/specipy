from typing import Callable, Iterable, Iterator, TypeVar

from src.base import Specification

T = TypeVar("T")


def filter_by_spec(items: Iterable[T], spec: Specification[T]) -> Iterator[T]:
    return (item for item in items if spec.is_satisfied_by(item))


def lambda_spec(fn: Callable[[T], bool]) -> Specification[T]:
    class _LambdaSpec(Specification[T]):
        def is_satisfied_by(self, candidate: T) -> bool:
            return fn(candidate)

    return _LambdaSpec()
