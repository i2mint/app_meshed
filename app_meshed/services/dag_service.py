"""DAG service for meshed operations.

This module provides:
- DAG serialization/deserialization (JSON <-> meshed.DAG)
- DAG construction from JSON configurations
- DAG execution
"""

from typing import Any, Dict, List, Optional, Callable
import json

try:
    from meshed import DAG
    from meshed.makers import code_to_dag
except ImportError:
    raise ImportError("meshed is required. Install with: pip install meshed")

from app_meshed.services.function_registry import FunctionRegistry


class DAGService:
    """Service for managing and executing meshed DAGs.

    This service handles:
    - Converting JSON configs to live DAG objects
    - Executing DAGs with provided inputs
    - Serializing DAG definitions
    """

    def __init__(self, function_registry: FunctionRegistry):
        """Initialize the DAG service.

        Args:
            function_registry: Registry of available functions
        """
        self.function_registry = function_registry

    def json_to_dag(self, dag_config: Dict) -> DAG:
        """Convert a JSON configuration to a meshed.DAG object.

        Args:
            dag_config: Dictionary with DAG configuration
                {
                    "name": "my_dag",
                    "nodes": [
                        {
                            "id": "node1",
                            "function": "add",
                            "output_name": "sum"
                        },
                        ...
                    ],
                    "edges": [
                        {
                            "source": "node1",
                            "target": "node2",
                            "sourceOutput": "sum",
                            "targetInput": "a"
                        },
                        ...
                    ],
                    "params": {
                        "node1": {"a": 5, "b": 3}
                    }
                }

        Returns:
            Constructed DAG object

        Raises:
            ValueError: If configuration is invalid
        """
        name = dag_config.get("name", "unnamed_dag")
        nodes = dag_config.get("nodes", [])
        edges = dag_config.get("edges", [])
        params = dag_config.get("params", {})

        if not nodes:
            raise ValueError("DAG must have at least one node")

        # Build function map
        funcs = {}
        for node in nodes:
            node_id = node["id"]
            func_name = node["function"]

            try:
                func = self.function_registry.get_function(func_name)
                funcs[node_id] = func
            except KeyError:
                raise ValueError(
                    f"Function '{func_name}' not found in registry for node '{node_id}'"
                )

        # Build bindings from edges
        # Format: {target_node: {target_param: source_node}}
        binds = {}
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            target_input = edge.get("targetInput", edge.get("sourceOutput", "value"))

            if target not in binds:
                binds[target] = {}

            binds[target][target_input] = source

        # Create the DAG
        try:
            dag = DAG(funcs, **binds)
            return dag
        except Exception as e:
            raise ValueError(f"Error creating DAG: {str(e)}")

    def dag_to_json(self, dag: DAG) -> Dict:
        """Convert a DAG object to JSON configuration.

        Args:
            dag: DAG object

        Returns:
            JSON-serializable dictionary

        Note:
            This is a simplified serialization. Full serialization
            would require introspecting the DAG structure.
        """
        # This is challenging without direct DAG introspection
        # For now, return a placeholder structure
        return {
            "name": "exported_dag",
            "nodes": [],
            "edges": [],
            "note": "Full DAG serialization requires DAG introspection",
        }

    def execute_dag(self, dag: DAG, inputs: Dict[str, Any]) -> Any:
        """Execute a DAG with given inputs.

        Args:
            dag: DAG to execute
            inputs: Dictionary of input values

        Returns:
            DAG execution result
        """
        try:
            result = dag(**inputs)
            return result
        except Exception as e:
            raise RuntimeError(f"DAG execution failed: {str(e)}")

    def execute_from_config(
        self, dag_config: Dict, inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a DAG from JSON configuration.

        Args:
            dag_config: DAG configuration
            inputs: Input values for execution

        Returns:
            Dictionary with execution result and metadata
        """
        try:
            dag = self.json_to_dag(dag_config)
            result = self.execute_dag(dag, inputs)

            return {
                "status": "success",
                "result": result,
                "dag_name": dag_config.get("name", "unnamed"),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "dag_name": dag_config.get("name", "unnamed"),
            }


def create_simple_dag_example() -> Dict:
    """Create a simple DAG configuration example.

    Returns:
        Example DAG configuration
    """
    return {
        "name": "simple_add_dag",
        "nodes": [
            {
                "id": "add_node",
                "function": "add",
                "output_name": "result",
            }
        ],
        "edges": [],
        "params": {},
    }


def create_chained_dag_example() -> Dict:
    """Create a chained DAG configuration example.

    This creates a DAG that:
    1. Adds two numbers (a + b)
    2. Multiplies the result by c

    Returns:
        Example DAG configuration
    """
    return {
        "name": "chained_operations",
        "nodes": [
            {"id": "add_step", "function": "add", "output_name": "sum"},
            {"id": "multiply_step", "function": "multiply", "output_name": "product"},
        ],
        "edges": [
            {
                "source": "add_step",
                "target": "multiply_step",
                "sourceOutput": "sum",
                "targetInput": "a",
            }
        ],
        "params": {},
    }
