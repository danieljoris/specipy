# tests/test_base.py

import pytest
from src.base import Specification


class TestSpecification:

    def test_unimplemented_is_satisfied_by(self):
        class InvalidSpecification(Specification[int]):
            pass

        spec = InvalidSpecification()
        with pytest.raises(
            NotImplementedError, match="Você deve implementar o método is_satisfied_by."
        ):
            spec(10)

    def test_implemented_is_satisfied_by(self):

        class ValidSpecification(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 5

        spec = ValidSpecification()
        assert spec(10)
        assert not spec(3)
