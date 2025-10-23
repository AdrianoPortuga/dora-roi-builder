// src/services/system.ts
import api from './api';

export type Health = {
  status: 'ok' | string;
  version: string;
  env: string;
};

export async function getHealth(): Promise<Health> {
  const { data } = await api.get('/health');
  return data;
}
