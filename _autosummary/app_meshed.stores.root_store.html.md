# app_meshed.stores.root_store

Unified store interface using dol for source-keyed data access.

This module implements the Root Store pattern, providing a fanout interface
to different data sources:

- raw_data: Binary blobs (audio, sensor data, etc.)
- functions: Callable functions available for DAG composition
- meshes: Saved DAG configurations (JSON)
- configs: Application configurations

### Functions

| [`create_default_root_store`](#app_meshed.stores.root_store.create_default_root_store)([base_path])   | Factory function to create a default root store.   |
|-------------------------------------------------------------------------------------------|----------------------------------------------------|

### Classes

| [`RootStore`](#app_meshed.stores.root_store.RootStore)([base_path])   | Root store that provides access to all sub-stores.   |
|---------------------------------------------------------------------------|------------------------------------------------------|

### *class* app_meshed.stores.root_store.RootStore(base_path='./data')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Root store that provides access to all sub-stores.

This implements a fanout pattern where different data types are accessed
through dedicated sub-stores, all unified under a single interface.

### Example

```pycon
>>> import tempfile
>>> root = RootStore(base_path=tempfile.mkdtemp())
>>> [hasattr(root, name) for name in ("raw_data", "functions", "meshes")]
[True, True, True]
```

#### get_store(store_name)

Get a specific sub-store by name.

* **Parameters:**
  **store_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the store (raw_data, functions, meshes, configs)
* **Return type:**
  [`Mapping`](https://docs.python.org/3/library/typing.html#typing.Mapping)
* **Returns:**
  The requested store
* **Raises:**
  [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If store_name is not valid

#### list_all_keys()

List all keys across all sub-stores.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]
* **Returns:**
  Dictionary mapping store names to lists of keys

### app_meshed.stores.root_store.create_default_root_store(base_path='./data')

Factory function to create a default root store.

* **Parameters:**
  **base_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Base directory for storing data
* **Return type:**
  [`RootStore`](#app_meshed.stores.root_store.RootStore)
* **Returns:**
  Configured RootStore instance
