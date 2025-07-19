from typing import Any, Callable, Iterable, Iterator, TypeVar

from src.base import Specification

T = TypeVar("T")


def filter_by_spec(items: Iterable[T], spec: Specification) -> Iterator[T]:
    return (item for item in items if spec.is_satisfied_by(item))


def lambda_spec(fn: Callable[[Any], bool]) -> Specification:
    class _LambdaSpec(Specification):
        def is_satisfied_by(self, candidate: Any) -> bool:
            return fn(candidate)

    return _LambdaSpec()
