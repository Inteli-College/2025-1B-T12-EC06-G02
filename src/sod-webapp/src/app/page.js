import { cookies } from 'next/headers'
import { supabase } from '../backend/lib/supabase'
import { redirect } from 'next/navigation'

export default async function Home() {
  // Não é possível usar cookies e supabase client do lado do servidor neste projeto, pois o supabase importado é client-side.
  // Portanto, apenas redireciona para login.
  redirect('/login')
}