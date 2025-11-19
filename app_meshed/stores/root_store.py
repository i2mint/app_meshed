"""Unified store interface using dol for source-keyed data access.

This module implements the Root Store pattern, providing a fanout interface
to different data sources:
- raw_data: Binary blobs (audio, sensor data, etc.)
- functions: Callable functions available for DAG composition
- meshes: Saved DAG configurations (JSON)
- configs: Application configurations
"""

from typing import Any, Mapping
from pathlib import Path
import json
import pickle
from functools import partial

try:
    from dol import Pipe, Store, wrap_kvs, filt_iter, cached_keys
    from dol.sources import Files
except ImportError:
    raise ImportError(
        "dol is required. Install with: pip install dol"
    )


class RootStore:
    """Root store that provides access to all sub-stores.

    This implements a fanout pattern where different data types are accessed
    through dedicated sub-stores, all unified under a single interface.

    Example:
        >>> root = RootStore(base_path="/data")
        >>> root.raw_data["audio_001.wav"]  # Access raw data
        >>> root.functions["process_audio"]  # Access functions
        >>> root.meshes["my_dag"]  # Access saved DAGs
    """

    def __init__(self, base_path: str = "./data"):
        """Initialize the root store with sub-stores.

        Args:
            base_path: Base directory for storing data
        """
        self.base_path = Path(base_path)
        self._ensure_directories()

        # Initialize sub-stores
        self.raw_data = self._create_raw_data_store()
        self.functions = self._create_functions_store()
        self.meshes = self._create_meshes_store()
        self.configs = self._create_configs_store()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for subdir in ["raw_data", "functions", "meshes", "configs"]:
            (self.base_path / subdir).mkdir(parents=True, exist_ok=True)

    def _create_raw_data_store(self) -> Mapping:
        """Create a store for raw binary data (audio, sensors, etc.).

        Returns:
            A dol store for raw data files
        """
        return Files(str(self.base_path / "raw_data"))

    def _create_functions_store(self) -> Mapping:
        """Create a store for Python functions.

        Functions are stored as pickled objects. For production use,
        consider using dill or cloudpickle for better serialization.

        Returns:
            A dol store for functions with pickle codec
        """
        base_store = Files(str(self.base_path / "functions"))

        # Wrap with pickle codec for Python object serialization
        return wrap_kvs(
            base_store,
            key_of_id=lambda k: k if k.endswith('.pkl') else f"{k}.pkl",
            id_of_key=lambda k: k.replace('.pkl', ''),
            obj_of_data=pickle.loads,
            data_of_obj=pickle.dumps,
        )

    def _create_meshes_store(self) -> Mapping:
        """Create a store for DAG configurations (meshes).

        Meshes are stored as JSON files containing DAG definitions.

        Returns:
            A dol store for mesh configurations with JSON codec
        """
        base_store = Files(str(self.base_path / "meshes"))

        # Wrap with JSON codec
        return wrap_kvs(
            base_store,
            key_of_id=lambda k: k if k.endswith('.json') else f"{k}.json",
            id_of_key=lambda k: k.replace('.json', ''),
            obj_of_data=lambda data: json.loads(data.decode() if isinstance(data, bytes) else data),
            data_of_obj=lambda obj: json.dumps(obj, indent=2).encode(),
        )

    def _create_configs_store(self) -> Mapping:
        """Create a store for application configurations.

        Returns:
            A dol store for configs with JSON codec
        """
        base_store = Files(str(self.base_path / "configs"))

        return wrap_kvs(
            base_store,
            key_of_id=lambda k: k if k.endswith('.json') else f"{k}.json",
            id_of_key=lambda k: k.replace('.json', ''),
            obj_of_data=lambda data: json.loads(data.decode() if isinstance(data, bytes) else data),
            data_of_obj=lambda obj: json.dumps(obj, indent=2).encode(),
        )

    def list_all_keys(self) -> dict[str, list[str]]:
        """List all keys across all sub-stores.

        Returns:
            Dictionary mapping store names to lists of keys
        """
        return {
            "raw_data": list(self.raw_data.keys()),
            "functions": list(self.functions.keys()),
            "meshes": list(self.meshes.keys()),
            "configs": list(self.configs.keys()),
        }

    def get_store(self, store_name: str) -> Mapping:
        """Get a specific sub-store by name.

        Args:
            store_name: Name of the store (raw_data, functions, meshes, configs)

        Returns:
            The requested store

        Raises:
            ValueError: If store_name is not valid
        """
        if not hasattr(self, store_name):
            raise ValueError(
                f"Unknown store: {store_name}. "
                f"Available stores: raw_data, functions, meshes, configs"
            )
        return getattr(self, store_name)


def create_default_root_store(base_path: str = "./data") -> RootStore:
    """Factory function to create a default root store.

    Args:
        base_path: Base directory for storing data

    Returns:
        Configured RootStore instance
    """
    return RootStore(base_path=base_path)
