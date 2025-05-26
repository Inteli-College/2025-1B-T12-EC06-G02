import { supabase } from '@/backend/lib/supabase'
import { NextResponse } from 'next/server'

export async function GET(request) {
  const { searchParams } = new URL(request.url)
  const projectId = searchParams.get('projectId')

  let query = supabase.from('images').select('*')
  if (projectId) {
    query = query.eq('project_id', projectId)
  }

  const { data: images, error } = await query

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(images)
}

export async function POST(request) {
  const formData = await request.formData()
  const file = formData.get('file')
  const projectId = formData.get('projectId')
  const userId = formData.get('userId')
  const metadata = JSON.parse(formData.get('metadata') || '{}')
  
  // Upload file to storage
  const fileName = `${userId}/${projectId}/${Date.now()}-${file.name}`
  const { data: uploadData, error: uploadError } = await supabase.storage
    .from('crack_images')
    .upload(fileName, file)

  if (uploadError) {
    return NextResponse.json({ error: uploadError.message }, { status: 500 })
  }

  // Create database record
  const { data: imageRecord, error: dbError } = await supabase
    .from('images')
    .insert({
      user_id: userId,
      project_id: projectId,
      file_path: uploadData.path,
      file_name: file.name,
      type: file.type,
      size_kb: Math.round(file.size / 1024),
      metadata,
      axis: metadata.axis,
      floor: metadata.floor
    })
    .select()

  if (dbError) {
    return NextResponse.json({ error: dbError.message }, { status: 500 })
  }

  return NextResponse.json(imageRecord)
}

export async function DELETE(request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  // Get image record first to get file path
  const { data: image, error: getError } = await supabase
    .from('images')
    .select('file_path')
    .eq('id', id)
    .single()

  if (getError) {
    return NextResponse.json({ error: getError.message }, { status: 500 })
  }

  // Delete from storage
  const { error: storageError } = await supabase.storage
    .from('crack_images')
    .remove([image.file_path])

  if (storageError) {
    return NextResponse.json({ error: storageError.message }, { status: 500 })
  }

  // Delete database record
  const { error: dbError } = await supabase
    .from('images')
    .delete()
    .eq('id', id)

  if (dbError) {
    return NextResponse.json({ error: dbError.message }, { status: 500 })
  }

  return NextResponse.json({ message: 'Image deleted successfully' })
}
