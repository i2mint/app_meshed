"""Main FastAPI application for app_meshed.

This module provides the HTTP API for:
- Store browsing and CRUD operations
- Function introspection and schema generation
- DAG composition and execution
- Stream visualization
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional
from pathlib import Path
import os

from app_meshed.stores.root_store import create_default_root_store
from app_meshed.services.function_registry import get_global_registry
from app_meshed.services.schema_service import func_to_schema, object_to_schema, get_dag_config_schema
from app_meshed.services.dag_service import DAGService
from app_meshed.services.stream_service import get_stream_registry, MultiChannelView

# Create FastAPI app
app = FastAPI(
    title="app_meshed",
    description="HTTP services for meshed operations",
    version="0.0.1",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize stores
DATA_PATH = os.getenv("APP_MESHED_DATA_PATH", "./data")
root_store = create_default_root_store(base_path=DATA_PATH)

# Get function registry
function_registry = get_global_registry()

# Initialize DAG service
dag_service = DAGService(function_registry)

# Initialize stream service
stream_registry = get_stream_registry()
multi_channel_view = MultiChannelView(stream_registry)


# Startup event handler
@app.on_event("startup")
async def startup_event():
    """Run initialization tasks on server startup."""
    from app_meshed.api.startup import run_startup_initialization
    run_startup_initialization(data_path=DATA_PATH)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "app_meshed",
        "version": "0.0.1",
        "description": "HTTP services for meshed operations",
        "endpoints": {
            "store": "/store/{store_name}",
            "functions": "/functions",
            "schema": "/schema/{function_name}",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# Store API Endpoints
# ============================================================================


@app.get("/store/list")
async def list_stores():
    """List all available stores."""
    return {
        "stores": ["raw_data", "functions", "meshes", "configs"],
        "description": {
            "raw_data": "Binary blobs (audio, sensor data)",
            "functions": "Callable functions for DAG composition",
            "meshes": "Saved DAG configurations",
            "configs": "Application configurations",
        },
    }


@app.get("/store/{store_name}/keys")
async def list_store_keys(store_name: str):
    """List all keys in a specific store.

    Args:
        store_name: Name of the store (raw_data, functions, meshes, configs)

    Returns:
        List of keys in the store
    """
    try:
        store = root_store.get_store(store_name)
        keys = list(store.keys())
        return {"store": store_name, "keys": keys, "count": len(keys)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing keys: {str(e)}")


@app.get("/store/{store_name}/{key:path}")
async def get_store_item(store_name: str, key: str):
    """Get an item from a store.

    Args:
        store_name: Name of the store
        key: Key of the item to retrieve

    Returns:
        The requested item
    """
    try:
        store = root_store.get_store(store_name)

        if key not in store:
            raise HTTPException(
                status_code=404, detail=f"Key '{key}' not found in store '{store_name}'"
            )

        item = store[key]

        # For raw_data, return metadata instead of binary content
        if store_name == "raw_data":
            file_path = Path(DATA_PATH) / store_name / key
            return {
                "key": key,
                "size": file_path.stat().st_size,
                "type": "binary",
                "path": str(file_path),
            }

        return {"key": key, "value": item}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving item: {str(e)}")


@app.put("/store/{store_name}/{key:path}")
async def put_store_item(store_name: str, key: str, value: Any = Body(...)):
    """Store an item in a store.

    Args:
        store_name: Name of the store
        key: Key to store the item under
        value: Value to store

    Returns:
        Confirmation message
    """
    try:
        store = root_store.get_store(store_name)

        # Don't allow storing to raw_data via this endpoint (use file upload instead)
        if store_name == "raw_data":
            raise HTTPException(
                status_code=400,
                detail="Use /upload endpoint for raw_data files",
            )

        store[key] = value
        return {"status": "success", "store": store_name, "key": key}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing item: {str(e)}")


@app.delete("/store/{store_name}/{key:path}")
async def delete_store_item(store_name: str, key: str):
    """Delete an item from a store.

    Args:
        store_name: Name of the store
        key: Key of the item to delete

    Returns:
        Confirmation message
    """
    try:
        store = root_store.get_store(store_name)

        if key not in store:
            raise HTTPException(
                status_code=404, detail=f"Key '{key}' not found in store '{store_name}'"
            )

        del store[key]
        return {"status": "success", "store": store_name, "key": key, "action": "deleted"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")


# ============================================================================
# Function Registry API Endpoints
# ============================================================================


@app.get("/functions")
async def list_functions():
    """List all registered functions.

    Returns:
        List of function names and their metadata
    """
    try:
        return {
            "functions": function_registry.list_functions(),
            "metadata": function_registry.get_all_metadata(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing functions: {str(e)}")


@app.get("/functions/{function_name}/metadata")
async def get_function_metadata(function_name: str):
    """Get metadata for a specific function.

    Args:
        function_name: Name of the function

    Returns:
        Function metadata including parameters, types, and documentation
    """
    try:
        metadata = function_registry.get_metadata(function_name)
        return metadata.to_dict()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving function metadata: {str(e)}"
        )


# ============================================================================
# Utility Endpoints
# ============================================================================


@app.get("/stats")
async def get_stats():
    """Get statistics about the application state.

    Returns:
        Statistics about stores and functions
    """
    try:
        all_keys = root_store.list_all_keys()
        return {
            "stores": {
                name: {"count": len(keys), "keys": keys}
                for name, keys in all_keys.items()
            },
            "functions": {
                "count": len(function_registry.list_functions()),
                "names": function_registry.list_functions(),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")


# ============================================================================
# Schema API Endpoints (for RJSF form generation)
# ============================================================================


@app.get("/schema/function/{function_name}")
async def get_function_schema(function_name: str):
    """Get JSON Schema for a function (for RJSF forms).

    Args:
        function_name: Name of the function

    Returns:
        JSON Schema for the function's parameters
    """
    try:
        func = function_registry.get_function(function_name)
        schema = func_to_schema(func, title=f"{function_name} Parameters")
        return schema
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating schema: {str(e)}"
        )


@app.post("/schema/object")
async def get_object_schema(obj: Any = Body(...), title: Optional[str] = None):
    """Get JSON Schema for an object.

    Args:
        obj: Object to generate schema for
        title: Optional title for the schema

    Returns:
        JSON Schema for the object
    """
    try:
        schema = object_to_schema(obj, title=title)
        return schema
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating schema: {str(e)}"
        )


@app.get("/schema/dag-config")
async def get_dag_schema():
    """Get JSON Schema for DAG configuration.

    Returns:
        JSON Schema for DAG configuration
    """
    return get_dag_config_schema()


# ============================================================================
# DAG API Endpoints
# ============================================================================


@app.post("/dag/execute")
async def execute_dag(dag_config: Dict = Body(...), inputs: Dict[str, Any] = Body({})):
    """Execute a DAG from JSON configuration.

    Args:
        dag_config: DAG configuration (nodes, edges, params)
        inputs: Input values for execution

    Returns:
        Execution result
    """
    try:
        result = dag_service.execute_from_config(dag_config, inputs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DAG execution error: {str(e)}")


@app.post("/dag/validate")
async def validate_dag(dag_config: Dict = Body(...)):
    """Validate a DAG configuration without executing it.

    Args:
        dag_config: DAG configuration to validate

    Returns:
        Validation result
    """
    try:
        dag = dag_service.json_to_dag(dag_config)
        return {
            "status": "valid",
            "dag_name": dag_config.get("name", "unnamed"),
            "message": "DAG configuration is valid",
        }
    except Exception as e:
        return {
            "status": "invalid",
            "error": str(e),
            "dag_name": dag_config.get("name", "unnamed"),
        }


@app.get("/dag/examples")
async def get_dag_examples():
    """Get example DAG configurations.

    Returns:
        List of example DAG configurations
    """
    from app_meshed.services.dag_service import (
        create_simple_dag_example,
        create_chained_dag_example,
    )

    return {
        "examples": [
            {
                "name": "Simple Add",
                "description": "Single node DAG that adds two numbers",
                "config": create_simple_dag_example(),
            },
            {
                "name": "Chained Operations",
                "description": "Multi-node DAG with chained operations",
                "config": create_chained_dag_example(),
            },
        ]
    }


# ============================================================================
# Stream API Endpoints (Phase III)
# ============================================================================


@app.get("/streams")
async def list_streams():
    """List all registered streams.

    Returns:
        List of stream IDs and their metadata
    """
    try:
        return {
            "streams": stream_registry.list_streams(),
            "metadata": stream_registry.get_all_metadata(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing streams: {str(e)}")


@app.get("/streams/{source_id}/metadata")
async def get_stream_metadata(source_id: str):
    """Get metadata for a specific stream.

    Args:
        source_id: Stream identifier

    Returns:
        Stream metadata
    """
    try:
        stream = stream_registry.get(source_id)
        return stream.get_metadata()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving stream metadata: {str(e)}"
        )


@app.get("/streams/{source_id}/slice")
async def slice_stream(source_id: str, bt: float = 0.0, tt: Optional[float] = None):
    """Slice a stream by time range [bt:tt].

    Args:
        source_id: Stream identifier
        bt: Bottom time (start) in seconds
        tt: Top time (end) in seconds (None = end of stream)

    Returns:
        Sliced stream data
    """
    try:
        stream = stream_registry.get(source_id)

        # Get stream length if tt not specified
        if tt is None:
            metadata = stream.get_metadata()
            tt = metadata.get("length_seconds", 10.0)

        result = stream_registry.slice_stream(source_id, bt, tt)
        return result
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error slicing stream: {str(e)}")


@app.post("/streams/multi-channel/slice")
async def slice_multi_channel(
    channel_ids: List[str] = Body(...),
    bt: float = Body(0.0),
    tt: float = Body(10.0),
):
    """Get synchronized slices from multiple channels.

    Args:
        channel_ids: List of stream/channel IDs
        bt: Bottom time (start) in seconds
        tt: Top time (end) in seconds

    Returns:
        Synchronized multi-channel data
    """
    try:
        result = multi_channel_view.get_synchronized_slice(channel_ids, bt, tt)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error slicing multi-channel data: {str(e)}"
        )


@app.post("/streams/multi-channel/info")
async def get_multi_channel_info(channel_ids: List[str] = Body(...)):
    """Get metadata for multiple channels.

    Args:
        channel_ids: List of channel IDs

    Returns:
        Metadata for each channel
    """
    try:
        result = multi_channel_view.get_channel_info(channel_ids)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving channel info: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
