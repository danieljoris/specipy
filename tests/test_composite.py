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

    def test_and_specification_with_lambda_spec(self):
        is_even_spec = lambda_spec(lambda x: x % 2 == 0)
        greater_than_five = GreaterThanSpecification(5)

        combined_spec = is_even_spec & greater_than_five
        assert combined_spec(6)  # Even AND greater than 5
        assert not combined_spec(7)  # Odd
        assert not combined_spec(4)  # Even but not greater than 5


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
        is_even_spec = lambda_spec(lambda x: x % 2 == 0)
        is_positive_spec = lambda_spec(lambda x: x > 0)

        combined_spec = is_even_spec | is_positive_spec
        assert combined_spec(2)  # Par
        assert combined_spec(3)  # Positivo
        assert combined_spec(-2)  # Par (mesmo sendo negativo)


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

        assert not_even(3)  # Ímpar
        assert not not_even(2)  # Par


class TestComplexCompositions:
    def test_complex_and_or_composition(self):
        # (x > 5 AND x < 12) OR (x < 0)
        spec1 = GreaterThanSpecification(5) & LessThanSpecification(12)
        spec2 = LessThanSpecification(0)

        combined_spec = spec1 | spec2

        assert combined_spec(10)  # 5 < 10 < 12
        assert combined_spec(-5)  # -5 < 0
        assert not combined_spec(15)  # Não satisfaz nenhuma condição

    def test_complex_not_composition(self):
        # NOT (x > 5 AND x < 12)
        spec = GreaterThanSpecification(5) & LessThanSpecification(12)
        not_spec = ~spec

        assert not_spec(3)  # x <= 5
        assert not_spec(15)  # x >= 12
        assert not not_spec(10)  # 5 < 10 < 12

    def test_mixed_type_specifications(self):
        # Testa composição entre especificações de tipos diferentes
        # (usando create_int_spec para compatibilidade)
        is_even_spec: Specification[int] = lambda_spec(lambda x: x % 2 == 0)
        greater_than_five = GreaterThanSpecification(5)

        # x > 5 AND x é par
        combined_spec = greater_than_five & is_even_spec

        assert combined_spec(6)  # 6 > 5 E é par
        assert not combined_spec(7)  # 7 > 5 mas é ímpar
        assert not combined_spec(4)  # 4 é par mas <= 5
