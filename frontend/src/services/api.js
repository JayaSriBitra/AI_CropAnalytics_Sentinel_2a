const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const demoDashboard = {
  health: { status: 'demo' },
  summary: { area: 1248, areaUnit: 'ha', health: 78, yield: 5.8, yieldUnit: 't/ha', change: 12.4 },
  ndvi: [0.42, 0.47, 0.51, 0.48, 0.59, 0.64, 0.61, 0.69, 0.73, 0.71, 0.78, 0.76],
  classes: [
    { label: 'Healthy crop', value: 58, color: '#356859' },
    { label: 'Stressed crop', value: 24, color: '#d88b42' },
    { label: 'Bare soil', value: 11, color: '#b7a785' },
    { label: 'Water / other', value: 7, color: '#6f9db3' },
  ],
};

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { Accept: 'application/json', ...options.headers },
  });
  if (!response.ok) throw new Error(`API request failed (${response.status})`);
  return response.json();
}

export async function getDashboardData(signal) {
  try {
    const [health, statistics] = await Promise.all([
      request('/api/v1/health', { signal }),
      request('/api/v1/statistics', { signal }),
    ]);
    return { ...demoDashboard, health, ...statistics, source: 'api' };
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    return { ...demoDashboard, source: 'demo' };
  }
}

export async function uploadPrediction(file) {
  const body = new FormData();
  body.append('file', file);
  return request('/api/v1/predictions', { method: 'POST', body, headers: {} });
}

export async function createReport(analysisId) {
  return request('/api/v1/reports', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ analysis_id: analysisId, format: 'PDF' }),
  });
}