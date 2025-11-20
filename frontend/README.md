# app_meshed Frontend

**React + TypeScript frontend for the app_meshed platform**

A modern web interface for composing, executing, and visualizing meshed DAGs with integrated support for:
- Store browsing and CRUD operations (dol)
- Visual DAG composition with React Flow
- Dynamic form generation with RJSF
- Multi-channel time-series visualization with Plotly

---

## Features

### 🗂️ Phase I: Store Browser
- Browse all four dol stores (raw_data, functions, meshes, configs)
- Create, read, update, and delete items
- JSON editor for configurations
- Real-time synchronization with backend

### 🔗 Phase II: Mesh Maker
- Visual DAG composition with React Flow
- Drag-and-drop function nodes
- Automatic form generation for node configuration (RJSF)
- Connect nodes to create data pipelines
- Execute DAGs with custom inputs
- Save/load DAG configurations

### 📊 Phase III: Stream Viewer
- Multi-channel time-series visualization
- Interactive zoom and pan controls
- Synchronized data from multiple streams
- Real-time [bt:tt] time-based slicing
- Channel metadata display

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **TypeScript** | Type safety |
| **Vite** | Build tool & dev server |
| **React Flow** | DAG canvas |
| **RJSF** | Form generation |
| **Plotly** | Data visualization |
| **TanStack Query** | Data fetching & caching |
| **Axios** | HTTP client |
| **Playwright** | E2E testing |
| **Lucide React** | Icons |

---

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- app_meshed backend running on `localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:5173

### Backend Connection

The frontend expects the backend API at `http://localhost:8000`. To use a different URL, create a `.env` file:

```bash
VITE_API_BASE_URL=http://your-backend-url:port
```

---

## Available Scripts

```bash
# Development
npm run dev              # Start dev server (hot reload)
npm run build            # Build for production
npm run preview          # Preview production build

# Testing
npm run test:e2e         # Run Playwright E2E tests
npm run test:e2e:ui      # Run tests with Playwright UI
npm run test:e2e:headed  # Run tests in headed mode
npm run test:e2e:report  # Show test report

# Code Quality
npm run lint             # Lint code with ESLint
```

---

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts            # API client for backend
│   ├── components/              # Reusable components (future)
│   ├── pages/
│   │   ├── StoreBrowser.tsx     # Phase I: Store CRUD
│   │   ├── MeshMaker.tsx        # Phase II: DAG canvas
│   │   └── StreamViewer.tsx     # Phase III: Visualization
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── App.tsx                  # Main app component
│   ├── App.css                  # Global styles
│   └── main.tsx                 # Entry point
│
├── e2e/
│   ├── store-browser.spec.ts    # Store Browser tests
│   ├── mesh-maker.spec.ts       # Mesh Maker tests
│   ├── stream-viewer.spec.ts    # Stream Viewer tests
│   └── app-integration.spec.ts  # Integration tests
│
├── playwright.config.ts         # Playwright configuration
├── vite.config.ts              # Vite configuration
└── package.json
```

---

## Usage Guide

### Store Browser

1. **Select a Store**: Click on one of the four stores (meshes, configs, functions, raw_data)
2. **Browse Keys**: View all items in the selected store
3. **View Item**: Click on a key to view its contents
4. **Create Item**: Click the + button, enter a key and JSON value
5. **Delete Item**: Select an item and click the delete button

### Mesh Maker

1. **Add Nodes**: Click on a function in the left panel to add it to the canvas
2. **Configure Nodes**: Click a node to see its configuration form (RJSF)
3. **Connect Nodes**: Drag from one node's output to another's input
4. **Set DAG Name**: Enter a name in the top-left input
5. **Execute**: Enter inputs in JSON format and click "Execute"
6. **Save**: Click "Save" to persist the DAG to the meshes store

### Stream Viewer

1. **Select Streams**: Check the boxes next to streams you want to visualize
2. **View Plot**: Multi-channel plot appears automatically
3. **Zoom**: Use the zoom in/out buttons to adjust time scale
4. **Pan**: Use pan left/right to navigate through time
5. **Refresh**: Click refresh to reload data from backend

---

## API Client

The TypeScript API client (`src/api/client.ts`) provides methods for all backend endpoints:

```typescript
import { apiClient } from './api/client';

