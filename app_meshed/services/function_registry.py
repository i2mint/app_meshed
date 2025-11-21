"""Function registry with i2 signature introspection.

This module provides a registry for functions that will be used in DAG composition.
It uses i2 to ensure clean, inspectable signatures and provides metadata about
each function's parameters, types, and documentation.
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, asdict
import inspect

try:
    from i2 import Sig
except ImportError:
    raise ImportError(
        "i2 is required for function introspection. Install with: pip install i2"
    )


@dataclass
class ParameterInfo:
    """Information about a function parameter."""
    name: str
    annotation: str
    default: Optional[Any] = None
    has_default: bool = False
    kind: str = "POSITIONAL_OR_KEYWORD"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "annotation": self.annotation,
            "default": repr(self.default) if self.has_default else None,
            "has_default": self.has_default,
            "kind": self.kind,
        }


@dataclass
class FunctionMetadata:
    """Metadata about a registered function."""
    name: str
    doc: Optional[str]
    parameters: List[ParameterInfo]
    return_annotation: str
    module: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "doc": self.doc,
            "parameters": [p.to_dict() for p in self.parameters],
            "return_annotation": self.return_annotation,
            "module": self.module,
        }


class FunctionRegistry:
    """Registry for functions with i2 signature introspection.

    This registry maintains a collection of functions that can be used
    in DAG composition. It uses i2.Sig to extract and normalize function
    signatures, making them inspectable and usable for form generation.

    Example:
        >>> registry = FunctionRegistry()
        >>> def add(a: int, b: int) -> int:
        ...     return a + b
        >>> registry.register("add", add)
        >>> metadata = registry.get_metadata("add")
        >>> print(metadata.parameters)
    """

    def __init__(self):
        """Initialize the function registry."""
        self._functions: Dict[str, Callable] = {}
        self._metadata: Dict[str, FunctionMetadata] = {}

    def register(self, name: str, func: Callable, *, override: bool = False) -> None:
        """Register a function in the registry.

        Args:
            name: Name to register the function under
            func: The callable to register
            override: If True, allow overriding existing registrations

        Raises:
            ValueError: If function already registered and override=False
        """
        if name in self._functions and not override:
            raise ValueError(
                f"Function '{name}' already registered. Use override=True to replace."
            )

        # Store the function
        self._functions[name] = func

        # Extract metadata using i2.Sig
        self._metadata[name] = self._extract_metadata(name, func)

    def _extract_metadata(self, name: str, func: Callable) -> FunctionMetadata:
        """Extract metadata from a function using i2.Sig.

        Args:
            name: Function name
            func: The callable

        Returns:
            FunctionMetadata with extracted information
        """
        # Get signature using i2
        sig = Sig(func)

        # Extract parameters
        parameters = []
        for param_name in sig.names:
            param = sig.params[param_name]

            # Get annotation as string
            annotation = "Any"
            if param.annotation != inspect.Parameter.empty:
                annotation = (
                    param.annotation.__name__
                    if hasattr(param.annotation, "__name__")
                    else str(param.annotation)
                )

            # Check for default value
            has_default = param.default != inspect.Parameter.empty
            default = param.default if has_default else None

            parameters.append(
                ParameterInfo(
                    name=param_name,
                    annotation=annotation,
                    default=default,
                    has_default=has_default,
                    kind=param.kind.name,
                )
            )

        # Extract return annotation
        return_annotation = "Any"
        if sig.return_annotation != inspect.Signature.empty:
            return_annotation = (
                sig.return_annotation.__name__
                if hasattr(sig.return_annotation, "__name__")
                else str(sig.return_annotation)
            )

        return FunctionMetadata(
            name=name,
            doc=inspect.getdoc(func),
            parameters=parameters,
            return_annotation=return_annotation,
            module=func.__module__ if hasattr(func, "__module__") else None,
        )

    def get_function(self, name: str) -> Callable:
        """Get a registered function by name.

        Args:
            name: Function name

        Returns:
            The registered function

        Raises:
            KeyError: If function not found
        """
        if name not in self._functions:
            raise KeyError(f"Function '{name}' not found in registry")
        return self._functions[name]

    def get_metadata(self, name: str) -> FunctionMetadata:
        """Get metadata for a registered function.

        Args:
            name: Function name

        Returns:
            FunctionMetadata for the function

        Raises:
            KeyError: If function not found
        """
        if name not in self._metadata:
            raise KeyError(f"Function '{name}' not found in registry")
        return self._metadata[name]

    def list_functions(self) -> List[str]:
        """List all registered function names.

        Returns:
            List of function names
        """
        return list(self._functions.keys())

    def unregister(self, name: str) -> None:
        """Remove a function from the registry.

        Args:
            name: Function name to remove

        Raises:
            KeyError: If function not found
        """
        if name not in self._functions:
            raise KeyError(f"Function '{name}' not found in registry")

        del self._functions[name]
        del self._metadata[name]

    def get_all_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all registered functions.

        Returns:
            Dictionary mapping function names to metadata dicts
        """
        return {name: meta.to_dict() for name, meta in self._metadata.items()}


# Create a global registry instance
_global_registry = FunctionRegistry()


def register_function(name: str, func: Callable, *, override: bool = False) -> None:
    """Register a function in the global registry.

    Args:
        name: Name to register the function under
        func: The callable to register
        override: If True, allow overriding existing registrations
    """
    _global_registry.register(name, func, override=override)


def get_global_registry() -> FunctionRegistry:
    """Get the global function registry instance.

    Returns:
        The global FunctionRegistry
    """
    return _global_registry
