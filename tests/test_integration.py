# tests/test_integration.py

from src.extensions import (
    BetweenSpecification,
    CircuitBreakerSpecification,
    GreaterThanSpecification,
    LessThanSpecification,
    MaxLengthSpecification,
    MinLengthSpecification,
)
from src.utils import filter_by_spec, lambda_spec


class TestFullSystemIntegration:
    """Test complete integration between base, extensions and utils"""

    def test_lambda_spec_with_extensions(self):
        """Test if lambda_spec works with extension specifications"""
        is_even = lambda_spec(lambda x: x % 2 == 0)
        combined_spec = is_even & GreaterThanSpecification(5)

        assert combined_spec(6)
        assert not combined_spec(7)
        assert not combined_spec(4)

    def test_filter_with_complex_specifications(self):
        """Test filter_by_spec with composite specifications"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        is_even = lambda_spec(lambda x: x % 2 == 0)
        between_3_8 = BetweenSpecification(3, 8)

        combined_spec = is_even & between_3_8

        result = list(filter_by_spec(numbers, combined_spec))
        assert result == [4, 6, 8]

    def test_circuit_breaker_with_lambda_spec(self):
        """Test CircuitBreaker with lambda_spec"""

        def risky_spec(candidate):
            if candidate == 0:
                raise ValueError("Zero is not allowed")
            return candidate > 5

        base_spec = lambda_spec(risky_spec)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=2)

        assert cb_spec.is_satisfied_by(0) is False
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(10) is False

    def test_string_specifications_integration(self):
        """Test integration between string specifications"""
        words = ["a", "ab", "abc", "abcd", "abcde", "abcdef"]

        min_length = MinLengthSpecification(3)
        max_length = MaxLengthSpecification(5)

        combined_spec = min_length & max_length

        result = list(filter_by_spec(words, combined_spec))
        assert result == ["abc", "abcd", "abcde"]

    def test_numeric_specifications_integration(self):
        """Test integration between numeric specifications"""
        numbers = [-5, -2, 0, 3, 7, 12, 15, 20]

        between_5_15 = BetweenSpecification(5, 15)
        is_negative = lambda_spec(lambda x: x < 0)

        combined_spec = between_5_15 | is_negative

        result = list(filter_by_spec(numbers, combined_spec))
        assert result == [-5, -2, 7, 12, 15]

    def test_specification_composition_chain(self):
        """Test chaining of specification compositions"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        spec1 = GreaterThanSpecification(3) & LessThanSpecification(8)
        spec2 = lambda_spec(lambda x: x % 2 == 0) & GreaterThanSpecification(8)

        combined_spec = spec1 | spec2

        result = list(filter_by_spec(numbers, combined_spec))
        assert result == [4, 5, 6, 7, 10]

    def test_type_safety_across_system(self):
        """Test if type safety is maintained throughout the system"""
        string_spec = MinLengthSpecification(3)
        number_spec = GreaterThanSpecification(5)
        assert string_spec.is_satisfied_by("abc")
        assert number_spec.is_satisfied_by(10)

        strings = ["a", "ab", "abc", "abcd"]
        numbers = [1, 5, 10, 15]

        string_result = list(filter_by_spec(strings, string_spec))
        number_result = list(filter_by_spec(numbers, number_spec))

        assert string_result == ["abc", "abcd"]
        assert number_result == [10, 15]
