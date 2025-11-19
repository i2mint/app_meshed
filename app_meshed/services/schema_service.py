"""Schema generation service using ju (JSON Schema utilities).

This module provides schema generation from:
- Function signatures (via i2 + ju)
- Python objects
- Custom types

Schemas are used to generate forms in the frontend (RJSF).
"""

from typing import Any, Callable, Dict, Optional, get_type_hints
import inspect

try:
    from i2 import Sig
except ImportError:
    raise ImportError("i2 is required. Install with: pip install i2")

try:
    import ju
except ImportError:
    # ju might not have a direct func_to_schema, we'll implement a fallback
    ju = None


class SchemaGenerator:
    """Generate JSON Schemas from various sources.

    This class uses ju and i2 to convert Python types, function signatures,
    and objects into JSON Schema format suitable for RJSF form generation.
    """

    @staticmethod
    def python_type_to_json_type(py_type: Any) -> str:
        """Convert Python type to JSON Schema type.

        Args:
            py_type: Python type annotation

        Returns:
            JSON Schema type string
        """
        type_mapping = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
            type(None): "null",
        }

        # Handle typing module types
        if hasattr(py_type, "__origin__"):
            origin = py_type.__origin__
            if origin in (list, List):
                return "array"
            elif origin in (dict, Dict):
                return "object"

        return type_mapping.get(py_type, "string")

    @staticmethod
    def get_default_value(param: inspect.Parameter) -> Optional[Any]:
        """Extract default value from parameter.

        Args:
            param: Function parameter

        Returns:
            Default value or None
        """
        if param.default != inspect.Parameter.empty:
            return param.default
        return None

    def function_to_schema(self, func: Callable, title: Optional[str] = None) -> Dict:
        """Generate JSON Schema from a function signature.

        Args:
            func: Function to generate schema for
            title: Optional title for the schema

        Returns:
            JSON Schema dict suitable for RJSF
        """
        sig = Sig(func)
        schema = {
            "type": "object",
            "title": title or func.__name__,
            "properties": {},
            "required": [],
        }

        # Add description from docstring
        if func.__doc__:
            schema["description"] = func.__doc__.strip()

        # Process each parameter
        for param_name in sig.names:
            param = sig.params[param_name]

            # Get type annotation
            param_type = "string"  # default
            if param.annotation != inspect.Parameter.empty:
                param_type = self.python_type_to_json_type(param.annotation)

            # Build property schema
            prop_schema = {"type": param_type}

            # Add default if available
            default = self.get_default_value(param)
            if default is not None:
                prop_schema["default"] = default
            else:
                # No default = required parameter
                schema["required"].append(param_name)

            # Add to properties
            schema["properties"][param_name] = prop_schema

        return schema

    def object_to_schema(self, obj: Any, title: Optional[str] = None) -> Dict:
        """Generate JSON Schema from a Python object.

        Args:
            obj: Object to generate schema for
            title: Optional title for the schema

        Returns:
            JSON Schema dict
        """
        if isinstance(obj, dict):
            return self._dict_to_schema(obj, title)
        elif isinstance(obj, list):
            return self._list_to_schema(obj, title)
        else:
            return self._value_to_schema(obj, title)

    def _dict_to_schema(self, obj: dict, title: Optional[str] = None) -> Dict:
        """Generate schema from a dictionary.

        Args:
            obj: Dictionary object
            title: Optional title

        Returns:
            JSON Schema dict
        """
        schema = {
            "type": "object",
            "title": title or "Object",
            "properties": {},
        }

        for key, value in obj.items():
            schema["properties"][key] = self._value_to_schema(value, key)

        return schema

    def _list_to_schema(self, obj: list, title: Optional[str] = None) -> Dict:
        """Generate schema from a list.

        Args:
            obj: List object
            title: Optional title

        Returns:
            JSON Schema dict
        """
        schema = {
            "type": "array",
            "title": title or "Array",
        }

        # Try to infer item schema from first element
        if obj:
            schema["items"] = self._value_to_schema(obj[0])

        return schema

    def _value_to_schema(self, value: Any, title: Optional[str] = None) -> Dict:
        """Generate schema from a single value.

        Args:
            value: Value to generate schema for
            title: Optional title

        Returns:
            JSON Schema dict
        """
        py_type = type(value)
        json_type = self.python_type_to_json_type(py_type)

        schema = {"type": json_type}
        if title:
            schema["title"] = title

        # For nested objects
        if isinstance(value, dict):
            return self._dict_to_schema(value, title)
        elif isinstance(value, list):
            return self._list_to_schema(value, title)

        return schema

    def dag_config_schema(self) -> Dict:
        """Generate schema for DAG configuration.

        Returns:
            JSON Schema for DAG configuration
        """
        return {
            "type": "object",
            "title": "DAG Configuration",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "DAG Name",
                    "description": "Name of the DAG",
                },
                "nodes": {
                    "type": "array",
                    "title": "Nodes",
                    "description": "Function nodes in the DAG",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "function": {"type": "string"},
                            "params": {"type": "object"},
                        },
                        "required": ["id", "function"],
                    },
                },
                "edges": {
                    "type": "array",
                    "title": "Edges",
                    "description": "Connections between nodes",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "target": {"type": "string"},
                            "sourceOutput": {"type": "string"},
                            "targetInput": {"type": "string"},
                        },
                        "required": ["source", "target"],
                    },
                },
            },
            "required": ["name", "nodes"],
        }


# Create a global schema generator instance
_schema_generator = SchemaGenerator()


def func_to_schema(func: Callable, title: Optional[str] = None) -> Dict:
    """Generate JSON Schema from a function.

    Args:
        func: Function to generate schema for
        title: Optional title

    Returns:
        JSON Schema dict
    """
    return _schema_generator.function_to_schema(func, title)


def object_to_schema(obj: Any, title: Optional[str] = None) -> Dict:
    """Generate JSON Schema from an object.

    Args:
        obj: Object to generate schema for
        title: Optional title

    Returns:
        JSON Schema dict
    """
    return _schema_generator.object_to_schema(obj, title)


def get_dag_config_schema() -> Dict:
    """Get the JSON Schema for DAG configuration.

    Returns:
        JSON Schema dict
    """
    return _schema_generator.dag_config_schema()