// Store operations
await apiClient.listStores();
await apiClient.getStoreItem('meshes', 'my_dag');
await apiClient.putStoreItem('meshes', 'my_dag', dagConfig);

// Function operations
await apiClient.listFunctions();
await apiClient.getFunctionSchema('add');

// DAG operations
await apiClient.executeDAG(dagConfig, inputs);
await apiClient.validateDAG(dagConfig);

// Stream operations
await apiClient.listStreams();
await apiClient.sliceStream('audio_sample', 0, 5);
await apiClient.sliceMultiChannel(['accel_x', 'accel_y'], 0, 10);
```

---

## Testing

### E2E Tests with Playwright

The app includes comprehensive E2E tests covering all three phases:

**Store Browser Tests** (8 tests)
- Display stores
- Select store and view keys
- Create new items
- View item content
- Delete items
- Switch between stores

**Mesh Maker Tests** (8 tests)
- Display function palette
- Add function nodes
- Configure nodes with RJSF forms
- Update DAG name
- Save DAG
- Execute DAG
- Connect nodes

**Stream Viewer Tests** (11 tests)
- Display available streams
- Select streams
- Display metadata
- Zoom in/out
- Pan left/right
- Refresh data
- Multi-channel visualization

**Integration Tests** (7 tests)
- Navigation between views
- State persistence
- Complete workflows
- Backend connectivity

### Running Tests

```bash
# Run all tests
npm run test:e2e

# Run with UI (recommended for debugging)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# View test report
npm run test:e2e:report
```

---

## Type Safety

The frontend is fully typed with TypeScript. Key types are defined in `src/types/index.ts`:

- `FunctionMetadata`: Function signature information
- `DAGConfig`: DAG structure (nodes, edges)
- `DAGExecutionResult`: Execution response
- `StreamMetadata`: Stream information
- `StreamSliceData`: Time-series data
- And more...

---

## State Management

- **TanStack Query**: Server state management with automatic caching and refetching
- **React State**: Local UI state for forms, selections, etc.
- **Query Keys**: Organized by feature (e.g., `['store-keys', storeName]`)

---

## Styling

- **Inline Styles**: Used for component-specific styling
- **CSS**: Global styles in `App.css`
- **React Flow**: Styled with built-in classes
- **Responsive**: Flexbox-based layouts

---

## Development Tips

### Hot Module Replacement (HMR)

Vite provides instant HMR. Changes to React components update immediately without page reload.

### Backend Connection Issues

If the frontend can't connect to the backend:

1. Ensure backend is running: `python -m app_meshed.cli`
2. Check the backend URL in `.env`
3. Check browser console for CORS errors
4. Verify backend is on port 8000

### Debugging Tests

```bash
# Run a specific test file
npx playwright test e2e/store-browser.spec.ts

# Run in debug mode
npx playwright test --debug

# Run with browser visible
npm run test:e2e:headed
```

---

## Performance

- **Code Splitting**: Vite automatically splits code for optimal loading
- **React Flow**: Efficiently handles large DAGs
- **Plotly**: Hardware-accelerated rendering for smooth visualizations
- **TanStack Query**: Smart caching reduces unnecessary API calls

---

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update types in `src/types/index.ts`
4. Test with `npm run test:e2e`

---

## License

MIT

---

## Related

- **Backend**: `../app_meshed` - Python FastAPI backend
- **Architecture**: `../ARCHITECTURE.md` - Full system design
- **Examples**: `../examples/` - Backend integration examples

---

Built with ❤️ using React, React Flow, RJSF, and Plotly
