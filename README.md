# app_meshed

**HTTP services and frontend for meshed operations**

A modular, source-keyed architecture for DAG construction, data storage, and stream visualization built on the i2mint ecosystem (`meshed`, `dol`, `i2`, `creek`, `ju`, `qh`).

## Overview

`app_meshed` provides a web-based platform to:
- Compose and execute `meshed` DAGs through a visual interface
- Access data through flat, key-value interfaces (source-keyed architecture)
- Visualize multi-dimensional time-series streams
- Generate forms automatically from function signatures

## Architecture

### Core Philosophy

**Source-Keyed Data:** All data is accessed via flat, key-value interfaces (Mappings) provided by `dol`.

**Interface-First:** Python functions are the source of truth. Their signatures (`i2`) drive frontend forms (`ju` + RJSF) and API endpoints.

### The Stack

- **Storage Layer:** `dol` - Abstracts local files, S3, or DBs into dict-like interfaces
- **Logic Layer:** `meshed` - DAGs and Slabs for workflow composition
- **Stream Layer:** `creek` - Time-series data with `[bt:tt]` slicing
- **Adaptation Layer:** `i2` - Function signature introspection, `ju` - JSON Schema generation
- **Service Layer:** FastAPI - HTTP endpoints for all operations
- **Frontend:** React + React Flow (visual graphs) + RJSF (forms) *(to be implemented)*

## Installation

```bash
# Clone the repository
git clone https://github.com/i2mint/app_meshed.git
cd app_meshed

# Install dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Running the Server

```bash
# Start the server (default: http://0.0.0.0:8000)
python -m app_meshed.cli

# Custom port and data directory
python -m app_meshed.cli --port 8080 --data-path /path/to/data

# Enable auto-reload for development
python -m app_meshed.cli --reload --debug
```

### API Documentation

Once the server is running, visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

### Basic Usage Examples

#### 1. List Available Functions

```bash
curl http://localhost:8000/functions
```

#### 2. Get Function Schema (for form generation)

```bash
curl http://localhost:8000/schema/function/add
```

#### 3. Execute a Simple DAG

```bash
curl -X POST http://localhost:8000/dag/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dag_config": {
      "name": "simple_add",
      "nodes": [
        {"id": "add_node", "function": "add"}
      ],
      "edges": []
    },
    "inputs": {
      "add_node": {"a": 5, "b": 3}
    }
  }'
```

#### 4. Access Time-Series Data

```bash
# List available streams
curl http://localhost:8000/streams

# Slice a stream by time range [bt:tt]
curl "http://localhost:8000/streams/audio_sample/slice?bt=0.0&tt=1.0"

# Get synchronized multi-channel data
curl -X POST http://localhost:8000/streams/multi-channel/slice \
  -H "Content-Type: application/json" \
  -d '{
    "channel_ids": ["sensor_accel_x", "sensor_accel_y"],
    "bt": 0.0,
    "tt": 5.0
  }'
```

## Project Structure

```
app_meshed/
├── app_meshed/
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   └── startup.py       # Initialization tasks
│   ├── stores/
│   │   └── root_store.py    # Unified dol-based storage
│   ├── services/
│   │   ├── function_registry.py  # Function introspection (i2)
│   │   ├── schema_service.py     # JSON Schema generation (ju)
│   │   ├── dag_service.py        # DAG serialization/execution (meshed)
│   │   └── stream_service.py     # Stream slicing (creek)
│   └── utils/
│       └── example_functions.py  # Sample functions for DAG composition
├── data/                    # Default data directory (gitignored)
│   ├── raw_data/           # Binary blobs (audio, sensor data)
│   ├── functions/          # Saved functions (pickled)
│   ├── meshes/             # DAG configurations (JSON)
│   └── configs/            # Application configs (JSON)
└── pyproject.toml
```

## API Endpoints

### Store API (Phase I)

- `GET /store/list` - List all available stores
- `GET /store/{store_name}/keys` - List keys in a store
- `GET /store/{store_name}/{key}` - Get an item from a store
- `PUT /store/{store_name}/{key}` - Store an item
- `DELETE /store/{store_name}/{key}` - Delete an item

### Function API (Phase I)

- `GET /functions` - List all registered functions
- `GET /functions/{name}/metadata` - Get function metadata

### Schema API (Phase I & II)

- `GET /schema/function/{name}` - Get JSON Schema for a function's parameters
- `POST /schema/object` - Generate schema from an object
- `GET /schema/dag-config` - Get DAG configuration schema

### DAG API (Phase II)

- `POST /dag/execute` - Execute a DAG from JSON config
- `POST /dag/validate` - Validate DAG config without executing
- `GET /dag/examples` - Get example DAG configurations

### Stream API (Phase III)

- `GET /streams` - List all registered streams
- `GET /streams/{id}/metadata` - Get stream metadata
- `GET /streams/{id}/slice?bt=0&tt=10` - Slice stream by time range
- `POST /streams/multi-channel/slice` - Get synchronized multi-channel data
- `POST /streams/multi-channel/info` - Get multi-channel metadata

## Development Phases

### Phase I: Store Explorer ✅
- Unified dol-based storage interface
- Function registry with i2 signatures
- HTTP service with store CRUD operations
- Schema generation with ju

### Phase II: Mesh Maker (DAG Builder) ✅
- DAG JSON serialization/deserialization
- Schema endpoints for function parameters
- DAG execution and validation
- Example DAG configurations

### Phase III: Multi-Channel Viewer ✅
- Stream abstraction with creek
- [bt:tt] time-based slicing
- Multi-channel synchronization
- Sample stream generation

### Next Steps (Frontend)
- React-based Store Browser UI
- React Flow canvas for visual DAG composition
- RJSF forms for node configuration
- Plotly/Chart.js for stream visualization

## Key Concepts

### Source-Keyed Architecture

All data sources are accessed through a uniform Mapping interface:

```python
from app_meshed.stores.root_store import create_default_root_store

root = create_default_root_store()
root.meshes["my_dag"] = {"nodes": [...], "edges": [...]}
config = root.configs["app_settings"]
```

### Function Signatures Drive Everything

Functions registered in the system are introspected using `i2`, and their schemas are generated with `ju`:

```python
def process(audio: np.ndarray, gain: float = 1.0) -> np.ndarray:
    """Apply gain to audio signal."""
    return audio * gain
```

This automatically generates:
- API endpoint: `/schema/function/process`
- JSON Schema for RJSF forms
- Parameter metadata for the frontend

### Time-Based Slicing with [bt:tt]

Stream data is accessed using time ranges:

```python
stream = stream_registry.get("audio_sample")
chunk = stream[0.5:1.5]  # Get data from 0.5s to 1.5s
```

## Contributing

See the main [i2mint organization](https://github.com/i2mint) for contribution guidelines.

## License

MIT
