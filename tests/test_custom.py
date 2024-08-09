import pytest
from src.extensions import (
    GreaterThanSpecification,
    LessThanSpecification,
    BetweenSpecification,
    MinLengthSpecification,
    MaxLengthSpecification,
)


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


class TestBetweenSpecification:
    @pytest.fixture
    def spec(self):
        return BetweenSpecification(1, 10)

    def test_should_return_true_when_candidate_is_within_range(self, spec):
        assert spec.is_satisfied_by(5) is True

    def test_should_return_false_when_candidate_is_below_range(self, spec):
        assert spec.is_satisfied_by(0) is False

    def test_should_return_false_when_candidate_is_above_range(self, spec):
        assert spec.is_satisfied_by(11) is False


class TestMinLengthSpecification:
    @pytest.fixture
    def spec(self):
        return MinLengthSpecification(3)

    def test_should_return_true_when_candidate_has_min_length(self, spec):
        assert spec.is_satisfied_by("abc") is True

    def test_should_return_false_when_candidate_has_less_than_min_length(self, spec):
        assert spec.is_satisfied_by("ab") is False

    def test_should_return_true_when_candidate_has_more_than_min_length(self, spec):
        assert spec.is_satisfied_by("abcd") is True


class TestMaxLengthSpecification:
    @pytest.fixture
    def spec(self):
        return MaxLengthSpecification(5)

    def test_should_return_true_when_candidate_has_max_length(self, spec):
        assert spec.is_satisfied_by("abcde") is True

    def test_should_return_false_when_candidate_has_more_than_max_length(self, spec):
        assert spec.is_satisfied_by("abcdef") is False

    def test_should_return_true_when_candidate_has_less_than_max_length(self, spec):
        assert spec.is_satisfied_by("abcd") is True
