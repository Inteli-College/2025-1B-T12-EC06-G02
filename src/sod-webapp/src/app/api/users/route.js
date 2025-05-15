import { supabase } from '@/lib/supabase'
import { NextResponse } from 'next/server'

export async function GET(request) {
  const { data: users, error } = await supabase
    .from('users')
    .select('*')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(users)
}

export async function PUT(request) {
  const body = await request.json()
  const { id, ...updateData } = body

  const { data, error } = await supabase
    .from('users')
    .update(updateData)
    .eq('id', id)
    .select()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}
