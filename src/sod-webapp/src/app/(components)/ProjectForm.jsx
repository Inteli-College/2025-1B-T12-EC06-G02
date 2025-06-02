'use client'

import { createProject } from '@/app/actions'
import { useState } from 'react'

export default function ProjectForm() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(formData) {
    try {
      setLoading(true)
      setError(null)
      await createProject(formData)
      // Reset form
      formData.target.reset()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form action={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Nome do Projeto
        </label>
        <input
          type="text"
          name="name"
          id="name"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[#2d608d] focus:ring-[#2d608d]"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Descrição
        </label>
        <textarea
          name="description"
          id="description"
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[#2d608d] focus:ring-[#2d608d]"
        />
      </div>

      <div>
        <label htmlFor="address" className="block text-sm font-medium text-gray-700">
          Endereço
        </label>
        <input
          type="text"
          name="address"
          id="address"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[#2d608d] focus:ring-[#2d608d]"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-[#2d608d] text-white px-4 py-2 rounded hover:bg-[#245179] transition-colors disabled:opacity-50"
      >
        {loading ? 'Criando...' : 'Criar Projeto'}
      </button>
    </form>
  )
}
