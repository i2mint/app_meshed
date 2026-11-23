# app_meshed.services.dag_service

DAG service for meshed operations.

This module provides:

- DAG serialization/deserialization (JSON <-> meshed.DAG)
- DAG construction from JSON configurations
- DAG execution

### Functions

| [`create_chained_dag_example`](#app_meshed.services.dag_service.create_chained_dag_example)()   | Create a chained DAG configuration example.   |
|---------------------------------------------------------------------------------|-----------------------------------------------|
| [`create_simple_dag_example`](#app_meshed.services.dag_service.create_simple_dag_example)()    | Create a simple DAG configuration example.    |

### Classes

| [`DAGService`](#app_meshed.services.dag_service.DAGService)(function_registry)   | Service for managing and executing meshed DAGs.   |
|----------------------------------------------------------------------------------|---------------------------------------------------|

### *class* app_meshed.services.dag_service.DAGService(function_registry)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Service for managing and executing meshed DAGs.

This service handles:

- Converting JSON configs to live DAG objects
- Executing DAGs with provided inputs
- Serializing DAG definitions

#### dag_to_json(dag)

Convert a DAG object to JSON configuration.

* **Parameters:**
  **dag** (`DAG`) – DAG object
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  JSON-serializable dictionary

#### NOTE
This is a simplified serialization. Full serialization
would require introspecting the DAG structure.

#### execute_dag(dag, inputs)

Execute a DAG with given inputs.

* **Parameters:**
  * **dag** (`DAG`) – DAG to execute
  * **inputs** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – Dictionary of input values
* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
* **Returns:**
  DAG execution result

#### execute_from_config(dag_config, inputs)

Execute a DAG from JSON configuration.

* **Parameters:**
  * **dag_config** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – DAG configuration
  * **inputs** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – Input values for execution
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with execution result and metadata

#### json_to_dag(dag_config)

Convert a JSON configuration to a meshed.DAG object.

* **Parameters:**
  **dag_config** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – 

  Dictionary with DAG configuration
  {
  > ”name”: “my_dag”,
  > “nodes”: [
  > > {
  > > : “id”: “node1”,
  > >   “function”: “add”,
  > >   “output_name”: “sum”

  > ],
  > “edges”: [
  > > {
  > > : “source”: “node1”,
  > >   “target”: “node2”,
  > >   “sourceOutput”: “sum”,
  > >   “targetInput”: “a”

  > ],
  > “params”: {
  > > ”node1”: {“a”: 5, “b”: 3}

  > }

  }
* **Return type:**
  `DAG`
* **Returns:**
  Constructed DAG object
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If configuration is invalid

### app_meshed.services.dag_service.create_chained_dag_example()

Create a chained DAG configuration example.

This creates a DAG that:

1. Adds two numbers (a + b)
2. Multiplies the result by c

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  Example DAG configuration

### app_meshed.services.dag_service.create_simple_dag_example()

Create a simple DAG configuration example.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)
* **Returns:**
  Example DAG configuration
