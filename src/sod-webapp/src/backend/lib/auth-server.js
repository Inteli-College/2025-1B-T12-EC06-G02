import { cookies } from 'next/headers'
import { createClient } from '@/utils/supabase/server'

export async function getSession() {
  const cookieStore = cookies()
  const supabase = createClient(cookieStore)
  const { data: { session } } = await supabase.auth.getSession()
  return session
}

export async function signOut() {
  const cookieStore = cookies()
  const supabase = createClient(cookieStore)
  await supabase.auth.signOut()
}

export async function getUserProfile() {
  const session = await getSession()
  if (!session?.user) {
    return null
  }

  const cookieStore = cookies()
  const supabase = createClient(cookieStore)
  const { data: profile, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', session.user.id)
    .single()

  if (error || !profile) {
    return null
  }

  return profile
}
