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
  external_id: string
  name: string
  dataset_name?: string
  id?: string
}

export interface ProviderStats {
  totalDatasets: number
  categories: string[]
  lastSync?: string
}

export interface RawDataResponse {
  code: string
  dataset_name: string
  record_count: number
  raw_data: any[]
  message?: string
}
