import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/api/client'
import { formatDate } from '@/lib/utils'
import type { Project, DocumentListResponse } from '@/types'

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()

  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => api.get<Project>(`/projects/${id}`),
    enabled: !!id,
  })

  const { data: documents } = useQuery({
    queryKey: ['documents', { projectId: id }],
    queryFn: () => api.get<DocumentListResponse>(`/documents?project_id=${id}`),
    enabled: !!id,
  })

  if (projectLoading) {
    return <div className="text-center py-8 text-muted-foreground">Loading...</div>
  }

  if (!project) {
    return <div className="text-center py-8 text-muted-foreground">Project not found</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{project.name}</h1>
        <p className="text-muted-foreground">
          {project.funding_agency || 'No funding agency'} &bull; {project.status}
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Project Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Status</label>
              <p className="capitalize">{project.status}</p>
            </div>
            {project.description && (
              <div>
                <label className="text-sm font-medium text-muted-foreground">Description</label>
                <p>{project.description}</p>
              </div>
            )}
            {project.deadline && (
              <div>
                <label className="text-sm font-medium text-muted-foreground">Deadline</label>
                <p>{formatDate(project.deadline)}</p>
              </div>
            )}
            {project.target_amount && (
              <div>
                <label className="text-sm font-medium text-muted-foreground">Target Amount</label>
                <p>${project.target_amount.toLocaleString()}</p>
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-muted-foreground">Created</label>
              <p>{formatDate(project.created_at)}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Documents</CardTitle>
            <CardDescription>
              {documents?.total ?? 0} document(s) attached
            </CardDescription>
          </CardHeader>
          <CardContent>
            {documents?.items.length === 0 ? (
              <p className="text-sm text-muted-foreground">No documents uploaded yet.</p>
            ) : (
              <ul className="space-y-2">
                {documents?.items.map((doc) => (
                  <li key={doc.id} className="flex items-center justify-between text-sm">
                    <span>{doc.original_filename}</span>
                    <span className="text-muted-foreground capitalize">{doc.processing_status}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
