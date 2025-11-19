"""CLI for running the app_meshed server.

This module provides a command-line interface for starting the
app_meshed HTTP server.
"""

import argparse
import os
import logging

import uvicorn


def setup_logging(level: str = "INFO"):
    """Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run the app_meshed HTTP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server on default port (8000)
  python -m app_meshed.cli

  # Start on custom port
  python -m app_meshed.cli --port 8080

  # Enable debug mode
  python -m app_meshed.cli --debug

  # Specify data directory
  python -m app_meshed.cli --data-path /path/to/data
        """,
    )

    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )

    parser.add_argument(
        "--data-path",
        default="./data",
        help="Path for data storage (default: ./data)",
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log_level)

    # Set data path environment variable
    os.environ["APP_MESHED_DATA_PATH"] = args.data_path

    # Print startup info
    print("=" * 60)
    print("app_meshed - HTTP services for meshed operations")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Data Path: {args.data_path}")
    print(f"Debug: {args.debug}")
    print(f"Auto-reload: {args.reload}")
    print("=" * 60)
    print(f"\nServer starting at: http://{args.host}:{args.port}")
    print(f"API Documentation: http://{args.host}:{args.port}/docs")
    print("=" * 60)
    print()

    # Run the server
    uvicorn.run(
        "app_meshed.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower(),
    )


if __name__ == "__main__":
    main()
