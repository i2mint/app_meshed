# app_meshed.services.function_registry

Function registry with i2 signature introspection.

This module provides a registry for functions that will be used in DAG composition.
It uses i2 to ensure clean, inspectable signatures and provides metadata about
each function’s parameters, types, and documentation.

### Functions

| [`get_global_registry`](#app_meshed.services.function_registry.get_global_registry)()                         | Get the global function registry instance.   |
|------------------------------------------------------------------------------------------------|----------------------------------------------|
| [`register_function`](#app_meshed.services.function_registry.register_function)(name, func, \*[, override]) | Register a function in the global registry.  |

### Classes

| [`FunctionMetadata`](#app_meshed.services.function_registry.FunctionMetadata)(name, doc, parameters, ...)    | Metadata about a registered function.                   |
|--------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [`FunctionRegistry`](#app_meshed.services.function_registry.FunctionRegistry)()                              | Registry for functions with i2 signature introspection. |
| [`ParameterInfo`](#app_meshed.services.function_registry.ParameterInfo)(name, annotation[, default, ...]) | Information about a function parameter.                 |

### *class* app_meshed.services.function_registry.FunctionMetadata(name, doc, parameters, return_annotation, module=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Metadata about a registered function.

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* app_meshed.services.function_registry.FunctionRegistry

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Registry for functions with i2 signature introspection.

This registry maintains a collection of functions that can be used
in DAG composition. It uses i2.Sig to extract and normalize function
signatures, making them inspectable and usable for form generation.

### Example

```pycon
>>> registry = FunctionRegistry()
>>> def add(a: int, b: int) -> int:
...     return a + b
>>> registry.register("add", add)
>>> metadata = registry.get_metadata("add")
>>> [p.name for p in metadata.parameters]
['a', 'b']
```

#### get_all_metadata()

Get metadata for all registered functions.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)]
* **Returns:**
  Dictionary mapping function names to metadata dicts

#### get_function(name)

Get a registered function by name.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Function name
* **Return type:**
  [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)
* **Returns:**
  The registered function
* **Raises:**
  [**KeyError**](https://docs.python.org/3/builtins/exceptions.html#KeyError) – If function not found

#### get_metadata(name)

Get metadata for a registered function.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Function name
* **Return type:**
  [`FunctionMetadata`](#app_meshed.services.function_registry.FunctionMetadata)
* **Returns:**
  FunctionMetadata for the function
* **Raises:**
  [**KeyError**](https://docs.python.org/3/builtins/exceptions.html#KeyError) – If function not found

#### list_functions()

List all registered function names.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of function names

#### register(name, func, , override=False)

Register a function in the registry.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name to register the function under
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – The callable to register
  * **override** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, allow overriding existing registrations
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If function already registered and override=False
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### unregister(name)

Remove a function from the registry.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Function name to remove
* **Raises:**
  [**KeyError**](https://docs.python.org/3/builtins/exceptions.html#KeyError) – If function not found
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### *class* app_meshed.services.function_registry.ParameterInfo(name, annotation, default=None, has_default=False, kind='POSITIONAL_OR_KEYWORD')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Information about a function parameter.

#### to_dict()

Convert to dictionary for JSON serialization.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### app_meshed.services.function_registry.get_global_registry()

Get the global function registry instance.

* **Return type:**
  [`FunctionRegistry`](#app_meshed.services.function_registry.FunctionRegistry)
* **Returns:**
  The global FunctionRegistry

### app_meshed.services.function_registry.register_function(name, func, , override=False)

Register a function in the global registry.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name to register the function under
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – The callable to register
  * **override** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, allow overriding existing registrations
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
