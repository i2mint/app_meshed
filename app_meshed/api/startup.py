"""Startup initialization for app_meshed.

This module handles initialization tasks that run when the server starts:
- Registering example functions
- Setting up default stores
- Initializing sample data
"""

import logging
from pathlib import Path

from app_meshed.services.function_registry import get_global_registry
from app_meshed.services.stream_service import get_stream_registry, FileStreamSource
from app_meshed.utils.example_functions import EXAMPLE_FUNCTIONS

logger = logging.getLogger(__name__)


def register_example_functions():
    """Register all example functions in the global registry."""
    registry = get_global_registry()

    for func_name, func in EXAMPLE_FUNCTIONS:
        try:
            registry.register(func_name, func, override=True)
            logger.info(f"Registered function: {func_name}")
        except Exception as e:
            logger.error(f"Failed to register function {func_name}: {e}")

    logger.info(f"Registered {len(EXAMPLE_FUNCTIONS)} example functions")


def initialize_sample_streams(data_path: str = "./data"):
    """Initialize sample stream sources for demonstration.

    Args:
        data_path: Base path for data storage
    """
    import numpy as np

    stream_registry = get_stream_registry()
    data_dir = Path(data_path) / "raw_data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create sample data files
    sample_streams = [
        {
            "id": "audio_sample",
            "rate": 44100,  # 44.1 kHz
            "duration": 10,  # 10 seconds
        },
        {
            "id": "sensor_accel_x",
            "rate": 100,  # 100 Hz
            "duration": 60,  # 1 minute
        },
        {
            "id": "sensor_accel_y",
            "rate": 100,
            "duration": 60,
        },
    ]

    for stream_config in sample_streams:
        stream_id = stream_config["id"]
        sample_rate = stream_config["rate"]
        duration = stream_config["duration"]
        num_samples = int(sample_rate * duration)

        # Generate sample data
        file_path = data_dir / f"{stream_id}.npy"

        if not file_path.exists():
            # Create synthetic data
            if "audio" in stream_id:
                # Generate a simple sine wave
                t = np.linspace(0, duration, num_samples)
                data = np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
            else:
                # Generate random sensor data
                data = np.random.randn(num_samples) * 0.1

            np.save(file_path, data)
            logger.info(f"Created sample data: {file_path}")

        # Register the stream
        stream = FileStreamSource(
            source_id=stream_id,
            file_path=file_path,
            sample_rate=sample_rate,
        )
        stream_registry.register(stream)
        logger.info(f"Registered stream: {stream_id}")

    logger.info(f"Initialized {len(sample_streams)} sample streams")


def run_startup_initialization(data_path: str = "./data"):
    """Run all startup initialization tasks.

    Args:
        data_path: Base path for data storage
    """
    logger.info("Running startup initialization...")

    # Register example functions
    register_example_functions()

    # Initialize sample streams
    try:
        initialize_sample_streams(data_path)
    except Exception as e:
        logger.warning(f"Failed to initialize sample streams: {e}")

    logger.info("Startup initialization complete")
