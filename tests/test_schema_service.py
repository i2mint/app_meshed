"""Tests for schema generation service."""

import pytest
from app_meshed.services.schema_service import func_to_schema, object_to_schema


def test_func_to_schema_basic():
    """Test generating schema from a basic function."""

    def simple(a: int, b: str) -> dict:
        """A simple function."""
        return {}

    schema = func_to_schema(simple)

    assert schema["type"] == "object"
    assert "properties" in schema
    assert "a" in schema["properties"]
    assert "b" in schema["properties"]
    assert schema["properties"]["a"]["type"] == "integer"
    assert schema["properties"]["b"]["type"] == "string"


def test_func_to_schema_with_defaults():
    """Test schema generation with default parameters."""

    def with_defaults(a: int, b: str = "default", c: float = 1.0) -> None:
        """Function with defaults."""
        pass

    schema = func_to_schema(with_defaults)

    # 'a' is required (no default)
    assert "a" in schema["required"]

    # 'b' and 'c' have defaults
    assert "b" not in schema["required"]
    assert "c" not in schema["required"]
    assert schema["properties"]["b"]["default"] == "default"
    assert schema["properties"]["c"]["default"] == 1.0


def test_func_to_schema_with_title():
    """Test schema generation with custom title."""

    def my_func():
        pass

    schema = func_to_schema(my_func, title="Custom Title")

    assert schema["title"] == "Custom Title"


def test_func_to_schema_with_docstring():
    """Test that docstring is included in schema."""

    def documented(x: int) -> int:
        """This is a documented function."""
        return x

    schema = func_to_schema(documented)

    assert "description" in schema
    assert schema["description"] == "This is a documented function."


def test_object_to_schema_dict():
    """Test generating schema from a dictionary."""
    obj = {
        "name": "test",
        "count": 42,
        "active": True,
    }

    schema = object_to_schema(obj)

    assert schema["type"] == "object"
    assert "properties" in schema
    assert "name" in schema["properties"]
    assert "count" in schema["properties"]
    assert "active" in schema["properties"]


def test_object_to_schema_list():
    """Test generating schema from a list."""
    obj = [1, 2, 3]

    schema = object_to_schema(obj)

    assert schema["type"] == "array"
    assert "items" in schema


def test_object_to_schema_nested():
    """Test generating schema from nested objects."""
    obj = {
        "user": {
            "name": "Alice",
            "age": 30,
        },
        "settings": {
            "theme": "dark",
            "notifications": True,
        },
    }

    schema = object_to_schema(obj)

    assert schema["type"] == "object"
    assert "user" in schema["properties"]
    assert "settings" in schema["properties"]
    assert schema["properties"]["user"]["type"] == "object"
    assert schema["properties"]["settings"]["type"] == "object"


def test_python_type_to_json_type():
    """Test type conversions."""
    from app_meshed.services.schema_service import SchemaGenerator

    generator = SchemaGenerator()

    assert generator.python_type_to_json_type(int) == "integer"
    assert generator.python_type_to_json_type(float) == "number"
    assert generator.python_type_to_json_type(str) == "string"
    assert generator.python_type_to_json_type(bool) == "boolean"
    assert generator.python_type_to_json_type(list) == "array"
    assert generator.python_type_to_json_type(dict) == "object"
