# app_meshed.api.main

Main FastAPI application for app_meshed.

This module provides the HTTP API for:

- Store browsing and CRUD operations
- Function introspection and schema generation
- DAG composition and execution
- Stream visualization

### Functions

| [`delete_store_item`](#app_meshed.api.main.delete_store_item)(store_name, key)         | Delete an item from a store.                       |
|---------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`execute_dag`](#app_meshed.api.main.execute_dag)([dag_config, inputs])          | Execute a DAG from JSON configuration.             |
| [`get_dag_examples`](#app_meshed.api.main.get_dag_examples)()                         | Get example DAG configurations.                    |
| [`get_dag_schema`](#app_meshed.api.main.get_dag_schema)()                           | Get JSON Schema for DAG configuration.             |
| [`get_function_metadata`](#app_meshed.api.main.get_function_metadata)(function_name)       | Get metadata for a specific function.              |
| [`get_function_schema`](#app_meshed.api.main.get_function_schema)(function_name)         | Get JSON Schema for a function (for RJSF forms).   |
| [`get_multi_channel_info`](#app_meshed.api.main.get_multi_channel_info)([channel_ids])      | Get metadata for multiple channels.                |
| [`get_object_schema`](#app_meshed.api.main.get_object_schema)([obj, title])            | Get JSON Schema for an object.                     |
| [`get_stats`](#app_meshed.api.main.get_stats)()                                | Get statistics about the application state.        |
| [`get_store_item`](#app_meshed.api.main.get_store_item)(store_name, key)            | Get an item from a store.                          |
| [`get_stream_metadata`](#app_meshed.api.main.get_stream_metadata)(source_id)             | Get metadata for a specific stream.                |
| [`health`](#app_meshed.api.main.health)()                                   | Health check endpoint.                             |
| [`list_functions`](#app_meshed.api.main.list_functions)()                           | List all registered functions.                     |
| [`list_store_keys`](#app_meshed.api.main.list_store_keys)(store_name)                | List all keys in a specific store.                 |
| [`list_stores`](#app_meshed.api.main.list_stores)()                              | List all available stores.                         |
| [`list_streams`](#app_meshed.api.main.list_streams)()                             | List all registered streams.                       |
| [`put_store_item`](#app_meshed.api.main.put_store_item)(store_name, key[, value])   | Store an item in a store.                          |
| [`root`](#app_meshed.api.main.root)()                                     | Root endpoint with API information.                |
| [`slice_multi_channel`](#app_meshed.api.main.slice_multi_channel)([channel_ids, bt, tt]) | Get synchronized slices from multiple channels.    |
| [`slice_stream`](#app_meshed.api.main.slice_stream)(source_id[, bt, tt])          | Slice a stream by time range [bt:tt].              |
| [`startup_event`](#app_meshed.api.main.startup_event)()                            | Run initialization tasks on server startup.        |
| [`validate_dag`](#app_meshed.api.main.validate_dag)([dag_config])                 | Validate a DAG configuration without executing it. |

### *async* app_meshed.api.main.delete_store_item(store_name, key)

Delete an item from a store.

* **Parameters:**
  * **store_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the store
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Key of the item to delete
* **Returns:**
  Confirmation message

### *async* app_meshed.api.main.execute_dag(dag_config=Body(PydanticUndefined), inputs=Body({}))

Execute a DAG from JSON configuration.

* **Parameters:**
  * **dag_config** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – DAG configuration (nodes, edges, params)
  * **inputs** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – Input values for execution
* **Returns:**
  Execution result

### *async* app_meshed.api.main.get_dag_examples()

Get example DAG configurations.

* **Returns:**
  List of example DAG configurations

### *async* app_meshed.api.main.get_dag_schema()

Get JSON Schema for DAG configuration.

* **Returns:**
  JSON Schema for DAG configuration

### *async* app_meshed.api.main.get_function_metadata(function_name)

Get metadata for a specific function.

* **Parameters:**
  **function_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the function
* **Returns:**
  Function metadata including parameters, types, and documentation

### *async* app_meshed.api.main.get_function_schema(function_name)

Get JSON Schema for a function (for RJSF forms).

* **Parameters:**
  **function_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the function
* **Returns:**
  JSON Schema for the function’s parameters

### *async* app_meshed.api.main.get_multi_channel_info(channel_ids=Body(PydanticUndefined))

Get metadata for multiple channels.

* **Parameters:**
  **channel_ids** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of channel IDs
* **Returns:**
  Metadata for each channel

### *async* app_meshed.api.main.get_object_schema(obj=Body(PydanticUndefined), title=None)

Get JSON Schema for an object.

* **Parameters:**
  * **obj** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Object to generate schema for
  * **title** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional title for the schema
* **Returns:**
  JSON Schema for the object

### *async* app_meshed.api.main.get_stats()

Get statistics about the application state.

* **Returns:**
  Statistics about stores and functions

### *async* app_meshed.api.main.get_store_item(store_name, key)

Get an item from a store.

* **Parameters:**
  * **store_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the store
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Key of the item to retrieve
* **Returns:**
  The requested item

### *async* app_meshed.api.main.get_stream_metadata(source_id)

Get metadata for a specific stream.

* **Parameters:**
  **source_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Stream identifier
* **Returns:**
  Stream metadata

### *async* app_meshed.api.main.health()

Health check endpoint.

### *async* app_meshed.api.main.list_functions()

List all registered functions.

* **Returns:**
  List of function names and their metadata

### *async* app_meshed.api.main.list_store_keys(store_name)

List all keys in a specific store.

* **Parameters:**
  **store_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the store (raw_data, functions, meshes, configs)
* **Returns:**
  List of keys in the store

### *async* app_meshed.api.main.list_stores()

List all available stores.

### *async* app_meshed.api.main.list_streams()

List all registered streams.

* **Returns:**
  List of stream IDs and their metadata

### *async* app_meshed.api.main.put_store_item(store_name, key, value=Body(PydanticUndefined))

Store an item in a store.

* **Parameters:**
  * **store_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the store
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Key to store the item under
  * **value** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Value to store
* **Returns:**
  Confirmation message

### *async* app_meshed.api.main.root()

Root endpoint with API information.

### *async* app_meshed.api.main.slice_multi_channel(channel_ids=Body(PydanticUndefined), bt=Body(0.0), tt=Body(10.0))

Get synchronized slices from multiple channels.

* **Parameters:**
  * **channel_ids** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of stream/channel IDs
  * **bt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Bottom time (start) in seconds
  * **tt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Top time (end) in seconds
* **Returns:**
  Synchronized multi-channel data

### *async* app_meshed.api.main.slice_stream(source_id, bt=0.0, tt=None)

Slice a stream by time range [bt:tt].

* **Parameters:**
  * **source_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Stream identifier
  * **bt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Bottom time (start) in seconds
  * **tt** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]) – Top time (end) in seconds (None = end of stream)
* **Returns:**
  Sliced stream data

### *async* app_meshed.api.main.startup_event()

Run initialization tasks on server startup.

### *async* app_meshed.api.main.validate_dag(dag_config=Body(PydanticUndefined))

Validate a DAG configuration without executing it.

* **Parameters:**
  **dag_config** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – DAG configuration to validate
* **Returns:**
  Validation result
