"""Example demonstrating creek-inspired stream slicing.

This example shows how to work with time-series data using
[bt:tt] (bottom-time:top-time) slicing.
"""

import numpy as np
import tempfile
from pathlib import Path

from app_meshed.services.stream_service import (
    FileStreamSource,
    StreamRegistry,
    MultiChannelView,
)


def create_sample_data(file_path: Path, sample_rate: float, duration: float, signal_type: str = "sine"):
    """Create sample time-series data.

    Args:
        file_path: Where to save the data
        sample_rate: Samples per second
        duration: Duration in seconds
        signal_type: Type of signal to generate
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples)

    if signal_type == "sine":
        # 440 Hz sine wave (musical note A4)
        data = np.sin(2 * np.pi * 440 * t)
    elif signal_type == "chirp":
        # Chirp signal (frequency increases over time)
        f0, f1 = 100, 1000  # Start and end frequencies
        data = np.sin(2 * np.pi * (f0 + (f1 - f0) * t / duration) * t)
    elif signal_type == "noise":
        # Random noise
        data = np.random.randn(num_samples) * 0.1
    else:
        # Accelerometer-like data
        data = np.random.randn(num_samples) * 0.5 + np.sin(2 * np.pi * 2 * t) * 0.3

    np.save(file_path, data)
    return data


def main():
    """Run the stream slicing example."""
    print("=" * 70)
    print("Stream Slicing Example (creek-inspired [bt:tt])")
    print("=" * 70)
    print()

    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)

        # Example 1: Create and slice a single stream
        print("Example 1: Basic Time-Based Slicing")
        print("-" * 70)
        print()

        # Create sample audio data
        audio_path = data_dir / "audio.npy"
        sample_rate = 44100  # 44.1 kHz (CD quality)
        duration = 5  # 5 seconds

        print(f"Creating audio stream:")
        print(f"  Sample rate: {sample_rate} Hz")
        print(f"  Duration: {duration} seconds")
        print(f"  Total samples: {sample_rate * duration}")
        print()

        create_sample_data(audio_path, sample_rate, duration, "sine")

        # Create stream source
        audio_stream = FileStreamSource(
            source_id="audio_sample",
            file_path=audio_path,
            sample_rate=sample_rate,
        )

        # Slice using [bt:tt] notation
        print("Time-based slicing examples:")
        print()

        # Slice from 1.0s to 2.0s
        chunk1 = audio_stream[1.0:2.0]
        print(f"  audio_stream[1.0:2.0]")
        print(f"    Shape: {chunk1.shape}")
        print(f"    Duration: 1.0 second")
        print(f"    Samples: {len(chunk1)}")
        print()

        # Slice from 0.5s to 1.5s
        chunk2 = audio_stream[0.5:1.5]
        print(f"  audio_stream[0.5:1.5]")
        print(f"    Shape: {chunk2.shape}")
        print(f"    Duration: 1.0 second")
        print(f"    Samples: {len(chunk2)}")
        print()

        # Get metadata
        metadata = audio_stream.get_metadata()
        print("Stream metadata:")
        print(f"  Source ID: {metadata['source_id']}")
        print(f"  Sample rate: {metadata['sample_rate']} Hz")
        print(f"  Length: {metadata['length_seconds']:.2f} seconds")
        print(f"  Total samples: {metadata['length_samples']}")
        print()

        # Example 2: Multi-channel synchronized slicing
        print("=" * 70)
        print("Example 2: Multi-Channel Synchronized Slicing")
        print("-" * 70)
        print()

        # Create multiple sensor streams
        sensor_rate = 100  # 100 Hz
        sensor_duration = 10  # 10 seconds

        streams_config = [
            ("accel_x", "accelerometer"),
            ("accel_y", "accelerometer"),
            ("accel_z", "accelerometer"),
            ("gyro_x", "noise"),
        ]

        registry = StreamRegistry()
        print("Creating multi-channel sensor data:")
        print()

        for stream_id, signal_type in streams_config:
            path = data_dir / f"{stream_id}.npy"
            create_sample_data(path, sensor_rate, sensor_duration, signal_type)

            stream = FileStreamSource(
                source_id=stream_id,
                file_path=path,
                sample_rate=sensor_rate,
            )
            registry.register(stream)
            print(f"  ✓ Registered: {stream_id} ({signal_type})")

        print()

        # Use multi-channel view for synchronized slicing
        multi_view = MultiChannelView(registry)

        bt, tt = 2.0, 4.0  # Get 2 seconds of data from t=2s to t=4s
        print(f"Synchronized slice from {bt}s to {tt}s:")
        print()

        result = multi_view.get_synchronized_slice(
            channel_ids=["accel_x", "accel_y", "accel_z"],
            bt=bt,
            tt=tt,
        )

        print(f"Time range: [{result['bt']}, {result['tt']}]")
        print(f"Channels: {len(result['channels'])}")
        print()

        for channel_id, channel_data in result["channels"].items():
            if "error" not in channel_data:
                print(f"  {channel_id}:")
                print(f"    Samples: {len(channel_data['data'])}")
                print(f"    Shape: {channel_data['shape']}")
                print(f"    Sample rate: {channel_data['sample_rate']} Hz")
        print()

        # Example 3: Stream registry operations
        print("=" * 70)
        print("Example 3: Stream Registry Operations")
        print("-" * 70)
        print()

        print("All registered streams:")
        for stream_id in registry.list_streams():
            print(f"  - {stream_id}")
        print()

        print("Stream metadata:")
        all_metadata = registry.get_all_metadata()
        for stream_id, meta in all_metadata.items():
            print(f"  {stream_id}:")
            print(f"    Sample rate: {meta['sample_rate']} Hz")
            print(f"    Duration: {meta['length_seconds']:.2f}s")
        print()

        # Example 4: Different slicing patterns
        print("=" * 70)
        print("Example 4: Slicing Patterns")
        print("-" * 70)
        print()

        stream = registry.get("accel_x")

        patterns = [
            ("First second", 0.0, 1.0),
            ("Middle section", 4.0, 6.0),
            ("Last two seconds", 8.0, 10.0),
            ("Narrow window", 5.0, 5.1),  # 100ms
        ]

        print("Different time windows:")
        for name, bt, tt in patterns:
            chunk = stream[bt:tt]
            duration = tt - bt
            print(f"  {name} [{bt}s:{tt}s]")
            print(f"    Duration: {duration}s")
            print(f"    Samples: {len(chunk)}")
            print(f"    Expected samples: {int(duration * sensor_rate)}")
            print()

        # Example 5: How this maps to HTTP API
        print("=" * 70)
        print("Example 5: HTTP API Usage")
        print("-" * 70)
        print()

        print("Python code -> HTTP API:")
        print()
        print("  stream[1.0:2.0]")
        print("  ↓")
        print("  GET /streams/audio_sample/slice?bt=1.0&tt=2.0")
        print()
        print("  multi_view.get_synchronized_slice(['accel_x', 'accel_y'], 2.0, 4.0)")
        print("  ↓")
        print("  POST /streams/multi-channel/slice")
        print("  Body: {")
        print('    "channel_ids": ["accel_x", "accel_y"],')
        print('    "bt": 2.0,')
        print('    "tt": 4.0')
        print("  }")
        print()

        print("=" * 70)
        print("Stream Slicing Example Complete!")
        print("=" * 70)
        print()
        print("Key Benefits of [bt:tt] Slicing:")
        print("  ✓ Time-based access: Natural for time-series data")
        print("  ✓ Uniform interface: Works across all stream types")
        print("  ✓ Synchronized views: Multi-channel data stays aligned")
        print("  ✓ Efficient: Only load what you need")
        print("  ✓ Scalable: Works with large datasets")
        print()
        print("Use Cases:")
        print("  • Audio processing: Extract segments for analysis")
        print("  • Sensor data: Analyze specific time windows")
        print("  • Multi-modal signals: Synchronized accelerometer + gyro")
        print("  • Streaming visualization: Zoom/pan in frontend")
        print()


if __name__ == "__main__":
    main()
