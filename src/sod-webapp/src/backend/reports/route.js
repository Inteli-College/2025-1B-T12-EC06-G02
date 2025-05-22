import { supabase } from '@/backend/lib/supabase'
import { NextResponse } from 'next/server'

export async function GET(request) {
  const { searchParams } = new URL(request.url)
  const projectId = searchParams.get('projectId')

  let query = supabase.from('reports').select(`
    *,
    reports_images (
      image_id,
      images (
        file_path,
        file_name
      )
    )
  `)

  if (projectId) {
    query = query.eq('project_id', projectId)
  }

  const { data: reports, error } = await query

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(reports)
}

export async function POST(request) {
  const formData = await request.formData()
  const file = formData.get('file')
  const projectId = formData.get('projectId')
  const userId = formData.get('userId')
  const resultId = formData.get('resultId')
  const imageIds = JSON.parse(formData.get('imageIds') || '[]')
  
  // Upload report file to storage
  const fileName = `${userId}/${projectId}/${Date.now()}-${file.name}`
  const { data: uploadData, error: uploadError } = await supabase.storage
    .from('reports')
    .upload(fileName, file)

  if (uploadError) {
    return NextResponse.json({ error: uploadError.message }, { status: 500 })
  }

  // Create report record
  const { data: report, error: reportError } = await supabase
    .from('reports')
    .insert({
      user_id: userId,
      project_id: projectId,
      result_id: resultId,
      file_path: uploadData.path
    })
    .select()

  if (reportError) {
    return NextResponse.json({ error: reportError.message }, { status: 500 })
  }

  // Create report-image associations
  if (imageIds.length > 0) {
    const reportImages = imageIds.map(imageId => ({
      report_id: report[0].id,
      image_id: imageId
    }))

    const { error: imagesError } = await supabase
      .from('reports_images')
      .insert(reportImages)

    if (imagesError) {
      return NextResponse.json({ error: imagesError.message }, { status: 500 })
    }
  }

  return NextResponse.json(report)
}

export async function DELETE(request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  // Get report record first to get file path
  const { data: report, error: getError } = await supabase
    .from('reports')
    .select('file_path')
    .eq('id', id)
    .single()

  if (getError) {
    return NextResponse.json({ error: getError.message }, { status: 500 })
  }

  // Delete from storage
  const { error: storageError } = await supabase.storage
    .from('reports')
    .remove([report.file_path])

  if (storageError) {
    return NextResponse.json({ error: storageError.message }, { status: 500 })
  }

  // Delete database record (will cascade delete reports_images)
  const { error: dbError } = await supabase
    .from('reports')
    .delete()
    .eq('id', id)

  if (dbError) {
    return NextResponse.json({ error: dbError.message }, { status: 500 })
  }

  return NextResponse.json({ message: 'Report deleted successfully' })
}
