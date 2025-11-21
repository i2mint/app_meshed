"""Hello World DAG Example.

This demonstrates the basic workflow:
1. Register a simple function
2. Create a DAG configuration
3. Execute the DAG
4. Get function schema for form generation
"""

from app_meshed.services.function_registry import FunctionRegistry
from app_meshed.services.dag_service import DAGService
from app_meshed.services.schema_service import func_to_schema


def main():
    """Run the Hello World DAG example."""
    print("=" * 60)
    print("Hello World DAG Example")
    print("=" * 60)
    print()

    # Step 1: Create a simple function
    def add(a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b

    print("Step 1: Register the 'add' function")
    print(f"Function: {add.__name__}")
    print(f"Docstring: {add.__doc__.strip()}")
    print()

    # Step 2: Register the function
    registry = FunctionRegistry()
    registry.register("add", add)

    print("Step 2: Function registered successfully")
    print(f"Available functions: {registry.list_functions()}")
    print()

    # Step 3: Get function metadata
    metadata = registry.get_metadata("add")
    print("Step 3: Function metadata")
    print(f"Name: {metadata.name}")
    print(f"Parameters:")
    for param in metadata.parameters:
        print(f"  - {param.name}: {param.annotation}")
    print(f"Return type: {metadata.return_annotation}")
    print()

    # Step 4: Generate JSON Schema for the function
    schema = func_to_schema(add)
    print("Step 4: Generated JSON Schema (for RJSF forms)")
    import json
    print(json.dumps(schema, indent=2))
    print()

    # Step 5: Create a simple DAG configuration
    dag_config = {
        "name": "hello_world_dag",
        "nodes": [
            {
                "id": "add_node",
                "function": "add",
                "output_name": "result"
            }
        ],
        "edges": [],
        "params": {}
    }

    print("Step 5: DAG Configuration")
    print(json.dumps(dag_config, indent=2))
    print()

    # Step 6: Execute the DAG
    dag_service = DAGService(registry)

    inputs = {
        "a": 5,
        "b": 3
    }

    print(f"Step 6: Execute DAG with inputs: {inputs}")

    result = dag_service.execute_from_config(dag_config, inputs)

    print(f"Execution Status: {result['status']}")
    print(f"Result: {result['result']}")
    print()

    # Step 7: Demonstrate chained DAG
    print("=" * 60)
    print("Bonus: Chained DAG Example")
    print("=" * 60)
    print()

    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    registry.register("multiply", multiply)

    chained_config = {
        "name": "chained_operations",
        "nodes": [
            {"id": "add_step", "function": "add"},
            {"id": "multiply_step", "function": "multiply"}
        ],
        "edges": [
            {
                "source": "add_step",
                "target": "multiply_step",
                "sourceOutput": "add_step",  # Output from add
                "targetInput": "a"  # Input to multiply
            }
        ],
        "params": {}
    }

    print("Chained DAG: (a + b) * c")
    print(f"Configuration: {json.dumps(chained_config, indent=2)}")
    print()

    chained_inputs = {
        "a": 5,
        "b": 3,
        "multiply_step": {"b": 2}  # c = 2
    }

    print(f"Inputs: a=5, b=3, c=2")
    print(f"Expected: (5 + 3) * 2 = 16")
    print()

    chained_result = dag_service.execute_from_config(chained_config, chained_inputs)

    print(f"Status: {chained_result['status']}")
    print(f"Result: {chained_result['result']}")
    print()

    print("=" * 60)
    print("Example Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
