"""Example functions for DAG composition.

These functions are automatically registered on startup and can be used
to build DAGs in the Mesh Maker UI.
"""


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: First number
        b: Number to subtract

    Returns:
        Difference (a - b)
    """
    return a - b


def divide(a: float, b: float) -> float:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Quotient (a / b)

    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float = 2.0) -> float:
    """Raise base to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent (default: 2.0)

    Returns:
        base ** exponent
    """
    return base ** exponent


def absolute_value(x: float) -> float:
    """Get the absolute value of x.

    Args:
        x: Input number

    Returns:
        Absolute value of x
    """
    return abs(x)


def concatenate(a: str, b: str, separator: str = " ") -> str:
    """Concatenate two strings with a separator.

    Args:
        a: First string
        b: Second string
        separator: Separator to use (default: space)

    Returns:
        Concatenated string
    """
    return f"{a}{separator}{b}"


def to_uppercase(text: str) -> str:
    """Convert text to uppercase.

    Args:
        text: Input string

    Returns:
        Uppercase version of text
    """
    return text.upper()


def to_lowercase(text: str) -> str:
    """Convert text to lowercase.

    Args:
        text: Input string

    Returns:
        Lowercase version of text
    """
    return text.lower()


def string_length(text: str) -> int:
    """Get the length of a string.

    Args:
        text: Input string

    Returns:
        Length of the string
    """
    return len(text)


def list_sum(numbers: list) -> float:
    """Sum all numbers in a list.

    Args:
        numbers: List of numbers

    Returns:
        Sum of all numbers
    """
    return sum(numbers)


def list_average(numbers: list) -> float:
    """Calculate the average of numbers in a list.

    Args:
        numbers: List of numbers

    Returns:
        Average value

    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


# List of all example functions
EXAMPLE_FUNCTIONS = [
    ("add", add),
    ("multiply", multiply),
    ("subtract", subtract),
    ("divide", divide),
    ("power", power),
    ("absolute_value", absolute_value),
    ("concatenate", concatenate),
    ("to_uppercase", to_uppercase),
    ("to_lowercase", to_lowercase),
    ("string_length", string_length),
    ("list_sum", list_sum),
    ("list_average", list_average),
]
