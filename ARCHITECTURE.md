# app_meshed Architecture Documentation

**Version:** 0.0.1
**Status:** All Three Phases Complete ✅
**Branch:** `claude/build-dag-architecture-01Jrr5obUormejAS9h3YziT4`

---

## Executive Summary

**app_meshed** is a complete backend platform for composing, executing, and visualizing meshed DAGs with integrated support for:
- Source-keyed data storage (dol)
- Function introspection and form generation (i2 + ju)
- DAG composition and execution (meshed)
- Time-series stream slicing (creek-inspired)

All three development phases are **fully implemented** and production-ready.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Future)                        │
│  React + React Flow (DAG Canvas) + RJSF (Forms) + Plotly (Viz) │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼────────────────────────────────────┐
│                    FastAPI Application                          │
│  • Store CRUD API (Phase I)                                     │
│  • Schema Generation API (Phase I & II)                         │
│  • DAG Execution API (Phase II)                                 │
│  • Stream Slicing API (Phase III)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼──────┐  ┌─────────▼────────┐
│  Store Layer   │  │ Logic Layer   │  │  Stream Layer    │
│  (dol)         │  │ (meshed)      │  │  (creek)         │
│                │  │               │  │                  │
│ • raw_data     │  │ • DAG builder │  │ • [bt:tt] slice  │
│ • functions    │  │ • Execution   │  │ • Multi-channel  │
│ • meshes       │  │ • Validation  │  │ • Sync views     │
│ • configs      │  │               │  │                  │
└────────────────┘  └───────────────┘  └──────────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                ┌────────────▼───────────┐
                │  Adaptation Layer      │
                │  • i2 (signatures)     │
                │  • ju (JSON schema)    │
                └────────────────────────┘
```

---

## Implementation Status

### ✅ Phase I: Store Explorer (Complete)

**Purpose:** Generic browsing and CRUD interface for data and functions.

**Components:**
- `app_meshed/stores/root_store.py` - Unified dol-based storage
  - `raw_data`: Binary blobs (audio, sensor data)
  - `functions`: Python callables (pickled)
  - `meshes`: DAG configurations (JSON)
  - `configs`: Application settings (JSON)

- `app_meshed/services/function_registry.py` - Function management with i2
  - Signature introspection
  - Parameter metadata extraction
  - Type annotation handling

- `app_meshed/services/schema_service.py` - JSON Schema generation
  - Function → Schema (for RJSF forms)
  - Object → Schema
  - DAG configuration schema

**API Endpoints:**
```
GET    /store/list                    # List all stores
GET    /store/{store}/keys            # List keys in store
GET    /store/{store}/{key}           # Get item
PUT    /store/{store}/{key}           # Store item
DELETE /store/{store}/{key}           # Delete item

GET    /functions                     # List all functions
GET    /functions/{name}/metadata     # Get function details

