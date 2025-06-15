export interface DataProvider {
  id: string
  name: string
  description: string
  logoUrl?: string
  color: string
  website?: string
  enabled: boolean
}

export interface Dataset {
  codigo: string
  nombre: string
  cod_ioe?: string
  url?: string
  provider?: string // Optional since API doesn't return this
  category?: string
  lastUpdated?: string
}

export interface ProviderStats {
  totalDatasets: number
  categories: string[]
  lastSync?: string
}

export interface RawDataResponse {
  codigo: string
  dataset_name: string
  record_count: number
  raw_data: any[]
  message?: string
}
