import { supabase } from '@/lib/supabase'
import { NextResponse } from 'next/server'

export async function GET(request) {
  const { searchParams } = new URL(request.url)
  const projectId = searchParams.get('projectId')

  const { data: results, error } = await supabase
    .from('results')
    .select(`
      *,
      project_results!inner (
        project_id
      )
    `)
    .eq('project_results.project_id', projectId)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(results)
}

export async function POST(request) {
  const body = await request.json()
  const { projectId, ...resultData } = body

  // Create result record
  const { data: result, error: resultError } = await supabase
    .from('results')
    .insert(resultData)
    .select()

  if (resultError) {
    return NextResponse.json({ error: resultError.message }, { status: 500 })
  }

  // Create project-result association
  const { error: projResultError } = await supabase
    .from('project_results')
    .insert({
      project_id: projectId,
      result_id: result[0].id
    })

  if (projResultError) {
    return NextResponse.json({ error: projResultError.message }, { status: 500 })
  }

  return NextResponse.json(result)
}
