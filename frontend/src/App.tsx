/**
 * Main App Component - app_meshed Frontend
 */

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Database, Workflow, Activity } from 'lucide-react';
import { StoreBrowser } from './pages/StoreBrowser';
import { MeshMaker } from './pages/MeshMaker';
import { StreamViewer } from './pages/StreamViewer';
import './App.css';

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5000,
      retry: 1,
    },
  },
});

type View = 'store' | 'mesh' | 'stream';

function App() {
  const [currentView, setCurrentView] = useState<View>('mesh');

  const renderView = () => {
    switch (currentView) {
      case 'store':
        return <StoreBrowser />;
      case 'mesh':
        return <MeshMaker />;
      case 'stream':
        return <StreamViewer />;
      default:
        return <MeshMaker />;
    }
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="app-meshed" style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        {/* Header */}
        <header
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '1rem 2rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
              app_meshed
            </h1>
            <span style={{ fontSize: '0.875rem', opacity: 0.9 }}>
              Modular DAG Composition Platform
            </span>
          </div>

          {/* Navigation Tabs */}
          <nav style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={() => setCurrentView('store')}
              className={currentView === 'store' ? 'active' : ''}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '0.375rem',
                background: currentView === 'store' ? 'rgba(255,255,255,0.2)' : 'transparent',
                color: 'white',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'background 0.2s',
              }}
            >
              <Database size={18} />
              Store Browser
            </button>
            <button
              onClick={() => setCurrentView('mesh')}
              className={currentView === 'mesh' ? 'active' : ''}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '0.375rem',
                background: currentView === 'mesh' ? 'rgba(255,255,255,0.2)' : 'transparent',
                color: 'white',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'background 0.2s',
              }}
            >
              <Workflow size={18} />
              Mesh Maker
            </button>
            <button
              onClick={() => setCurrentView('stream')}
              className={currentView === 'stream' ? 'active' : ''}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '0.375rem',
                background: currentView === 'stream' ? 'rgba(255,255,255,0.2)' : 'transparent',
                color: 'white',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'background 0.2s',
              }}
            >
              <Activity size={18} />
              Stream Viewer
            </button>
          </nav>
        </header>

        {/* Main Content */}
        <main style={{ flex: 1, overflow: 'hidden' }}>
          {renderView()}
        </main>

        {/* Footer */}
        <footer
          style={{
            background: '#f9fafb',
            padding: '0.75rem 2rem',
            borderTop: '1px solid #e5e7eb',
            fontSize: '0.875rem',
            color: '#6b7280',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            Built with React, React Flow, RJSF, and Plotly
          </div>
          <div>
            Backend: <span style={{ fontFamily: 'monospace' }}>localhost:8000</span>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

export default App;
