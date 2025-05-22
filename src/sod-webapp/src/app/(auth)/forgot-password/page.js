'use client'

import { useState } from 'react'
import Image from "next/image"
import Link from "next/link"
import { useRouter } from 'next/navigation'
import { supabase } from '../../../backend/lib/supabase'

export default function LoginPage() {
  const router = useRouter()
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email')

    try {
       const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: 'http://localhost:3000/update-password'
      })

      if (error) {
        throw error
      }

    } catch (error) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="relative min-h-screen w-full">
      {/* Background Image with Filter */}
      <div className="absolute inset-0 -z-10">
        <div className="relative w-full h-full">
          <Image
            src="/cityscape-background.png"
            alt="Cityscape background"
            fill
            quality={100}
            priority
            className="object-cover brightness-90"
          />
        </div>
      </div>

      {/* Content Container */}
      <div className="relative min-h-screen w-full flex items-center justify-center p-4">
        {/* Semi-transparent Login Card */}
        <div className="w-full max-w-md bg-white/80 backdrop-blur-sm p-8 md:p-12 rounded shadow-lg">
          <h1 className="text-[#434343] text-4xl md:text-5xl font-medium mb-8 leading-tight">
            Esqueci a
            <br />
            minha senha
          </h1>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                name="email"
                type="email"
                placeholder="E-mail"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400"
                required
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              className="w-full p-4 bg-[#2d608d] text-white text-xl font-medium rounded hover:bg-[#245179] transition-colors disabled:opacity-50"
              disabled={isLoading}
            >
              {isLoading ? 'Enviando...' : 'Recuperar'}
            </button>
          </form>
          

          <div className="mt-4 text-center">
            <Link href="/login" className="text-[#2d608d] hover:underline">
              Já tem uma conta?
            </Link>
          </div>

          <div className="my-6 border-t border-gray-300"></div>

          <div className="text-center">
            <Link
              href="/signup"
              className="inline-block px-12 py-4 bg-[#00c939] text-white text-xl font-medium rounded hover:bg-[#00b033] transition-colors"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
