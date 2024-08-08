# tests/test_custom.py

import pytest

from src.extensions import GreaterThanSpecification, LessThanSpecification


class TestGreaterThanSpecification:
    def test_greater_than_specification_satisfied(self):
        spec = GreaterThanSpecification(5)
        assert spec(10)

    def test_greater_than_specification_not_satisfied(self):
        spec = GreaterThanSpecification(5)
        assert not spec(3)


class TestLessThanSpecification:
    def test_less_than_specification_satisfied(self):
        spec = LessThanSpecification(12)
        assert spec(10)

    def test_less_than_specification_not_satisfied(self):
        spec = LessThanSpecification(12)
        assert not spec(15)
