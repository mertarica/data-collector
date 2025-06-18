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
  status: string
  dataset_info: {
    table_id: string
    dataset_code: string
    dataset_name: string
    source: string
    data_type: string
  }
  processing_summary: {
    total_series: number
    total_data_points: number
    data_type_distribution: Record<string, number>
    period_distribution: Record<string, number>
    metadata_enriched: boolean
  }
  processed_data: any[]
  record_count: number
  retrieved_at: string
  metadata_version: string
}

class ApiService {
  private baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/'

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`

        try {
          const errorData = await response.json()
          if (errorData.detail) {
            errorMessage = errorData.detail
          }
        } catch {
          // If response is not JSON (like HTML error page)
          const textContent = await response.text()
          if (textContent.includes('<!DOCTYPE html>')) {
            errorMessage = `API returned HTML error page (${response.status}). The requested dataset might not exist or the API endpoint is incorrect.`
          }
        }

        throw new Error(errorMessage)
      }

      return response.json()
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(
          'Unable to connect to the API. Please check if the backend service is running.',
        )
      }
      throw error
    }
  }

  async getDatasets(): Promise<Dataset[]> {
    return this.request<Dataset[]>(`v1/datasets`)
  }

  async searchDatasets(query: string): Promise<Dataset[]> {
    return this.request<Dataset[]>(`v1/datasets/search?q=${encodeURIComponent(query)}`)
  }

  async getDatasetInfo(code: string): Promise<Dataset> {
    return this.request<Dataset>(`v1/datasets/${code}`)
  }

  async getRawData(code: string): Promise<RawDataResponse> {
    return this.request<RawDataResponse>(`v1/data/raw/${code}`)
  }

  async getProcessedData(code: string): Promise<ProcessedDataResponse> {
    return this.request<ProcessedDataResponse>(`v1/data/processed/${code}`)
  }

  async getProviderInfo(code: string): Promise<any> {
    return this.request<any>(`v1/data/info/${code}`)
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.request<{ status: string; service: string }>(`/health`)
  }
}

export const apiService = new ApiService()
