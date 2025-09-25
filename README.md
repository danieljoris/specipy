# SpeciPy
SpeciPy simplifies the implementation of the Specification pattern in Python, enabling easy creation and evaluation of flexible rules and criteria.

[![Build status](https://github.com/danieljoris/specipy/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/danieljoris/specipy/actions/workflows/ci.yml) [![Python Versions](https://img.shields.io/pypi/pyversions/specipy.svg)](https://pypi.org/project/specipy/) [![Package Version](https://badge.fury.io/py/specipy.svg)](https://pypi.org/project/specipy/) [![Coverage Status](https://codecov.io/gh/danieljoris/specipy/branch/main/graph/badge.svg?token=C70HMVKXDK)](https://codecov.io/gh/danieljoris/specipy) [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License](https://img.shields.io/github/license/danieljoris/specipy)](https://github.com/danieljoris/specipy/blob/main/LICENSE)

---

## 📋 Table of Contents

- [📥 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📈 Roadmap / Future Goals](#-roadmap--future-goals)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [📧 Contact](#-contact)

---

## 📥 Installation

To install Interpy with `pip`, you can use the following command:

```bash
pip install specipy
```
If you are using `poetry` you can use the command:

```bash
poetry add specipy
```

---

## 🚀 Usage

SpeciPy provides a clean and powerful implementation of the Specification Pattern in Python. It helps you encapsulate business rules or filtering logic in a reusable and composable way.

Below are practical examples of how to use specipy in real-world scenarios:


#### Defining and using a simple specification

```python
from specipy import Specification

class IsEven(Specification):
    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 == 0

spec = IsEven()
print(spec.is_satisfied_by(4))  # True
print(spec.is_satisfied_by(7))  # False
```


#### Combining specifications with boolean logic
```python
from specipy import Specification

class IsEven(Specification):
    def is_satisfied_by(self, candidate):
        return candidate % 2 == 0

class IsPositive(Specification):
    def is_satisfied_by(self, candidate):
        return candidate > 0

spec = IsEven() & IsPositive()

print(spec.is_satisfied_by(4))   # True (even and positive)
print(spec.is_satisfied_by(-2))  # False (even but negative)
print(spec.is_satisfied_by(3))   # False (odd)
```

You can also use | for OR and ~ for NOT:
```python
spec = IsEven() | IsPositive()
print(spec.is_satisfied_by(-3))  # False
print(spec.is_satisfied_by(3))   # True
```

#### Filtering collections with specifications
```python
from specipy import filter_by_spec, Specification

class StartsWithA(Specification):
    def is_satisfied_by(self, candidate):
        return candidate.lower().startswith("a")

names = ["Alice", "Bob", "anna", "Charles"]
spec = StartsWithA()

filtered = filter_by_spec(names, spec)
print(list(filtered))  # ['Alice', 'anna']
```

#### Validating complex domain rules
```python
class HasBalance(Specification):
    def is_satisfied_by(self, account):
        return account.balance > 0

class IsActive(Specification):
    def is_satisfied_by(self, account):
        return account.active

class Account:
    def __init__(self, balance, active):
        self.balance = balance
        self.active = active

account = Account(balance=100, active=True)
spec = HasBalance() & IsActive()

print(spec.is_satisfied_by(account))  # True
```
This allows rules to be isolated, tested independently, and composed into more complex conditions.

#### Dynamic one-off specifications with lambdas
```python
from specipy import lambda_spec

is_even = lambda_spec(lambda x: x % 2 == 0)

print(is_even.is_satisfied_by(10))  # True
```
Perfect for quick filters or dynamic rule creation without declaring classes.


---

## 📈 Roadmap / Future Goals
We plan to continue growing specipy into a robust, developer-friendly tool for business rule modeling. Some ideas we plan to explore:

#### ✅ Planned Features
- `__str__ / __repr__` for debugging
Clearer and descriptive output when printing specifications, like:
    ```python
    print(GreaterThanSpecification(10))
    # Output: GreaterThanSpecification(10)
    ```

- all_satisfied(specs) / any_satisfied(specs) 
Allows you to combine multiple specifications from a list dynamically:
    ```python
    specs = [
        lambda_spec(lambda x: x > 10),
        lambda_spec(lambda x: x % 2 == 0),
    ]

    assert all_satisfied(specs)(12)  # True
    assert any_satisfied(specs)(9)   # False
    ```

- spec.as_predicate() method
    Converts a specification into a simple callable predicate (function returning bool), making it easy to integrate with native Python functions like filter(), map(), or any functional programming context.
    ```python
    spec = GreaterThanSpecification(5)
    list(filter(spec.as_predicate(), [1, 6, 8]))  # [6, 8]
    ```
---

## 🤝 Contributing

Specipy is designed to grow with the community. If you have ideas for new features, improvements, or bug fixes, we warmly welcome your contributions! Feel free to open issues, discuss enhancements, or submit pull requests. Together, we can make this library even more powerful and developer-friendly.

If you would like to contribute to Specipy, please follow these steps:

1. Fork the repository
    `git clone git@github.com:danieljoris/specipy.git`
2. Create a branch for your feature 
    `git checkout -b feature/your-feature`
3. Commit your changes 
    `git commit -m 'Add your feature`
4. Push to the branch 
    `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 📧 Contact

Feel free to adjust and add more features as needed. If you need anything more specific or additional adjustments, let me know!
