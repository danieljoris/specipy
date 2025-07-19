from src.utils import filter_by_spec, lambda_spec


class TestLambdaSpec:
    def test_lambda_spec_true_condition(self):
        is_even = lambda_spec(lambda x: x % 2 == 0)
        assert is_even(2)
        assert is_even(4)
        assert not is_even(3)

    def test_lambda_spec_false_condition(self):
        is_positive = lambda_spec(lambda x: x > 0)
        assert is_positive(10)
        assert not is_positive(-5)
        assert not is_positive(0)


class TestFilterBySpec:
    def test_filter_even_numbers(self):
        numbers = [1, 2, 3, 4, 5, 6]
        is_even = lambda_spec(lambda x: x % 2 == 0)

        result = list(filter_by_spec(numbers, is_even))
        assert result == [2, 4, 6]

    def test_filter_empty_result(self):
        numbers = [1, 3, 5]
        is_even = lambda_spec(lambda x: x % 2 == 0)

        result = list(filter_by_spec(numbers, is_even))
        assert result == []

    def test_filter_all_match(self):
        numbers = [10, 20, 30]
        is_multiple_of_10 = lambda_spec(lambda x: x % 10 == 0)

        result = list(filter_by_spec(numbers, is_multiple_of_10))
        assert result == [10, 20, 30]
