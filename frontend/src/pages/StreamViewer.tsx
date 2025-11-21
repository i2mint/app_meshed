/**
 * Stream Viewer Page - Phase III: Multi-channel time-series visualization
 */

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import Plot from 'react-plotly.js';
import { ZoomIn, ZoomOut, RefreshCw } from 'lucide-react';
import type { StreamsResponse, MultiChannelSliceResponse } from '../types';

export function StreamViewer() {
  const [selectedStreams, setSelectedStreams] = useState<string[]>([]);
  const [timeRange, setTimeRange] = useState({ bt: 0, tt: 5 });
  const [zoom, setZoom] = useState(1);

  // Query for available streams
  const { data: streamsData } = useQuery<StreamsResponse>({
    queryKey: ['streams'],
    queryFn: () => apiClient.listStreams(),
  });

  // Query for multi-channel data
  const { data: channelData, refetch } = useQuery<MultiChannelSliceResponse>({
    queryKey: ['stream-slice', selectedStreams, timeRange],
    queryFn: () => apiClient.sliceMultiChannel(selectedStreams, timeRange.bt, timeRange.tt),
    enabled: selectedStreams.length > 0,
  });

  // Auto-select first 3 streams on load
  useEffect(() => {
    if (streamsData && selectedStreams.length === 0) {
      const firstThree = streamsData.streams.slice(0, 3);
      setSelectedStreams(firstThree);
    }
  }, [streamsData, selectedStreams.length]);

  const toggleStream = (streamId: string) => {
    setSelectedStreams((prev) =>
      prev.includes(streamId) ? prev.filter((id) => id !== streamId) : [...prev, streamId]
    );
  };

  const handleZoomIn = () => {
    const duration = timeRange.tt - timeRange.bt;
    const newDuration = duration / 2;
    const center = (timeRange.bt + timeRange.tt) / 2;
    setTimeRange({
      bt: center - newDuration / 2,
      tt: center + newDuration / 2,
    });
    setZoom(zoom * 2);
  };

  const handleZoomOut = () => {
    const duration = timeRange.tt - timeRange.bt;
    const newDuration = duration * 2;
    const center = (timeRange.bt + timeRange.tt) / 2;
    setTimeRange({
      bt: Math.max(0, center - newDuration / 2),
      tt: center + newDuration / 2,
    });
    setZoom(zoom / 2);
  };

  const handlePan = (direction: 'left' | 'right') => {
    const duration = timeRange.tt - timeRange.bt;
    const shift = duration * 0.5 * (direction === 'left' ? -1 : 1);
    setTimeRange({
      bt: Math.max(0, timeRange.bt + shift),
      tt: timeRange.tt + shift,
    });
  };

  // Prepare plot data
  const plotData = selectedStreams.map((streamId) => {
    const data = channelData?.channels[streamId];
    if (!data || 'error' in data) return null;

    const numPoints = data.data.length;
    const timeAxis = Array.from({ length: numPoints }, (_, i) => timeRange.bt + (i / numPoints) * (timeRange.tt - timeRange.bt));

    return {
      x: timeAxis,
      y: data.data,
      type: 'scatter',
      mode: 'lines',
      name: streamId,
      line: { width: 1 },
    };
  }).filter(Boolean);

  return (
    <div className="stream-viewer" style={{ display: 'flex', height: '100%' }}>
      {/* Stream Selection Sidebar */}
      <div
        className="sidebar"
        style={{
          width: '250px',
          borderRight: '1px solid #e5e7eb',
          padding: '1rem',
          overflow: 'auto',
        }}
      >
        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Streams
        </h2>

        <div className="stream-list">
          {streamsData?.streams.map((streamId) => {
            const metadata = streamsData.metadata[streamId];
            return (
              <div
                key={streamId}
                style={{
                  padding: '0.75rem',
                  marginBottom: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  background: selectedStreams.includes(streamId) ? '#dbeafe' : 'white',
                }}
              >
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={selectedStreams.includes(streamId)}
                    onChange={() => toggleStream(streamId)}
                    style={{ marginRight: '0.5rem' }}
                  />
                  <div>
                    <div style={{ fontWeight: '500' }}>{streamId}</div>
                    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                      {metadata.sample_rate} Hz
                      {metadata.length_seconds && ` • ${metadata.length_seconds.toFixed(1)}s`}
                    </div>
                  </div>
                </label>
              </div>
            );
          })}
        </div>
      </div>

      {/* Visualization Area */}
      <div className="viz-area" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Controls */}
        <div
          className="controls"
          style={{
            padding: '1rem',
            borderBottom: '1px solid #e5e7eb',
            display: 'flex',
            gap: '1rem',
            alignItems: 'center',
          }}
        >
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={handleZoomIn}
              style={{
                padding: '0.5rem',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
              title="Zoom In"
            >
              <ZoomIn size={16} />
            </button>
            <button
              onClick={handleZoomOut}
              style={{
                padding: '0.5rem',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
              title="Zoom Out"
            >
              <ZoomOut size={16} />
            </button>
            <button
              onClick={() => refetch()}
              style={{
                padding: '0.5rem',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
              title="Refresh"
            >
              <RefreshCw size={16} />
            </button>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={() => handlePan('left')}
              style={{
                padding: '0.5rem 1rem',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                cursor: 'pointer',
              }}
            >
              ← Pan Left
            </button>
            <button
              onClick={() => handlePan('right')}
              style={{
                padding: '0.5rem 1rem',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                cursor: 'pointer',
              }}
            >
              Pan Right →
            </button>
          </div>

          <div style={{ marginLeft: 'auto' }}>
            <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>
              Time: {timeRange.bt.toFixed(2)}s - {timeRange.tt.toFixed(2)}s
              {' • '}
              Zoom: {zoom.toFixed(1)}x
            </span>
          </div>
        </div>

        {/* Plot */}
        <div className="plot-container" style={{ flex: 1, padding: '1rem' }}>
          {selectedStreams.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#6b7280', marginTop: '2rem' }}>
              Select streams to visualize
            </div>
          ) : (
            <Plot
              data={plotData as any}
              layout={{
                title: 'Multi-Channel Stream View',
                xaxis: {
                  title: 'Time (seconds)',
                  range: [timeRange.bt, timeRange.tt],
                },
                yaxis: {
                  title: 'Amplitude',
                },
                showlegend: true,
                height: 600,
                margin: { t: 50, b: 50, l: 50, r: 50 },
              }}
              config={{
                responsive: true,
                displayModeBar: true,
              }}
              style={{ width: '100%', height: '100%' }}
            />
          )}
        </div>

        {/* Channel Info */}
        {channelData && (
          <div
            className="channel-info"
            style={{
              padding: '1rem',
              borderTop: '1px solid #e5e7eb',
              background: '#f9fafb',
            }}
          >
            <h3 style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              Channel Information
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              {selectedStreams.map((streamId) => {
                const data = channelData.channels[streamId];
                if ('error' in data) {
                  return (
                    <div key={streamId} style={{ fontSize: '0.875rem' }}>
                      <strong>{streamId}:</strong> Error - {data.error}
                    </div>
                  );
                }
                return (
                  <div key={streamId} style={{ fontSize: '0.875rem' }}>
                    <strong>{streamId}:</strong>
                    <div style={{ color: '#6b7280' }}>
                      {data.shape[0]} samples @ {data.sample_rate} Hz
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
