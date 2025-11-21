"""Example demonstrating ju-based JSON Schema generation.

This example shows how function signatures are automatically converted
to JSON Schemas suitable for React JSON Schema Form (RJSF).
"""

import json
from app_meshed.services.schema_service import func_to_schema, object_to_schema


def process_audio(
    audio_data: str,
    sample_rate: int = 44100,
    gain: float = 1.0,
    normalize: bool = True,
) -> dict:
    """Process audio data with configurable parameters.

    Args:
        audio_data: Path to audio file
        sample_rate: Sample rate in Hz
        gain: Gain multiplier
        normalize: Whether to normalize the output

    Returns:
        Processed audio metadata
    """
    return {
        "processed": True,
        "sample_rate": sample_rate,
        "gain": gain,
        "normalized": normalize,
    }


def main():
    """Run the ju schema generation example."""
    print("=" * 70)
    print("JSON Schema Generation Example (ju + i2)")
    print("=" * 70)
    print()

    # Example 1: Generate schema from function signature
    print("Example 1: Function to JSON Schema")
    print("-" * 70)
    print()

    schema = func_to_schema(process_audio, title="Audio Processing")

    print("Function signature:")
    print(f"  {process_audio.__name__}{process_audio.__code__.co_varnames[:process_audio.__code__.co_argcount]}")
    print()

    print("Generated JSON Schema (for RJSF):")
    print(json.dumps(schema, indent=2))
    print()

    # Example 2: Schema from a configuration object
    print("=" * 70)
    print("Example 2: Object to JSON Schema")
    print("-" * 70)
    print()

    config = {
        "server": {
            "host": "localhost",
            "port": 8000,
            "debug": True,
        },
        "data_path": "/path/to/data",
        "max_connections": 100,
    }

    object_schema = object_to_schema(config, title="Server Configuration")

    print("Configuration object:")
    print(json.dumps(config, indent=2))
    print()

    print("Generated JSON Schema:")
    print(json.dumps(object_schema, indent=2))
    print()

    # Example 3: Different parameter types
    print("=" * 70)
    print("Example 3: Various Parameter Types")
    print("-" * 70)
    print()

    def complex_function(
        name: str,
        age: int,
        height: float,
        active: bool,
        tags: list,
        metadata: dict,
        optional_note: str = "default note",
    ) -> dict:
        """Function with various parameter types."""
        return {}

    complex_schema = func_to_schema(complex_function, title="Complex Parameters")

    print("Function with various types:")
    print(json.dumps(complex_schema, indent=2))
    print()

    # Example 4: How this is used in the API
    print("=" * 70)
    print("Example 4: API Usage Pattern")
    print("-" * 70)
    print()

    print("In the app_meshed API:")
    print("  1. Frontend requests: GET /schema/function/process_audio")
    print("  2. Backend generates schema using func_to_schema()")
    print("  3. Frontend receives JSON Schema")
    print("  4. RJSF renders a form based on the schema")
    print("  5. User fills form and submits")
    print("  6. Frontend sends validated data to DAG execution endpoint")
    print()

    print("API Response Example:")
    api_response = {
        "endpoint": "/schema/function/process_audio",
        "method": "GET",
        "response": schema,
    }
    print(json.dumps(api_response, indent=2))
    print()

    print("=" * 70)
    print("Schema Generation Complete!")
    print("=" * 70)
    print()
    print("Key Benefits:")
    print("  ✓ No manual form definitions needed")
    print("  ✓ Type-safe: schemas match actual function signatures")
    print("  ✓ Self-documenting: docstrings included in schemas")
    print("  ✓ Automatic validation in the frontend")
    print()


if __name__ == "__main__":
    main()
