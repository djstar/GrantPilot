// Project types
export type ProjectStatus = 'draft' | 'active' | 'submitted' | 'funded' | 'archived'

export interface Project {
  id: string
  name: string
  description?: string
  status: ProjectStatus
  funding_agency?: string
  deadline?: string
  target_amount?: number
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
  funding_agency?: string
  deadline?: string
  target_amount?: number
}

export interface ProjectUpdate {
  name?: string
  description?: string
  status?: ProjectStatus
  funding_agency?: string
  deadline?: string
  target_amount?: number
}

export interface ProjectListResponse {
  items: Project[]
  total: number
}

// Document types
export type DocumentType =
  | 'grant_proposal'
  | 'rfa'
  | 'budget'
  | 'biosketch'
  | 'letter_of_support'
  | 'research_paper'
  | 'preliminary_data'
  | 'reviewer_feedback'
  | 'other'

export type ProcessingStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface Document {
  id: string
  project_id?: string
  filename: string
  original_filename: string
  file_size: number
  mime_type: string
  document_type: DocumentType
  document_type_confidence?: number
  processing_status: ProcessingStatus
  processing_error?: string
  page_count?: number
  word_count?: number
  version: number
  created_at: string
  updated_at: string
}

export interface DocumentListResponse {
  items: Document[]
  total: number
}

// API response types
export interface HealthResponse {
  status: string
  version: string
  database: string
}
