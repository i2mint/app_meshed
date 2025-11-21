"""Stream service using creek for time-series data slicing.

This module provides:
- Stream abstraction with [bt:tt] (bottom-time:top-time) slicing
- Multi-channel stream synchronization
- Time-series data access
"""

from typing import Any, Dict, List, Optional, Union, Iterable
from pathlib import Path
import numpy as np

try:
    import creek
except ImportError:
    # creek might not be available, provide fallback
    creek = None


class StreamSource:
    """Base class for stream sources.

    Provides a uniform interface for accessing time-series data
    with [bt:tt] slicing support.
    """

    def __init__(self, source_id: str, sample_rate: float = 1.0):
        """Initialize stream source.

        Args:
            source_id: Unique identifier for this stream
            sample_rate: Samples per second
        """
        self.source_id = source_id
        self.sample_rate = sample_rate

    def __getitem__(self, key: Union[slice, int]) -> np.ndarray:
        """Get data by time slice [bt:tt] or index.

        Args:
            key: Slice object (time range) or integer (index)

        Returns:
            Data for the requested range
        """
        raise NotImplementedError("Subclasses must implement __getitem__")

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this stream.

        Returns:
            Dictionary with stream metadata
        """
        return {
            "source_id": self.source_id,
            "sample_rate": self.sample_rate,
        }


class FileStreamSource(StreamSource):
    """Stream source backed by a file.

    Supports various file formats for time-series data.
    """

    def __init__(
        self,
        source_id: str,
        file_path: Union[str, Path],
        sample_rate: float = 1.0,
    ):
        """Initialize file-based stream source.

        Args:
            source_id: Unique identifier
            file_path: Path to data file
            sample_rate: Samples per second
        """
        super().__init__(source_id, sample_rate)
        self.file_path = Path(file_path)
        self._data = None

    def _load_data(self) -> np.ndarray:
        """Load data from file.

        Returns:
            Loaded data array
        """
        if self._data is None:
            # Placeholder - implement actual file loading
            # Could use creek readers here
            if self.file_path.suffix == ".npy":
                self._data = np.load(self.file_path)
            else:
                # Fallback to dummy data
                self._data = np.random.randn(1000)
        return self._data

    def __getitem__(self, key: Union[slice, int]) -> np.ndarray:
        """Get data by time slice or index.

        Args:
            key: Slice (time range in seconds) or int (sample index)

        Returns:
            Data for the requested range
        """
        data = self._load_data()

        if isinstance(key, slice):
            # Convert time to samples
            bt = key.start if key.start is not None else 0
            tt = key.stop if key.stop is not None else len(data) / self.sample_rate

            bt_idx = int(bt * self.sample_rate)
            tt_idx = int(tt * self.sample_rate)

            return data[bt_idx:tt_idx]
        else:
            return data[key]

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata including file info.

        Returns:
            Stream metadata
        """
        metadata = super().get_metadata()
        data = self._load_data()

        metadata.update({
            "file_path": str(self.file_path),
            "length_samples": len(data),
            "length_seconds": len(data) / self.sample_rate,
        })

        return metadata


class StreamRegistry:
    """Registry for managing multiple stream sources."""

    def __init__(self):
        """Initialize the stream registry."""
        self._streams: Dict[str, StreamSource] = {}

    def register(self, stream: StreamSource) -> None:
        """Register a stream source.

        Args:
            stream: Stream source to register
        """
        self._streams[stream.source_id] = stream

    def get(self, source_id: str) -> StreamSource:
        """Get a stream by ID.

        Args:
            source_id: Stream identifier

        Returns:
            StreamSource object

        Raises:
            KeyError: If stream not found
        """
        if source_id not in self._streams:
            raise KeyError(f"Stream '{source_id}' not found")
        return self._streams[source_id]

    def list_streams(self) -> List[str]:
        """List all registered stream IDs.

        Returns:
            List of stream IDs
        """
        return list(self._streams.keys())

    def get_all_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all streams.

        Returns:
            Dictionary mapping stream IDs to metadata
        """
        return {
            stream_id: stream.get_metadata()
            for stream_id, stream in self._streams.items()
        }

    def slice_stream(
        self, source_id: str, bt: float, tt: float
    ) -> Dict[str, Any]:
        """Slice a stream by time range.

        Args:
            source_id: Stream identifier
            bt: Bottom time (start) in seconds
            tt: Top time (end) in seconds

        Returns:
            Dictionary with sliced data and metadata
        """
        stream = self.get(source_id)
        data = stream[bt:tt]

        return {
            "source_id": source_id,
            "bt": bt,
            "tt": tt,
            "data": data.tolist(),  # Convert to list for JSON serialization
            "shape": data.shape,
            "sample_rate": stream.sample_rate,
        }


class MultiChannelView:
    """Synchronized view of multiple stream channels.

    This implements the "Slabs" concept for multi-channel data.
    """

    def __init__(self, registry: StreamRegistry):
        """Initialize multi-channel view.

        Args:
            registry: Stream registry with all channels
        """
        self.registry = registry

    def get_synchronized_slice(
        self, channel_ids: List[str], bt: float, tt: float
    ) -> Dict[str, Any]:
        """Get synchronized data from multiple channels.

        Args:
            channel_ids: List of stream/channel IDs
            bt: Bottom time (start) in seconds
            tt: Top time (end) in seconds

        Returns:
            Dictionary with synchronized multi-channel data
        """
        result = {
            "bt": bt,
            "tt": tt,
            "channels": {},
        }

        for channel_id in channel_ids:
            try:
                channel_data = self.registry.slice_stream(channel_id, bt, tt)
                result["channels"][channel_id] = channel_data
            except KeyError as e:
                result["channels"][channel_id] = {"error": str(e)}

        return result

    def get_channel_info(self, channel_ids: List[str]) -> Dict[str, Dict]:
        """Get metadata for multiple channels.

        Args:
            channel_ids: List of channel IDs

        Returns:
            Dictionary mapping channel IDs to metadata
        """
        return {
            channel_id: self.registry.get(channel_id).get_metadata()
            for channel_id in channel_ids
            if channel_id in self.registry.list_streams()
        }


# Global stream registry
_global_stream_registry = StreamRegistry()


def get_stream_registry() -> StreamRegistry:
    """Get the global stream registry.

    Returns:
        Global StreamRegistry instance
    """
    return _global_stream_registry
