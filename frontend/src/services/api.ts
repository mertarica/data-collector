export interface Dataset {
  codigo: string
  nombre: string
  cod_ioe?: string
  url?: string
}

export interface RawDataResponse {
  codigo: string
  dataset_name: string
  record_count: number
  raw_data: any[]
  message?: string
}

export interface ProcessedDataResponse {
  codigo: string
  dataset_name: string
  record_count: number
  processed_data: any[]
  columns: string[]
  message?: string
}

class ApiService {
  private baseURL = 'http://localhost:8000/api/v1'

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  async getDatasets(): Promise<Dataset[]> {
    return this.request<Dataset[]>(`/datasets`)
  }

  async searchDatasets(query: string, limit: number = 20): Promise<Dataset[]> {
    return this.request<Dataset[]>(`/datasets/search?q=${encodeURIComponent(query)}&limit=${limit}`)
  }

  async getDatasetInfo(code: string): Promise<Dataset> {
    return this.request<Dataset>(`/datasets/${code}`)
  }

  async getRawData(code: string): Promise<RawDataResponse> {
    return this.request<RawDataResponse>(`/data/raw/${code}`)
  }

  async getProcessedData(code: string): Promise<ProcessedDataResponse> {
    return this.request<ProcessedDataResponse>(`/data/processed/${code}`)
  }

  async getProviderInfo(code: string): Promise<any> {
    return this.request<any>(`/data/info/${code}`)
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.request<{ status: string; service: string }>(`/health`)
  }
}

export const apiService = new ApiService()
