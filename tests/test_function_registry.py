"""Tests for function registry service."""

import pytest
from app_meshed.services.function_registry import FunctionRegistry


def test_register_function():
    """Test registering a function."""
    registry = FunctionRegistry()

    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    registry.register("add", add)
    assert "add" in registry.list_functions()


def test_get_function():
    """Test retrieving a registered function."""
    registry = FunctionRegistry()

    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    registry.register("multiply", multiply)
    func = registry.get_function("multiply")

    assert func(3.0, 4.0) == 12.0


def test_get_metadata():
    """Test extracting function metadata."""
    registry = FunctionRegistry()

    def process(data: str, mode: int = 1) -> dict:
        """Process data with mode."""
        return {"data": data, "mode": mode}

    registry.register("process", process)
    metadata = registry.get_metadata("process")

    assert metadata.name == "process"
    assert len(metadata.parameters) == 2

    # Check first parameter
    param1 = metadata.parameters[0]
    assert param1.name == "data"
    assert param1.annotation == "str"
    assert not param1.has_default

    # Check second parameter
    param2 = metadata.parameters[1]
    assert param2.name == "mode"
    assert param2.annotation == "int"
    assert param2.has_default
    assert param2.default == 1


def test_unregister_function():
    """Test unregistering a function."""
    registry = FunctionRegistry()

    def temp_func():
        pass

    registry.register("temp", temp_func)
    assert "temp" in registry.list_functions()

    registry.unregister("temp")
    assert "temp" not in registry.list_functions()


def test_override_function():
    """Test overriding an existing function."""
    registry = FunctionRegistry()

    def func_v1():
        return 1

    def func_v2():
        return 2

    registry.register("func", func_v1)
    assert registry.get_function("func")() == 1

    registry.register("func", func_v2, override=True)
    assert registry.get_function("func")() == 2


def test_register_duplicate_without_override_raises():
    """Test that registering duplicate without override raises error."""
    registry = FunctionRegistry()

    def func():
        pass

    registry.register("func", func)

    with pytest.raises(ValueError, match="already registered"):
        registry.register("func", func, override=False)


def test_get_nonexistent_function_raises():
    """Test that getting a nonexistent function raises error."""
    registry = FunctionRegistry()

    with pytest.raises(KeyError, match="not found"):
        registry.get_function("nonexistent")


def test_get_all_metadata():
    """Test getting metadata for all functions."""
    registry = FunctionRegistry()

    def func1(a: int) -> int:
        """Function 1."""
        return a

    def func2(b: str) -> str:
        """Function 2."""
        return b

    registry.register("func1", func1)
    registry.register("func2", func2)

    all_meta = registry.get_all_metadata()

    assert len(all_meta) == 2
    assert "func1" in all_meta
    assert "func2" in all_meta
    assert all_meta["func1"]["name"] == "func1"
    assert all_meta["func2"]["name"] == "func2"
