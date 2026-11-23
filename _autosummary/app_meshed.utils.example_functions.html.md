# app_meshed.utils.example_functions

Example functions for DAG composition.

These functions are automatically registered on startup and can be used
to build DAGs in the Mesh Maker UI.

### Functions

| [`absolute_value`](#app_meshed.utils.example_functions.absolute_value)(x)              | Get the absolute value of x.                |
|---------------------------------------------------------------------------------|---------------------------------------------|
| [`add`](#app_meshed.utils.example_functions.add)(a, b)                      | Add two numbers.                            |
| [`concatenate`](#app_meshed.utils.example_functions.concatenate)(a, b[, separator]) | Concatenate two strings with a separator.   |
| [`divide`](#app_meshed.utils.example_functions.divide)(a, b)                   | Divide a by b.                              |
| [`list_average`](#app_meshed.utils.example_functions.list_average)(numbers)          | Calculate the average of numbers in a list. |
| [`list_sum`](#app_meshed.utils.example_functions.list_sum)(numbers)              | Sum all numbers in a list.                  |
| [`multiply`](#app_meshed.utils.example_functions.multiply)(a, b)                 | Multiply two numbers.                       |
| [`power`](#app_meshed.utils.example_functions.power)(base[, exponent])        | Raise base to the power of exponent.        |
| [`string_length`](#app_meshed.utils.example_functions.string_length)(text)            | Get the length of a string.                 |
| [`subtract`](#app_meshed.utils.example_functions.subtract)(a, b)                 | Subtract b from a.                          |
| [`to_lowercase`](#app_meshed.utils.example_functions.to_lowercase)(text)             | Convert text to lowercase.                  |
| [`to_uppercase`](#app_meshed.utils.example_functions.to_uppercase)(text)             | Convert text to uppercase.                  |

### app_meshed.utils.example_functions.absolute_value(x)

Get the absolute value of x.

* **Parameters:**
  **x** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Input number
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Absolute value of x

### app_meshed.utils.example_functions.add(a, b)

Add two numbers.

* **Parameters:**
  * **a** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – First number
  * **b** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Second number
* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
* **Returns:**
  Sum of a and b

### app_meshed.utils.example_functions.concatenate(a, b, separator=' ')

Concatenate two strings with a separator.

* **Parameters:**
  * **a** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – First string
  * **b** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Second string
  * **separator** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Separator to use (default: space)
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Concatenated string

### app_meshed.utils.example_functions.divide(a, b)

Divide a by b.

* **Parameters:**
  * **a** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Numerator
  * **b** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Denominator
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Quotient (a / b)
* **Raises:**
  [**ZeroDivisionError**](https://docs.python.org/3/builtins/exceptions.html#ZeroDivisionError) – If b is zero

### app_meshed.utils.example_functions.list_average(numbers)

Calculate the average of numbers in a list.

* **Parameters:**
  **numbers** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)) – List of numbers
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Average value
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If list is empty

### app_meshed.utils.example_functions.list_sum(numbers)

Sum all numbers in a list.

* **Parameters:**
  **numbers** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)) – List of numbers
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Sum of all numbers

### app_meshed.utils.example_functions.multiply(a, b)

Multiply two numbers.

* **Parameters:**
  * **a** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – First number
  * **b** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Second number
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Product of a and b

### app_meshed.utils.example_functions.power(base, exponent=2.0)

Raise base to the power of exponent.

* **Parameters:**
  * **base** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Base number
  * **exponent** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Exponent (default: 2.0)
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  base \*\* exponent

### app_meshed.utils.example_functions.string_length(text)

Get the length of a string.

* **Parameters:**
  **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input string
* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
* **Returns:**
  Length of the string

### app_meshed.utils.example_functions.subtract(a, b)

Subtract b from a.

* **Parameters:**
  * **a** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – First number
  * **b** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Number to subtract
* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
* **Returns:**
  Difference (a - b)

### app_meshed.utils.example_functions.to_lowercase(text)

Convert text to lowercase.

* **Parameters:**
  **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input string
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Lowercase version of text

### app_meshed.utils.example_functions.to_uppercase(text)

Convert text to uppercase.

* **Parameters:**
  **text** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Input string
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Uppercase version of text
