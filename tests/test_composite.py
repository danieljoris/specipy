from src.base import Specification
from src.extensions import GreaterThanSpecification, LessThanSpecification
from src.utils import lambda_spec


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

    def test_or_specification_with_lambda_spec(self):
        div_by_3_spec = lambda_spec(lambda x: x % 3 == 0)
        div_by_5_spec = lambda_spec(lambda x: x % 5 == 0)

        combined_spec = div_by_3_spec | div_by_5_spec

        assert combined_spec(3)
        assert combined_spec(5)
        assert combined_spec(15)
        assert not combined_spec(7)
        assert not combined_spec(11)


class TestNotSpecification:
    def test_not_specification_satisfied(self):
        spec = GreaterThanSpecification(5)
        not_spec = ~spec
        assert not_spec(3)

    def test_not_specification_not_satisfied(self):
        spec = GreaterThanSpecification(5)
        not_spec = ~spec
        assert not not_spec(10)

    def test_not_specification_with_lambda_spec(self):
        is_even_spec = lambda_spec(lambda x: x % 2 == 0)
        not_even = ~is_even_spec

        assert not_even(3)
        assert not not_even(2)


class TestComplexCompositions:
    def test_complex_and_or_composition(self):
        spec1 = GreaterThanSpecification(5) & LessThanSpecification(12)
        spec2 = LessThanSpecification(0)

        combined_spec = spec1 | spec2

        assert combined_spec(10)
        assert combined_spec(-5)
        assert not combined_spec(15)

    def test_complex_not_composition(self):
        spec = GreaterThanSpecification(5) & LessThanSpecification(12)
        not_spec = ~spec

        assert not_spec(3)
        assert not_spec(15)
        assert not not_spec(10)

    def test_mixed_type_specifications(self):
        is_even_spec: Specification[int] = lambda_spec(lambda x: x % 2 == 0)
        greater_than_five = GreaterThanSpecification(5)

        combined_spec = greater_than_five & is_even_spec

        assert combined_spec(6)
        assert not combined_spec(7)
        assert not combined_spec(4)


class TestCompositionChaining:
    def test_multiple_and_chaining(self):
        spec1 = GreaterThanSpecification(5)
        spec2 = LessThanSpecification(12)
        spec3 = lambda_spec(lambda x: x % 2 == 0)

        combined_spec = spec1 & spec2 & spec3

        assert combined_spec(6)
        assert combined_spec(8)
        assert combined_spec(10)
        assert not combined_spec(4)
        assert not combined_spec(13)
        assert not combined_spec(7)

    def test_multiple_or_chaining(self):
        spec1 = LessThanSpecification(0)
        spec2 = GreaterThanSpecification(100)
        spec3 = lambda_spec(lambda x: x % 7 == 0)

        combined_spec = spec1 | spec2 | spec3

        assert combined_spec(-5)
        assert combined_spec(150)
        assert combined_spec(14)
        assert combined_spec(21)
        assert not combined_spec(50)

    def test_mixed_and_or_precedence(self):
        spec1 = GreaterThanSpecification(5) & LessThanSpecification(12)
        spec2 = LessThanSpecification(-5)

        combined_spec = spec1 | spec2

        assert combined_spec(10)
        assert combined_spec(-10)
        assert not combined_spec(15)
        assert not combined_spec(3)

    def test_not_with_complex_composition(self):
        inner_spec = (
            GreaterThanSpecification(5) & LessThanSpecification(12)
        ) | LessThanSpecification(-5)
        not_spec = ~inner_spec

        assert not_spec(15)
        assert not_spec(3)
        assert not not_spec(10)
        assert not not_spec(-10)

    def test_de_morgan_law_verification(self):
        spec_a = GreaterThanSpecification(5)
        spec_b = LessThanSpecification(12)

        not_a_and_b = ~(spec_a & spec_b)
        not_a_or_not_b = (~spec_a) | (~spec_b)

        test_values = [3, 6, 10, 15, -5]
        for value in test_values:
            assert not_a_and_b(value) == not_a_or_not_b(
                value
            ), f"De Morgan's law failed for value {value}"
