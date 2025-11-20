/**
 * Store Browser Page - Phase I: Browse and manage dol stores
 */

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { Folder, File, Trash2, Plus, RefreshCw } from 'lucide-react';
import type { StoreKeysResponse } from '../types';

export function StoreBrowser() {
  const [selectedStore, setSelectedStore] = useState<string>('meshes');
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [newKey, setNewKey] = useState('');
  const [editValue, setEditValue] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const queryClient = useQueryClient();

  // Query for store list
  const { data: stores } = useQuery({
    queryKey: ['stores'],
    queryFn: () => apiClient.listStores(),
  });

  // Query for keys in selected store
  const { data: storeKeys, isLoading: keysLoading } = useQuery<StoreKeysResponse>({
    queryKey: ['store-keys', selectedStore],
    queryFn: () => apiClient.listStoreKeys(selectedStore),
    enabled: !!selectedStore,
  });

  // Query for selected item
  const { data: itemData } = useQuery({
    queryKey: ['store-item', selectedStore, selectedKey],
    queryFn: () => apiClient.getStoreItem(selectedStore, selectedKey!),
    enabled: !!selectedStore && !!selectedKey,
  });

  // Mutation for creating/updating items
  const createMutation = useMutation({
    mutationFn: ({ key, value }: { key: string; value: any }) =>
      apiClient.putStoreItem(selectedStore, key, value),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-keys', selectedStore] });
      setIsCreating(false);
      setNewKey('');
      setEditValue('');
    },
  });

  // Mutation for deleting items
  const deleteMutation = useMutation({
    mutationFn: (key: string) => apiClient.deleteStoreItem(selectedStore, key),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['store-keys', selectedStore] });
      setSelectedKey(null);
    },
  });

  const handleCreate = () => {
    if (!newKey) return;
    try {
      const value = JSON.parse(editValue);
      createMutation.mutate({ key: newKey, value });
    } catch (e) {
      alert('Invalid JSON');
    }
  };

  const handleDelete = () => {
    if (!selectedKey) return;
    if (confirm(`Delete ${selectedKey}?`)) {
      deleteMutation.mutate(selectedKey);
    }
  };

  return (
    <div className="store-browser" style={{ display: 'flex', height: '100%' }}>
      {/* Store Selection Sidebar */}
      <div className="sidebar" style={{ width: '200px', borderRight: '1px solid #e5e7eb', padding: '1rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Stores
        </h2>
        <div className="store-list">
          {stores?.stores.map((store: string) => (
            <button
              key={store}
              onClick={() => setSelectedStore(store)}
              className={selectedStore === store ? 'active' : ''}
              style={{
                width: '100%',
                textAlign: 'left',
                padding: '0.5rem',
                marginBottom: '0.25rem',
                borderRadius: '0.375rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                background: selectedStore === store ? '#3b82f6' : 'transparent',
                color: selectedStore === store ? 'white' : 'inherit',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              <Folder size={16} />
              {store}
            </button>
          ))}
        </div>

        {stores?.description && (
          <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#6b7280' }}>
            {selectedStore && stores.description[selectedStore]}
          </div>
        )}
      </div>

      {/* Keys List */}
      <div className="keys-panel" style={{ width: '250px', borderRight: '1px solid #e5e7eb', padding: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>
            Keys ({storeKeys?.count || 0})
          </h2>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={() => setIsCreating(true)}
              style={{ padding: '0.25rem', border: 'none', background: 'transparent', cursor: 'pointer' }}
              title="Create new"
            >
              <Plus size={20} />
            </button>
            <button
              onClick={() => queryClient.invalidateQueries({ queryKey: ['store-keys', selectedStore] })}
              style={{ padding: '0.25rem', border: 'none', background: 'transparent', cursor: 'pointer' }}
              title="Refresh"
            >
              <RefreshCw size={20} />
            </button>
          </div>
        </div>

        {keysLoading ? (
          <div>Loading...</div>
        ) : (
          <div className="keys-list">
            {storeKeys?.keys.map((key) => (
              <button
                key={key}
                onClick={() => setSelectedKey(key)}
                className={selectedKey === key ? 'active' : ''}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '0.5rem',
                  marginBottom: '0.25rem',
                  borderRadius: '0.375rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  background: selectedKey === key ? '#3b82f6' : 'transparent',
                  color: selectedKey === key ? 'white' : 'inherit',
                  border: 'none',
                  cursor: 'pointer',
                }}
              >
                <File size={16} />
                {key}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Content Panel */}
      <div className="content-panel" style={{ flex: 1, padding: '1rem', overflow: 'auto' }}>
        {isCreating ? (
          <div className="create-form">
            <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
              Create New Item
            </h2>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                Key:
              </label>
              <input
                type="text"
                value={newKey}
                onChange={(e) => setNewKey(e.target.value)}
                placeholder="my_item"
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                }}
              />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                Value (JSON):
              </label>
              <textarea
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                placeholder='{"key": "value"}'
                rows={10}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontFamily: 'monospace',
                }}
              />
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={handleCreate}
                disabled={createMutation.isPending}
                style={{
                  padding: '0.5rem 1rem',
                  background: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer',
                }}
              >
                {createMutation.isPending ? 'Creating...' : 'Create'}
              </button>
              <button
                onClick={() => setIsCreating(false)}
                style={{
                  padding: '0.5rem 1rem',
                  background: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer',
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : selectedKey && itemData ? (
          <div className="item-view">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{selectedKey}</h2>
              <button
                onClick={handleDelete}
                disabled={deleteMutation.isPending}
                style={{
                  padding: '0.5rem 1rem',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                }}
              >
                <Trash2 size={16} />
                {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
              </button>
            </div>

            <div
              style={{
                background: '#f3f4f6',
                padding: '1rem',
                borderRadius: '0.375rem',
                fontFamily: 'monospace',
                fontSize: '0.875rem',
                overflow: 'auto',
              }}
            >
              <pre>{JSON.stringify(itemData.value || itemData, null, 2)}</pre>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', color: '#6b7280', marginTop: '2rem' }}>
            Select an item to view its contents
          </div>
        )}
      </div>
    </div>
  );
}
