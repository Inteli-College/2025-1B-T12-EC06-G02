import { supabase } from './supabase'

export class ApiService {
  // Auth
  static async signIn(email, password) {
    return supabase.auth.signInWithPassword({ email, password })
  }
  static async signUp(email, password, name) {
    return supabase.auth.signUp({
      email,
      password,
      options: { data: { name } },
    })
  }
  static async signOut() {
    return supabase.auth.signOut()
  }

  static async getProjects() {
    return supabase
      .from('projects')
      .select('*')
      .order('created_at', { ascending: false })
  }
  static async getProject(id) {
    return supabase.from('projects').select('*').eq('id', id).single()
  }
  static async createProject(data) {
    return supabase.from('projects').insert([data]).select()
  }
  static async updateProject(id, data) {
    return supabase.from('projects').update(data).eq('id', id).select()
  }
  static async deleteProject(id) {
    return supabase.from('projects').delete().eq('id', id)
  }
}
