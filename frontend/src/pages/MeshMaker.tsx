/**
 * Mesh Maker Page - Phase II: Visual DAG composition with React Flow
 */

import { useState, useCallback, useMemo } from 'react';
import {
  ReactFlow,
  Node,
  Edge,
  addEdge,
  Background,
  Controls,
  MiniMap,
  Connection,
  useNodesState,
  useEdgesState,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { Play, Save, FileJson } from 'lucide-react';
import Form from '@rjsf/core';
import validator from '@rjsf/validator-ajv8';
import type { DAGConfig, NodeData } from '../types';

// Custom node component
function FunctionNode({ data }: { data: NodeData }) {
  return (
    <div
      style={{
        padding: '10px 20px',
        borderRadius: '8px',
        border: '2px solid #3b82f6',
        background: 'white',
        minWidth: '150px',
      }}
    >
      <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>{data.label}</div>
      <div style={{ fontSize: '12px', color: '#6b7280' }}>{data.functionName}</div>
    </div>
  );
}

const nodeTypes = {
  functionNode: FunctionNode,
};

export function MeshMaker() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [dagName, setDagName] = useState('my_dag');
  const [executionInputs, setExecutionInputs] = useState<string>('{}');
  const [executionResult, setExecutionResult] = useState<any>(null);

  // Query for available functions
  const { data: functionsData } = useQuery({
    queryKey: ['functions'],
    queryFn: () => apiClient.listFunctions(),
  });

  // Query for function schema when node is selected
  const { data: nodeSchema } = useQuery({
    queryKey: ['function-schema', selectedNode?.data.functionName],
    queryFn: () => apiClient.getFunctionSchema(selectedNode!.data.functionName),
    enabled: !!selectedNode?.data.functionName,
  });

  // Execute DAG mutation
  const executeMutation = useMutation({
    mutationFn: ({ config, inputs }: { config: DAGConfig; inputs: any }) =>
      apiClient.executeDAG(config, inputs),
    onSuccess: (data) => {
      setExecutionResult(data);
    },
  });

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  const addFunctionNode = (functionName: string) => {
    const newNode: Node = {
      id: `${functionName}_${Date.now()}`,
      type: 'functionNode',
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: {
        label: functionName,
        functionName,
        inputs: {},
      },
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const buildDAGConfig = (): DAGConfig => {
    return {
      name: dagName,
      nodes: nodes.map((node) => ({
        id: node.id,
        function: node.data.functionName,
      })),
      edges: edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
        sourceOutput: edge.source,
        targetInput: edge.targetHandle || 'value',
      })),
    };
  };

  const handleExecute = () => {
    try {
      const inputs = JSON.parse(executionInputs);
      const config = buildDAGConfig();
      executeMutation.mutate({ config, inputs });
    } catch (e) {
      alert('Invalid JSON inputs');
    }
  };

  const handleSave = async () => {
    const config = buildDAGConfig();
    try {
      await apiClient.putStoreItem('meshes', dagName, config);
      alert(`DAG "${dagName}" saved successfully!`);
    } catch (e) {
      alert('Failed to save DAG');
    }
  };

  const handleNodeConfigUpdate = (formData: any) => {
    if (!selectedNode) return;
    setNodes((nds) =>
      nds.map((node) =>
        node.id === selectedNode.id
          ? { ...node, data: { ...node.data, inputs: formData } }
          : node
      )
    );
  };

  return (
    <div className="mesh-maker" style={{ display: 'flex', height: '100%' }}>
      {/* Function Palette */}
      <div
        className="function-palette"
        style={{
          width: '200px',
          borderRight: '1px solid #e5e7eb',
          padding: '1rem',
          overflow: 'auto',
        }}
      >
        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Functions
        </h2>
        <div>
          {functionsData?.functions.map((funcName: string) => (
            <button
              key={funcName}
              onClick={() => addFunctionNode(funcName)}
              style={{
                width: '100%',
                textAlign: 'left',
                padding: '0.5rem',
                marginBottom: '0.25rem',
                borderRadius: '0.375rem',
                background: '#f3f4f6',
                border: '1px solid #d1d5db',
                cursor: 'pointer',
              }}
            >
              {funcName}
            </button>
          ))}
        </div>
      </div>

      {/* Canvas */}
      <div className="canvas-container" style={{ flex: 1, position: 'relative' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
          <Panel position="top-left">
            <div
              style={{
                background: 'white',
                padding: '1rem',
                borderRadius: '0.5rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              }}
            >
              <div style={{ marginBottom: '0.5rem' }}>
                <input
                  type="text"
                  value={dagName}
                  onChange={(e) => setDagName(e.target.value)}
                  placeholder="DAG name"
                  style={{
                    padding: '0.5rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                    marginRight: '0.5rem',
                  }}
                />
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={handleSave}
                  style={{
                    padding: '0.5rem 1rem',
                    background: '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}
                >
                  <Save size={16} />
                  Save
                </button>
                <button
                  onClick={handleExecute}
                  disabled={executeMutation.isPending}
                  style={{
                    padding: '0.5rem 1rem',
                    background: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}
                >
                  <Play size={16} />
                  {executeMutation.isPending ? 'Running...' : 'Execute'}
                </button>
              </div>
            </div>
          </Panel>
        </ReactFlow>
      </div>

      {/* Configuration Panel */}
      <div
        className="config-panel"
        style={{
          width: '300px',
          borderLeft: '1px solid #e5e7eb',
          padding: '1rem',
          overflow: 'auto',
        }}
      >
        {selectedNode ? (
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
              Configure: {selectedNode.data.label}
            </h2>

            {nodeSchema && (
              <Form
                schema={nodeSchema}
                formData={selectedNode.data.inputs || {}}
                validator={validator}
                onChange={(e) => handleNodeConfigUpdate(e.formData)}
                onSubmit={(e) => handleNodeConfigUpdate(e.formData)}
              >
                <button type="submit" style={{ display: 'none' }}>
                  Submit
                </button>
              </Form>
            )}
          </div>
        ) : (
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
              Execution
            </h2>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                Inputs (JSON):
              </label>
              <textarea
                value={executionInputs}
                onChange={(e) => setExecutionInputs(e.target.value)}
                placeholder='{"node_id": {"param": "value"}}'
                rows={8}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                }}
              />
            </div>

            {executionResult && (
              <div>
                <h3 style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Result:</h3>
                <div
                  style={{
                    background: executionResult.status === 'success' ? '#d1fae5' : '#fee2e2',
                    padding: '0.75rem',
                    borderRadius: '0.375rem',
                    fontFamily: 'monospace',
                    fontSize: '0.875rem',
                  }}
                >
                  <pre>{JSON.stringify(executionResult, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