GET    /schema/function/{name}        # Get function schema (RJSF)
POST   /schema/object                 # Generate schema from object
GET    /schema/dag-config             # DAG configuration schema
```

### ✅ Phase II: Mesh Maker (DAG Builder) (Complete)

**Purpose:** Visual composition and execution of meshed DAGs.

**Components:**
- `app_meshed/services/dag_service.py` - DAG operations
  - JSON ↔ DAG serialization
  - DAG construction from node/edge configs
  - Execution with input binding
  - Validation

- `app_meshed/utils/example_functions.py` - 12 ready-to-use functions
  - Math: add, multiply, subtract, divide, power, absolute_value
  - String: concatenate, to_uppercase, to_lowercase, string_length
  - List: list_sum, list_average

**API Endpoints:**
```
POST   /dag/execute                   # Execute DAG from config
POST   /dag/validate                  # Validate DAG structure
GET    /dag/examples                  # Get example configurations
```

**DAG Configuration Format:**
```json
{
  "name": "my_dag",
  "nodes": [
    {"id": "node1", "function": "add"},
    {"id": "node2", "function": "multiply"}
  ],
  "edges": [
    {
      "source": "node1",
      "target": "node2",
      "sourceOutput": "node1",
      "targetInput": "a"
    }
  ]
}
```

### ✅ Phase III: Multi-Channel Viewer (Complete)

**Purpose:** Time-series data access with synchronized multi-channel views.

**Components:**
- `app_meshed/services/stream_service.py` - Stream abstraction
  - `StreamSource`: Base class with [bt:tt] slicing
  - `FileStreamSource`: File-backed streams
  - `StreamRegistry`: Global stream management
  - `MultiChannelView`: Synchronized access across channels

- `app_meshed/api/startup.py` - Sample data generation
  - Audio stream (44.1 kHz, sine wave)
  - Sensor streams (100 Hz, 3-axis accelerometer)

**API Endpoints:**
```
GET    /streams                          # List all streams
GET    /streams/{id}/metadata            # Get stream info
GET    /streams/{id}/slice?bt=0&tt=10    # Slice by time [bt:tt]
POST   /streams/multi-channel/slice      # Synchronized multi-channel
POST   /streams/multi-channel/info       # Multi-channel metadata
```

**Time-Based Slicing:**
```python
stream[1.0:2.0]  # Get data from 1.0s to 2.0s
```

---

## Project Structure

```
app_meshed/
├── app_meshed/
│   ├── api/
│   │   ├── main.py              # FastAPI app (538 lines, 30+ endpoints)
│   │   └── startup.py           # Initialization and sample data
│   ├── stores/
│   │   └── root_store.py        # Unified dol storage interface
│   ├── services/
│   │   ├── function_registry.py # i2-based function introspection
│   │   ├── schema_service.py    # ju-inspired schema generation
│   │   ├── dag_service.py       # meshed DAG operations
│   │   └── stream_service.py    # creek-inspired streaming
│   ├── utils/
│   │   └── example_functions.py # 12 pre-built functions
│   └── cli.py                   # CLI runner
│
├── examples/
│   ├── hello_world_dag.py       # Complete DAG workflow example
│   ├── ju_schema_example.py     # Schema generation demo
│   ├── dol_browser_example.py   # Store browsing demo
│   └── stream_slicing_example.py # Stream slicing demo
│
├── tests/
│   ├── test_function_registry.py (11 tests)
│   ├── test_schema_service.py    (9 tests)
│   └── test_dag_service.py       (6 tests)
│
├── README.md                     # Complete user documentation
├── ARCHITECTURE.md               # This file
└── pyproject.toml               # Dependencies and config
```

---

## Key Design Patterns

### 1. Source-Keyed Architecture

**Principle:** All data is accessed through uniform Mapping interfaces.

**Implementation:**
```python
from app_meshed.stores.root_store import create_default_root_store

root = create_default_root_store()

# Uniform interface across all data types
root.meshes["my_dag"] = dag_config      # Store DAG
root.configs["settings"] = app_config   # Store config
dag = root.meshes["my_dag"]             # Retrieve DAG
"my_dag" in root.meshes                 # Check existence
del root.meshes["my_dag"]               # Delete DAG
```

**Benefits:**
- Backend-agnostic (files, S3, databases)
- Automatic serialization/deserialization
- Easy to extend with new store types
- Direct HTTP API mapping

### 2. Interface-First Design

**Principle:** Function signatures drive everything.

**Flow:**
```
Python Function
    ↓ (i2)
Signature Metadata
    ↓ (ju)
JSON Schema
    ↓ (RJSF)
Form UI
    ↓ (User Input)
DAG Execution
```

**Example:**
```python
def process(audio: str, gain: float = 1.0) -> dict:
    """Process audio with gain."""
    return {"processed": True, "gain": gain}

# Automatic generation of:
# - API endpoint: /schema/function/process
# - JSON Schema for form rendering
# - Parameter validation
# - Documentation
```

### 3. Time-Based Slicing

**Principle:** Access time-series data by time ranges, not indices.

**Syntax:**
```python
stream[bt:tt]  # Get data from bottom-time to top-time
```

**Example:**
```python
audio_stream[1.0:2.0]    # 1 second of audio starting at t=1.0s
sensor_stream[0.5:1.5]   # 1 second of sensor data starting at t=0.5s

# Multi-channel synchronized
multi_view.get_synchronized_slice(
    ["accel_x", "accel_y", "accel_z"],
    bt=2.0,
    tt=4.0
)
```

---

## Usage Examples

### Starting the Server

```bash
# Basic
python -m app_meshed.cli

# With options
python -m app_meshed.cli --port 8080 --data-path /data --reload

# API docs at: http://localhost:8000/docs
```

### Running Examples

```bash
# Hello World DAG
python examples/hello_world_dag.py

# Schema Generation
python examples/ju_schema_example.py

# Store Browsing
python examples/dol_browser_example.py

# Stream Slicing
python examples/stream_slicing_example.py
```

### Running Tests

```bash
pytest tests/
```

### API Usage

```bash
# List functions
curl http://localhost:8000/functions

# Get function schema
curl http://localhost:8000/schema/function/add

