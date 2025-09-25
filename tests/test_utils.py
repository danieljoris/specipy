from src.base import Specification
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

    def test_lambda_spec_with_strings(self):
        has_min_length = lambda_spec(lambda s: len(s) >= 3)
        assert has_min_length("abc")
        assert has_min_length("abcd")
        assert not has_min_length("ab")

    def test_lambda_spec_with_custom_objects(self):
        class User:
            user: str
            age: int

            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age

        is_adult = lambda_spec(lambda user: user.age >= 18)

        user1 = User("João", 20)
        user2 = User("Maria", 16)

        assert is_adult(user1) is True
        assert is_adult(user2) is False

    def test_lambda_spec_with_implicit_type(self):
        is_even = lambda_spec(lambda x: x % 2 == 0)
        assert is_even(2)
        assert is_even(4)
        assert not is_even(3)

    def test_lambda_spec_with_explicit_type(self):
        is_even: Specification[int] = lambda_spec(lambda x: x % 2 == 0)
        assert is_even(2)
        assert is_even(4)
        assert not is_even(3)


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

    def test_filter_with_strings(self):
        words = ["a", "ab", "abc", "abcd", "abcde"]
        has_min_length = lambda_spec(lambda s: len(s) >= 3)

        result = list(filter_by_spec(words, has_min_length))
        assert result == ["abc", "abcd", "abcde"]

    def test_filter_with_custom_specifications(self):
        from src.extensions import GreaterThanSpecification

        numbers = [1, 5, 10, 15, 20]
        greater_than_ten = GreaterThanSpecification(10)

        result = list(filter_by_spec(numbers, greater_than_ten))
        assert result == [15, 20]

    def test_filter_empty_iterable(self):
        empty_list = []
        is_even = lambda_spec(lambda x: x % 2 == 0)

        result = list(filter_by_spec(empty_list, is_even))
        assert result == []
