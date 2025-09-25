from src.extensions import (
    BetweenSpecification,
    CircuitBreakerSpecification,
    GreaterThanSpecification,
    LessThanSpecification,
    MaxLengthSpecification,
    MinLengthSpecification,
)
from src.utils import lambda_spec


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

    def test_should_return_true_when_candidate_is_within_range(self):
        spec = BetweenSpecification(1, 10)
        assert spec.is_satisfied_by(5) is True

    def test_should_return_false_when_candidate_is_below_range(self):
        spec = BetweenSpecification(1, 10)
        assert spec.is_satisfied_by(0) is False

    def test_should_return_false_when_candidate_is_above_range(self):
        spec = BetweenSpecification(1, 10)
        assert spec.is_satisfied_by(11) is False


class TestMinLengthSpecification:
    def test_should_return_true_when_candidate_has_min_length(self):
        spec = MinLengthSpecification(3)
        assert spec.is_satisfied_by("abc") is True

    def test_should_return_false_when_candidate_has_less_than_min_length(self):
        spec = MinLengthSpecification(3)
        assert spec.is_satisfied_by("ab") is False

    def test_should_return_true_when_candidate_has_more_than_min_length(self):
        spec = MinLengthSpecification(3)
        assert spec.is_satisfied_by("abcd") is True


class TestMaxLengthSpecification:
    def test_should_return_true_when_candidate_has_max_length(self):
        spec = MaxLengthSpecification(5)
        assert spec.is_satisfied_by("abcde") is True

    def test_should_return_false_when_candidate_has_more_than_max_length(self):
        spec = MaxLengthSpecification(5)
        assert spec.is_satisfied_by("abcdef") is False

    def test_should_return_true_when_candidate_has_less_than_max_length(self):
        spec = MaxLengthSpecification(5)
        assert spec.is_satisfied_by("abcd") is True


