# app_meshed.api.startup

Startup initialization for app_meshed.

This module handles initialization tasks that run when the server starts:

- Registering example functions
- Setting up default stores
- Initializing sample data

### Functions

| [`initialize_sample_streams`](#app_meshed.api.startup.initialize_sample_streams)([data_path])   | Initialize sample stream sources for demonstration.    |
|-------------------------------------------------------------------------------------------|--------------------------------------------------------|
| [`register_example_functions`](#app_meshed.api.startup.register_example_functions)()             | Register all example functions in the global registry. |
| [`run_startup_initialization`](#app_meshed.api.startup.run_startup_initialization)([data_path])  | Run all startup initialization tasks.                  |

### app_meshed.api.startup.initialize_sample_streams(data_path='./data')

Initialize sample stream sources for demonstration.

* **Parameters:**
  **data_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Base path for data storage

### app_meshed.api.startup.register_example_functions()

Register all example functions in the global registry.

### app_meshed.api.startup.run_startup_initialization(data_path='./data')

Run all startup initialization tasks.

* **Parameters:**
  **data_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Base path for data storage
