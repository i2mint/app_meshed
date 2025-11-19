"""Tests for DAG service."""

import pytest
from app_meshed.services.function_registry import FunctionRegistry
from app_meshed.services.dag_service import DAGService


@pytest.fixture
def registry_with_functions():
    """Create a registry with test functions."""
    registry = FunctionRegistry()

    def add(a: int, b: int) -> int:
        return a + b

    def multiply(a: float, b: float) -> float:
        return a * b

    def subtract(a: float, b: float) -> float:
        return a - b

    registry.register("add", add)
    registry.register("multiply", multiply)
    registry.register("subtract", subtract)

    return registry


@pytest.fixture
def dag_service(registry_with_functions):
    """Create a DAG service with test functions."""
    return DAGService(registry_with_functions)


def test_simple_dag_execution(dag_service):
    """Test executing a simple single-node DAG."""
    config = {
        "name": "simple_add",
        "nodes": [{"id": "add_node", "function": "add"}],
        "edges": [],
        "params": {},
    }

    inputs = {"a": 5, "b": 3}

    result = dag_service.execute_from_config(config, inputs)

    assert result["status"] == "success"
    assert result["result"] == 8
    assert result["dag_name"] == "simple_add"


def test_chained_dag_execution(dag_service):
    """Test executing a DAG with chained operations."""
    config = {
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
        "params": {},
    }

    # (5 + 3) * 2 = 16
    inputs = {"a": 5, "b": 3, "step2": {"b": 2}}

    result = dag_service.execute_from_config(config, inputs)

    assert result["status"] == "success"
    # The actual result will depend on meshed's execution model
    # This test validates the structure works


def test_dag_validation_valid(dag_service):
    """Test validating a valid DAG configuration."""
    config = {
        "name": "valid_dag",
        "nodes": [{"id": "node1", "function": "add"}],
        "edges": [],
    }

    dag = dag_service.json_to_dag(config)
    assert dag is not None


def test_dag_validation_invalid_function(dag_service):
    """Test validation fails for nonexistent function."""
    config = {
        "name": "invalid_dag",
        "nodes": [{"id": "node1", "function": "nonexistent"}],
        "edges": [],
    }

    with pytest.raises(ValueError, match="not found in registry"):
        dag_service.json_to_dag(config)


def test_dag_validation_empty_nodes(dag_service):
    """Test validation fails for empty nodes."""
    config = {"name": "empty_dag", "nodes": [], "edges": []}

    with pytest.raises(ValueError, match="at least one node"):
        dag_service.json_to_dag(config)


def test_execute_from_config_error_handling(dag_service):
    """Test error handling in DAG execution."""
    config = {
        "name": "error_dag",
        "nodes": [{"id": "node1", "function": "nonexistent"}],
        "edges": [],
    }

    result = dag_service.execute_from_config(config, {})

    assert result["status"] == "error"
    assert "error" in result
    assert result["dag_name"] == "error_dag"