class TestCircuitBreakerSpecification:
    """Comprehensive tests for CircuitBreakerSpecification"""

    def test_circuit_breaker_initial_state(self):
        """Tests the initial state of the circuit breaker"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=3)

        # Initial state: should work normally
        assert cb_spec.is_satisfied_by(10) is True
        assert cb_spec.is_satisfied_by(3) is False

        # Counters should be updated
        assert cb_spec.failure_count == 1  # One failure (3)
        assert cb_spec.last_failure_time > 0

    def test_circuit_breaker_activates_after_threshold(self):
        """Tests circuit breaker activation after reaching threshold"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=2)

        # First failure
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.failure_count == 1

        # Second failure - circuit breaker activates
        assert cb_spec.is_satisfied_by(2) is False
        assert cb_spec.failure_count == 2

        # Third attempt - circuit breaker blocks (OPEN state)
        assert cb_spec.is_satisfied_by(10) is False
        assert cb_spec.failure_count == 2  # No more increments

    def test_circuit_breaker_reset_after_timeout(self):
        """Tests automatic reset after timeout"""
        import time

        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(
            base_spec, failure_threshold=2, recover_timeout=0.1
        )

        # Activates the circuit breaker
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(2) is False

        # Circuit breaker is active
        assert cb_spec.failure_count >= 2

        # Wait for timeout
        time.sleep(0.2)

        # Should work again (HALF_OPEN state)
        assert cb_spec.is_satisfied_by(10) is True
        # Counters should be reset after success
        assert cb_spec.failure_count == 0

    def test_circuit_breaker_reset_method(self):
        """Tests manual reset of the circuit breaker"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=2)

        # Activates the circuit breaker
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(2) is False

        # Manual reset
        cb_spec.reset()

        # Should work again
        assert cb_spec.is_satisfied_by(10) is True
        assert cb_spec.failure_count == 0
        assert cb_spec.last_failure_time == 0

    def test_circuit_breaker_exception_handling(self):
        """Tests exception handling"""

        # Creating a specification that can raise exceptions
        def failing_spec(candidate):
            if candidate == 0:
                raise ValueError("Zero is not allowed")
            return candidate > 5

        base_spec = lambda_spec(failing_spec)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=2)

        # Exception counts as failure
        assert cb_spec.is_satisfied_by(0) is False
        assert cb_spec.failure_count == 1

        # Second failure (value doesn't satisfy)
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.failure_count == 2

        # Circuit breaker activates
        assert cb_spec.is_satisfied_by(10) is False

    def test_circuit_breaker_success_after_failures(self):
        """Tests success after some failures (doesn't activate circuit breaker)"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=3)

        # Two failures
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(2) is False
        assert cb_spec.failure_count == 2

        # One success - doesn't activate circuit breaker
        assert cb_spec.is_satisfied_by(10) is True
        assert cb_spec.failure_count == 2  # Keeps the counter

        # One more failure - still doesn't activate
        assert cb_spec.is_satisfied_by(1) is False
        assert cb_spec.failure_count == 3

        # Now activates
        assert cb_spec.is_satisfied_by(15) is False

    def test_circuit_breaker_half_open_state(self):
        """Tests HALF_OPEN state after timeout"""
        import time

        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(
            base_spec, failure_threshold=2, recover_timeout=0.1
        )

        # Activates the circuit breaker
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(2) is False

        # Wait for timeout
        time.sleep(0.2)

        # HALF_OPEN state - allows one attempt
        assert cb_spec.is_satisfied_by(10) is True

        # If it fails again, goes back to OPEN
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.failure_count == 1

    def test_circuit_breaker_with_different_specifications(self):
        """Tests circuit breaker with different types of specifications"""
        # With string specification
        string_spec = MinLengthSpecification(3)
        cb_string = CircuitBreakerSpecification(string_spec, failure_threshold=2)

        # Failures with strings
        assert cb_string.is_satisfied_by("a") is False
        assert cb_string.is_satisfied_by("ab") is False

        # Circuit breaker activates
        assert cb_string.is_satisfied_by("abc") is False

        # With numeric specification
        num_spec = BetweenSpecification(5, 15)
        cb_num = CircuitBreakerSpecification(num_spec, failure_threshold=2)

        # Failures with numbers
        assert cb_num.is_satisfied_by(3) is False
        assert cb_num.is_satisfied_by(20) is False

        # Circuit breaker activates
        assert cb_num.is_satisfied_by(10) is False

    def test_circuit_breaker_edge_cases(self):
        """Tests edge cases of the circuit breaker"""
        base_spec = GreaterThanSpecification(5)

        # Threshold = 1 (activates immediately)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=1)
        assert cb_spec.is_satisfied_by(3) is False
        assert cb_spec.is_satisfied_by(10) is False  # Already activated

        # Threshold = 0 (always active - blocks immediately)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=0)
        # With threshold 0, any failure activates the circuit breaker
        assert cb_spec.is_satisfied_by(3) is False  # First failure activates
        assert cb_spec.is_satisfied_by(10) is False  # Already activated

        # Very high threshold
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=100)
        for i in range(50):  # Many failures
            cb_spec.is_satisfied_by(3)
        assert cb_spec.failure_count == 50
        assert cb_spec.is_satisfied_by(10) is True  # Still works

    def test_circuit_breaker_state_transitions(self):
        """Tests circuit breaker state transitions"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(
            base_spec, failure_threshold=2, recover_timeout=0.1
        )

        # CLOSED -> OPEN state
        assert cb_spec.is_satisfied_by(3) is False  # failure_count = 1
        assert cb_spec.is_satisfied_by(2) is False  # failure_count = 2, OPEN

        # OPEN state (blocks all calls)
        assert cb_spec.is_satisfied_by(10) is False
        assert cb_spec.is_satisfied_by(15) is False

        # OPEN -> HALF_OPEN (after timeout)
        import time

        time.sleep(0.2)

        # HALF_OPEN: allows one attempt
        assert cb_spec.is_satisfied_by(10) is True

        # HALF_OPEN -> CLOSED (if success) or OPEN (if failure)
        assert cb_spec.is_satisfied_by(10) is True  # Continues working

    def test_circuit_breaker_reset_behavior(self):
        """Tests reset method behavior"""
        base_spec = GreaterThanSpecification(5)
        cb_spec = CircuitBreakerSpecification(base_spec, failure_threshold=2)

        # Accumulates some failures
        cb_spec.is_satisfied_by(3)
        cb_spec.is_satisfied_by(2)

        # Check state before reset
        assert cb_spec.failure_count > 0
        assert cb_spec.last_failure_time > 0

        # Reset
        cb_spec.reset()

        # Check state after reset
        assert cb_spec.failure_count == 0
        assert cb_spec.last_failure_time == 0

        # Should work normally
        assert cb_spec.is_satisfied_by(10) is True
