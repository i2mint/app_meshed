"""Example demonstrating dol-based store browsing.

This example shows how the unified root store provides a flat,
key-value interface to different types of data storage.
"""

import json
import tempfile
from pathlib import Path

from app_meshed.stores.root_store import create_default_root_store


def main():
    """Run the dol browser example."""
    print("=" * 70)
    print("DOL Store Browser Example")
    print("=" * 70)
    print()

    # Create a temporary directory for this example
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Using temporary directory: {tmpdir}")
        print()

        # Create the root store
        root = create_default_root_store(base_path=tmpdir)

        # Example 1: Storing and retrieving DAG configurations
        print("Example 1: DAG Configuration Storage (meshes store)")
        print("-" * 70)
        print()

        dag_config = {
            "name": "example_dag",
            "nodes": [
                {"id": "node1", "function": "add"},
                {"id": "node2", "function": "multiply"},
            ],
            "edges": [
                {
                    "source": "node1",
                    "target": "node2",
                    "sourceOutput": "node1",
                    "targetInput": "a",
                }
            ],
        }

        # Store the DAG (automatic JSON serialization)
        root.meshes["my_first_dag"] = dag_config
        print("✓ Stored DAG configuration: 'my_first_dag'")
        print()

        # Retrieve it
        retrieved = root.meshes["my_first_dag"]
        print("Retrieved DAG:")
        print(json.dumps(retrieved, indent=2))
        print()

        # List all meshes
        print(f"All meshes in store: {list(root.meshes.keys())}")
        print()

        # Example 2: Application configurations
        print("=" * 70)
        print("Example 2: Application Configuration (configs store)")
        print("-" * 70)
        print()

        app_config = {
            "server": {"host": "0.0.0.0", "port": 8000},
            "data_path": "/data",
            "features": {
                "enable_streaming": True,
                "max_upload_size": 104857600,  # 100MB
            },
        }

        root.configs["app_settings"] = app_config
        print("✓ Stored configuration: 'app_settings'")
        print()

        # Retrieve and display
        settings = root.configs["app_settings"]
        print("Retrieved settings:")
        print(json.dumps(settings, indent=2))
        print()

        # Example 3: Working with multiple items
        print("=" * 70)
        print("Example 3: Bulk Operations")
        print("-" * 70)
        print()

        # Store multiple DAGs
        dags = {
            "simple_add": {
                "name": "simple_add",
                "nodes": [{"id": "add", "function": "add"}],
                "edges": [],
            },
            "simple_multiply": {
                "name": "simple_multiply",
                "nodes": [{"id": "mul", "function": "multiply"}],
                "edges": [],
            },
            "chained": {
                "name": "chained",
                "nodes": [
                    {"id": "step1", "function": "add"},
                    {"id": "step2", "function": "multiply"},
                ],
                "edges": [
                    {
                        "source": "step1",
                        "target": "step2",
                        "sourceOutput": "step1",
                        "targetInput": "a",
                    }
                ],
            },
        }

        for name, config in dags.items():
            root.meshes[name] = config
            print(f"✓ Stored DAG: '{name}'")

        print()
        print(f"Total DAGs in store: {len(list(root.meshes.keys()))}")
        print(f"DAG names: {list(root.meshes.keys())}")
        print()

        # Example 4: Store statistics
        print("=" * 70)
        print("Example 4: Store Statistics")
        print("-" * 70)
        print()

        all_keys = root.list_all_keys()
        print("Items in each store:")
        for store_name, keys in all_keys.items():
            print(f"  {store_name}: {len(keys)} items")
            if keys:
                print(f"    Keys: {keys}")
        print()

        # Example 5: Source-keyed architecture in action
        print("=" * 70)
        print("Example 5: Source-Keyed Architecture")
        print("-" * 70)
        print()

        print("Key insight: All stores use the same dict-like interface!")
        print()
        print("Code examples:")
        print("  root.meshes['my_dag'] = {...}         # Store a DAG")
        print("  root.configs['settings'] = {...}      # Store config")
        print("  dag = root.meshes['my_dag']           # Retrieve DAG")
        print("  'my_dag' in root.meshes               # Check existence")
        print("  del root.meshes['my_dag']             # Delete DAG")
        print("  list(root.meshes.keys())              # List all keys")
        print()

        # Demonstrate the interface
        print("Live demonstration:")
        print(f"  'simple_add' in root.meshes -> {('simple_add' in root.meshes)}")
        print(f"  'nonexistent' in root.meshes -> {('nonexistent' in root.meshes)}")
        print()

        # Example 6: How this maps to HTTP API
        print("=" * 70)
        print("Example 6: HTTP API Mapping")
        print("-" * 70)
        print()

        print("Python code -> HTTP API:")
        print()
        print("  root.meshes['my_dag'] = config")
        print("  ↓")
        print("  PUT /store/meshes/my_dag")
        print("  Body: config (JSON)")
        print()
        print("  dag = root.meshes['my_dag']")
        print("  ↓")
        print("  GET /store/meshes/my_dag")
        print()
        print("  list(root.meshes.keys())")
        print("  ↓")
        print("  GET /store/meshes/keys")
        print()
        print("  del root.meshes['my_dag']")
        print("  ↓")
        print("  DELETE /store/meshes/my_dag")
        print()

        print("=" * 70)
        print("DOL Browser Example Complete!")
        print("=" * 70)
        print()
        print("Key Benefits of dol:")
        print("  ✓ Uniform interface: Everything is a Mapping")
        print("  ✓ Automatic serialization: JSON, pickle, etc.")
        print("  ✓ Backend agnostic: Files, S3, databases, etc.")
        print("  ✓ Easy to extend: Add new stores as needed")
        print("  ✓ API-ready: Direct mapping to HTTP endpoints")
        print()


if __name__ == "__main__":
    main()
