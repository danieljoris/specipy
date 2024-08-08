# tests/test_composite.py

import pytest

from src.extensions import GreaterThanSpecification, LessThanSpecification


class TestAndSpecification:
    def test_and_specification_satisfied(self):
        combined_spec = GreaterThanSpecification(5) & LessThanSpecification(12)
        assert combined_spec(10)

    def test_and_specification_not_satisfied(self):
        spec1 = GreaterThanSpecification(5)
        spec2 = LessThanSpecification(12)
        combined_spec = spec1 & spec2
        assert not combined_spec(3)
        assert not combined_spec(13)


class TestOrSpecification:
    def test_or_specification_satisfied(self):
        spec1 = GreaterThanSpecification(15)
        spec2 = LessThanSpecification(5)
        combined_spec = spec1 | spec2
        assert combined_spec(20)
        assert combined_spec(3)

    def test_or_specification_not_satisfied(self):
        spec1 = GreaterThanSpecification(15)
        spec2 = LessThanSpecification(5)
        combined_spec = spec1 | spec2
        assert not combined_spec(10)


class TestNotSpecification:
    def test_not_specification_satisfied(self):
        spec = GreaterThanSpecification(5)
        not_spec = ~spec
        assert not_spec(3)

    def test_not_specification_not_satisfied(self):
        spec = GreaterThanSpecification(5)
        not_spec = ~spec
        assert not not_spec(10)