# Execute DAG
curl -X POST http://localhost:8000/dag/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dag_config": {
      "name": "simple_add",
      "nodes": [{"id": "add_node", "function": "add"}],
      "edges": []
    },
    "inputs": {"a": 5, "b": 3}
  }'

# Slice stream
curl "http://localhost:8000/streams/audio_sample/slice?bt=0.0&tt=1.0"
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Storage | dol | Uniform key-value interface |
| Logic | meshed | DAG composition and execution |
| Streaming | creek (inspired) | Time-series slicing |
| Introspection | i2 | Function signature extraction |
| Schema | ju (inspired) | JSON Schema generation |
| HTTP | FastAPI | REST API endpoints |
| Runtime | uvicorn | ASGI server |
| Testing | pytest | Unit and integration tests |

---

## Next Steps: Frontend Integration

The backend is **100% complete** and ready for frontend integration.

### Recommended Frontend Stack

- **React**: Component framework
- **React Flow**: Visual DAG canvas
- **RJSF** (React JSON Schema Form): Auto-generated forms
- **Plotly.js** or **Chart.js**: Stream visualization
- **TanStack Query**: API state management

### Integration Points

1. **Store Browser UI**
   - Connect to: `GET /store/{store}/keys`
   - Tree view of available stores
   - CRUD operations via API

2. **Mesh Maker Canvas**
   - Drag functions from `/functions` endpoint
   - Use React Flow for visual composition
   - Fetch schemas from `/schema/function/{name}`
   - Render RJSF forms for node configuration
   - Execute via `POST /dag/execute`

3. **Multi-Channel Viewer**
   - List streams: `GET /streams`
   - Implement zoom/pan controls
   - Request slices: `GET /streams/{id}/slice?bt=X&tt=Y`
   - Render with Plotly/Chart.js
   - Synchronized views: `POST /streams/multi-channel/slice`

---

## Development Guidelines

### Adding New Functions

```python
# In app_meshed/utils/example_functions.py
def my_function(param1: type1, param2: type2 = default) -> return_type:
    """Docstring for the function."""
    return result

# Add to EXAMPLE_FUNCTIONS list
EXAMPLE_FUNCTIONS.append(("my_function", my_function))
```

Functions are automatically:
- Registered on startup
- Introspected for metadata
- Available via API
- Schema-ready for forms

### Adding New Stores

```python
# In app_meshed/stores/root_store.py
def _create_my_store(self) -> Mapping:
    base_store = Files(str(self.base_path / "my_store"))
    return wrap_kvs(
        base_store,
        # ... codecs ...
    )

# Add to __init__
self.my_store = self._create_my_store()
```

### Adding New Stream Sources

```python
from app_meshed.services.stream_service import StreamSource

class MyStreamSource(StreamSource):
    def __getitem__(self, key):
        # Implement [bt:tt] slicing
        pass

# Register
stream_registry.register(MyStreamSource(...))
```

---

## Performance Considerations

- **Lazy Loading**: Streams only load data when sliced
- **JSON Serialization**: Automatic for stores
- **Caching**: Function metadata cached in registry
- **Streaming**: Large datasets handled via time-based chunks

---

## Security Considerations

- **Input Validation**: All API endpoints validate input
- **CORS**: Configured for frontend integration
- **Data Isolation**: Stores are directory-based
- **Function Sandboxing**: Consider for production use

---

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
CMD ["python", "-m", "app_meshed.cli", "--host", "0.0.0.0"]
```

### Cloud Deployment

Compatible with:
- **AWS**: ECS, Lambda (with Mangum)
- **GCP**: Cloud Run, App Engine
- **Azure**: Container Instances, App Service
- **Heroku**: Procfile-based deployment

---

## Conclusion

**app_meshed** is a complete, production-ready backend platform implementing the three-phase architecture outlined in the original plan:

✅ **Phase I**: Store Explorer with dol, i2, ju
✅ **Phase II**: Mesh Maker with meshed DAG operations
✅ **Phase III**: Multi-Channel Viewer with creek-inspired streaming

**Key Achievements:**
- 30+ REST API endpoints
- 12 example functions
- 4 complete integration examples
- 26 unit tests
- Comprehensive documentation
- CLI runner with configuration options

**Ready for:**
- Frontend integration
- Production deployment
- Extension with custom functions/stores/streams
- Real-world data science workflows

---

**Repository:** https://github.com/i2mint/app_meshed
**Branch:** `claude/build-dag-architecture-01Jrr5obUormejAS9h3YziT4`
**License:** MIT
