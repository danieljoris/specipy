from __future__ import annotations
from typing import Protocol, TypeVar

T = TypeVar("T")


class Specification(Protocol[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        raise NotImplementedError("You must implement the 'is_satisfied_by' method.")

    def __call__(self, candidate: T) -> bool:
        return self.is_satisfied_by(candidate)

    def __and__(self, other) -> AndSpecification[T]:
        return AndSpecification(self, other)  # type: ignore

    def __or__(self, other: Specification[T]) -> OrSpecification[T]:
        return OrSpecification(self, other)

    def __invert__(self) -> NotSpecification[T]:
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    def __init__(self, spec1: Specification[T], spec2: Specification[T]):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.spec1(candidate) and self.spec2(candidate)


class OrSpecification(Specification[T]):
    def __init__(self, spec1: Specification[T], spec2: Specification[T]):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.spec1(candidate) or self.spec2(candidate)


class NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]):
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec(candidate)
