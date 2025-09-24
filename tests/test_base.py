import pytest

from src.base import Specification


class TestSpecification:

    def test_unimplemented_is_satisfied_by(self):
        class InvalidSpecification(Specification[int]):
            pass

        spec = InvalidSpecification()
        with pytest.raises(
            NotImplementedError, match="You must implement the 'is_satisfied_by' method."
        ):
            spec(10)

    def test_implemented_is_satisfied_by(self):

        class ValidSpecification(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 5

        spec = ValidSpecification()
        assert spec(10)
        assert not spec(3)

    def test_specification_with_strings(self):
        class StringLengthSpecification(Specification[str]):
            def __init__(self, min_length: int):
                self.min_length = min_length

            def is_satisfied_by(self, candidate: str) -> bool:
                return len(candidate) >= self.min_length

        spec = StringLengthSpecification(3)
        assert spec("abc")
        assert spec("abcd")
        assert not spec("ab")

    def test_specification_call_method(self):
        class EvenNumberSpecification(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate % 2 == 0

        spec = EvenNumberSpecification()
        assert spec(2)
        assert not spec(3)
