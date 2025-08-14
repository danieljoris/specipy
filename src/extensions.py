import time
from typing import TypeVar

from src.base import Specification


class GreaterThanSpecification(Specification[int]):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > self.threshold


class LessThanSpecification(Specification[int]):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate < self.threshold


class BetweenSpecification(Specification[int]):
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def is_satisfied_by(self, candidate: int) -> bool:
        return self.lower <= candidate <= self.upper


class MinLengthSpecification(Specification[str]):
    def __init__(self, min_length: int):
        self.min_length = min_length

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) >= self.min_length


class MaxLengthSpecification(Specification[str]):
    def __init__(self, max_length: int):
        self.max_length = max_length

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) <= self.max_length


T = TypeVar("T")


class CircuitBreakerSpecification(Specification[T]):
    def __init__(
        self, spec: Specification[T], failure_threshold: int, recover_timeout: float = 60
    ):
        self.spec = spec
        self.failure_threshold = failure_threshold
        self.recover_timeout = recover_timeout
        self.failure_count = 0
        self.last_failure_time = 0

    def is_satisfied_by(self, candidate: T) -> bool:

        if self.failure_count >= self.failure_threshold:
            if time.time() - self.last_failure_time < self.recover_timeout:
                return False
            self.reset()

        try:
            result = self.spec.is_satisfied_by(candidate)
            if not result:
                self.failure_count += 1
                self.last_failure_time = time.time()
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            return False

    def reset(self):
        self.failure_count = 0
        self.last_failure_time = 0
