/**
 * API client for app_meshed backend
 */

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class AppMeshedClient {
  private client: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // ============================================================================
  // Store API
  // ============================================================================

  async listStores() {
    const { data } = await this.client.get('/store/list');
    return data;
  }

  async listStoreKeys(storeName: string) {
    const { data } = await this.client.get(`/store/${storeName}/keys`);
    return data;
  }

  async getStoreItem(storeName: string, key: string) {
    const { data } = await this.client.get(`/store/${storeName}/${key}`);
    return data;
  }

  async putStoreItem(storeName: string, key: string, value: any) {
    const { data } = await this.client.put(`/store/${storeName}/${key}`, value);
    return data;
  }

  async deleteStoreItem(storeName: string, key: string) {
    const { data } = await this.client.delete(`/store/${storeName}/${key}`);
    return data;
  }

  // ============================================================================
  // Function API
  // ============================================================================

  async listFunctions() {
    const { data } = await this.client.get('/functions');
    return data;
  }

  async getFunctionMetadata(functionName: string) {
    const { data } = await this.client.get(`/functions/${functionName}/metadata`);
    return data;
  }

  // ============================================================================
  // Schema API
  // ============================================================================

  async getFunctionSchema(functionName: string) {
    const { data } = await this.client.get(`/schema/function/${functionName}`);
    return data;
  }

  async getObjectSchema(obj: any, title?: string) {
    const { data } = await this.client.post('/schema/object', { obj, title });
    return data;
  }

  async getDagConfigSchema() {
    const { data } = await this.client.get('/schema/dag-config');
    return data;
  }

  // ============================================================================
  // DAG API
  // ============================================================================

  async executeDAG(dagConfig: any, inputs: any) {
    const { data } = await this.client.post('/dag/execute', {
      dag_config: dagConfig,
      inputs,
    });
    return data;
  }

  async validateDAG(dagConfig: any) {
    const { data } = await this.client.post('/dag/validate', dagConfig);
    return data;
  }

  async getDagExamples() {
    const { data } = await this.client.get('/dag/examples');
    return data;
  }

  // ============================================================================
  // Stream API
  // ============================================================================

  async listStreams() {
    const { data } = await this.client.get('/streams');
    return data;
  }

  async getStreamMetadata(sourceId: string) {
    const { data } = await this.client.get(`/streams/${sourceId}/metadata`);
    return data;
  }

  async sliceStream(sourceId: string, bt: number, tt: number) {
    const { data } = await this.client.get(`/streams/${sourceId}/slice`, {
      params: { bt, tt },
    });
    return data;
  }

  async sliceMultiChannel(channelIds: string[], bt: number, tt: number) {
    const { data } = await this.client.post('/streams/multi-channel/slice', {
      channel_ids: channelIds,
      bt,
      tt,
    });
    return data;
  }

  async getMultiChannelInfo(channelIds: string[]) {
    const { data } = await this.client.post('/streams/multi-channel/info', {
      channel_ids: channelIds,
    });
    return data;
  }

  // ============================================================================
  // Utility API
  // ============================================================================

  async getStats() {
    const { data } = await this.client.get('/stats');
    return data;
  }

  async getHealth() {
    const { data } = await this.client.get('/health');
    return data;
  }
}

export const apiClient = new AppMeshedClient();
export default AppMeshedClient;
