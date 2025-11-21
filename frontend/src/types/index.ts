/**
 * TypeScript types for app_meshed
 */

// ============================================================================
// Function Types
// ============================================================================

export interface ParameterInfo {
  name: string;
  annotation: string;
  default: any;
  has_default: boolean;
  kind: string;
}

export interface FunctionMetadata {
  name: string;
  doc: string | null;
  parameters: ParameterInfo[];
  return_annotation: string;
  module: string | null;
}

export interface FunctionsResponse {
  functions: string[];
  metadata: Record<string, FunctionMetadata>;
}

// ============================================================================
// DAG Types
// ============================================================================

export interface DAGNode {
  id: string;
  function: string;
  output_name?: string;
}

export interface DAGEdge {
  source: string;
  target: string;
  sourceOutput?: string;
  targetInput?: string;
}

export interface DAGConfig {
  name: string;
  nodes: DAGNode[];
  edges: DAGEdge[];
  params?: Record<string, any>;
}

export interface DAGExecutionResult {
  status: 'success' | 'error';
  result?: any;
  error?: string;
  dag_name: string;
}

export interface DAGValidationResult {
  status: 'valid' | 'invalid';
  dag_name: string;
  message?: string;
  error?: string;
}

export interface DAGExample {
  name: string;
  description: string;
  config: DAGConfig;
}

// ============================================================================
// Store Types
// ============================================================================

export interface StoreListResponse {
  stores: string[];
  description: Record<string, string>;
}

export interface StoreKeysResponse {
  store: string;
  keys: string[];
  count: number;
}

export interface StoreItemResponse {
  key: string;
  value?: any;
  size?: number;
  type?: string;
  path?: string;
}

// ============================================================================
// Stream Types
// ============================================================================

export interface StreamMetadata {
  source_id: string;
  sample_rate: number;
  file_path?: string;
  length_samples?: number;
  length_seconds?: number;
}

export interface StreamsResponse {
  streams: string[];
  metadata: Record<string, StreamMetadata>;
}

export interface StreamSliceData {
  source_id: string;
  bt: number;
  tt: number;
  data: number[];
  shape: number[];
  sample_rate: number;
}

export interface MultiChannelSliceResponse {
  bt: number;
  tt: number;
  channels: Record<string, StreamSliceData | { error: string }>;
}

// ============================================================================
// React Flow Types
// ============================================================================

export interface NodeData {
  label: string;
  functionName: string;
  inputs?: Record<string, any>;
  schema?: any;
}

export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: NodeData;
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}

// ============================================================================
// UI State Types
// ============================================================================

export interface AppState {
  currentView: 'store' | 'mesh' | 'stream';
  selectedStore?: string;
  selectedStreams?: string[];
}

export interface StatsResponse {
  stores: Record<string, { count: number; keys: string[] }>;
  functions: {
    count: number;
    names: string[];
  };
}
