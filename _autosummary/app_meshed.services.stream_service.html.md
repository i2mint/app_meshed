# app_meshed.services.stream_service

Stream service using creek for time-series data slicing.

This module provides:

- Stream abstraction with [bt:tt] (bottom-time:top-time) slicing
- Multi-channel stream synchronization
- Time-series data access

### Functions

| [`get_stream_registry`](#app_meshed.services.stream_service.get_stream_registry)()   | Get the global stream registry.   |
|--------------------------------------------------------------------------|-----------------------------------|

### Classes

| [`FileStreamSource`](#app_meshed.services.stream_service.FileStreamSource)(source_id, file_path[, ...])   | Stream source backed by a file.                |
|--------------------------------------------------------------------------------------------------|------------------------------------------------|
| [`MultiChannelView`](#app_meshed.services.stream_service.MultiChannelView)(registry)                      | Synchronized view of multiple stream channels. |
| [`StreamRegistry`](#app_meshed.services.stream_service.StreamRegistry)()                                | Registry for managing multiple stream sources. |
| [`StreamSource`](#app_meshed.services.stream_service.StreamSource)(source_id[, sample_rate])          | Base class for stream sources.                 |

### *class* app_meshed.services.stream_service.FileStreamSource(source_id, file_path, sample_rate=1.0)

Bases: [`StreamSource`](#app_meshed.services.stream_service.StreamSource)

Stream source backed by a file.

Supports various file formats for time-series data.

#### get_metadata()

Get metadata including file info.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Stream metadata

### *class* app_meshed.services.stream_service.MultiChannelView(registry)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Synchronized view of multiple stream channels.

This implements the “Slabs” concept for multi-channel data.

#### get_channel_info(channel_ids)

Get metadata for multiple channels.

* **Parameters:**
  **channel_ids** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of channel IDs
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)]
* **Returns:**
  Dictionary mapping channel IDs to metadata

#### get_synchronized_slice(channel_ids, bt, tt)

Get synchronized data from multiple channels.

* **Parameters:**
  * **channel_ids** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of stream/channel IDs
  * **bt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Bottom time (start) in seconds
  * **tt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Top time (end) in seconds
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with synchronized multi-channel data

### *class* app_meshed.services.stream_service.StreamRegistry

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Registry for managing multiple stream sources.

#### get(source_id)

Get a stream by ID.

* **Parameters:**
  **source_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Stream identifier
* **Return type:**
  [`StreamSource`](#app_meshed.services.stream_service.StreamSource)
* **Returns:**
  StreamSource object
* **Raises:**
  [**KeyError**](https://docs.python.org/3/builtins/exceptions.html#KeyError) – If stream not found

#### get_all_metadata()

Get metadata for all streams.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)]
* **Returns:**
  Dictionary mapping stream IDs to metadata

#### list_streams()

List all registered stream IDs.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of stream IDs

#### register(stream)

Register a stream source.

* **Parameters:**
  **stream** ([`StreamSource`](#app_meshed.services.stream_service.StreamSource)) – Stream source to register
* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

#### slice_stream(source_id, bt, tt)

Slice a stream by time range.

* **Parameters:**
  * **source_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Stream identifier
  * **bt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Bottom time (start) in seconds
  * **tt** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Top time (end) in seconds
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with sliced data and metadata

### *class* app_meshed.services.stream_service.StreamSource(source_id, sample_rate=1.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Base class for stream sources.

Provides a uniform interface for accessing time-series data
with [bt:tt] slicing support.

#### get_metadata()

Get metadata about this stream.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dictionary with stream metadata

### app_meshed.services.stream_service.get_stream_registry()

Get the global stream registry.

* **Return type:**
  [`StreamRegistry`](#app_meshed.services.stream_service.StreamRegistry)
* **Returns:**
  Global StreamRegistry instance
