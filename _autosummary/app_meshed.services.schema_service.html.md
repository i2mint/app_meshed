# app_meshed.services.schema_service

Schema generation service using ju (JSON Schema utilities).

This module provides schema generation from:

- Function signatures (via i2 + ju)
- Python objects
- Custom types

Schemas are used to generate forms in the frontend (RJSF).

### Functions

| [`func_to_schema`](#app_meshed.services.schema_service.func_to_schema)(func[, title])   | Generate JSON Schema from a function.      |
|----------------------------------------------------------------------------------|--------------------------------------------|
| [`get_dag_config_schema`](#app_meshed.services.schema_service.get_dag_config_schema)()         | Get the JSON Schema for DAG configuration. |
| [`object_to_schema`](#app_meshed.services.schema_service.object_to_schema)(obj[, title])  | Generate JSON Schema from an object.       |

### Classes

| [`SchemaGenerator`](#app_meshed.services.schema_service.SchemaGenerator)()   | Generate JSON Schemas from various sources.   |
|----------------------------------------------------------------------|-----------------------------------------------|

### *class* app_meshed.services.schema_service.SchemaGenerator

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Generate JSON Schemas from various sources.

This class uses ju and i2 to convert Python types, function signatures,
and objects into JSON Schema format suitable for RJSF form generation.

#### dag_config_schema()

Generate schema for DAG configuration.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema for DAG configuration

#### function_to_schema(func, title=None)

Generate JSON Schema from a function signature.

* **Parameters:**
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Function to generate schema for
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title for the schema
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema dict suitable for RJSF

#### *static* get_default_value(param)

Extract default value from parameter.

* **Parameters:**
  **param** ([`Parameter`](https://docs.python.org/3/library/inspect.html#inspect.Parameter)) – Function parameter
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Default value or None

#### object_to_schema(obj, title=None)

Generate JSON Schema from a Python object.

* **Parameters:**
  * **obj** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Object to generate schema for
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title for the schema
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema dict

#### *static* python_type_to_json_type(py_type)

Convert Python type to JSON Schema type.

* **Parameters:**
  **py_type** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Python type annotation
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  JSON Schema type string

### app_meshed.services.schema_service.func_to_schema(func, title=None)

Generate JSON Schema from a function.

* **Parameters:**
  * **func** ([`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)) – Function to generate schema for
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema dict

### app_meshed.services.schema_service.get_dag_config_schema()

Get the JSON Schema for DAG configuration.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema dict

### app_meshed.services.schema_service.object_to_schema(obj, title=None)

Generate JSON Schema from an object.

* **Parameters:**
  * **obj** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Object to generate schema for
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON Schema dict
