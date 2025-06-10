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
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email')
    const password = formData.get('password')

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) {
        throw error
      }

      // Atualiza o last_login na tabela users
      if (data && data.user && data.user.id) {
        await import('../../../backend/lib/api-service').then(({ ApiService }) =>
          ApiService.updateLastLogin(data.user.id)
        );
      }

      router.push('/home')
      router.refresh()
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
            Sistema Óptico
            <br />
            de Detecção
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
            <div className="relative">
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                placeholder="Senha"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400 pr-12"
                required
                disabled={isLoading}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                tabIndex={-1}
                onClick={() => setShowPassword(v => !v)}
                aria-label={showPassword ? 'Ocultar senha' : 'Ver senha'}
              >
                {showPassword ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-5.523 0-10-4.477-10-10 0-1.657.336-3.234.938-4.675M15 12a3 3 0 11-6 0 3 3 0 016 0zm6.062-4.675A9.956 9.956 0 0122 9c0 5.523-4.477 10-10 10a9.956 9.956 0 01-4.675-.938M3 3l18 18" /></svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0zm7-2s-3-5-10-5S2 10 2 10s3 5 10 5 10-5 10-5z" /></svg>
                )}
              </button>
            </div>

            <button
              type="submit"
              className="w-full p-4 bg-[#2d608d] text-white text-xl font-medium rounded hover:bg-[#245179] transition-colors disabled:opacity-50"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"               viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></              circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                  </svg>
                  <span>Entrando...</span>
                </div>
              ) : 'Login'}        
              </button>
          </form>

          <div className="mt-4 text-center">
            <Link href="/forgot-password" className="text-[#2d608d] hover:underline">
              Esqueci minha senha
            </Link>
          </div>

          <div className="my-6 border-t border-gray-300"></div>

          <div className="text-center">
            <Link
              href="/signup"
              className="inline-block px-12 py-4 bg-[#204565] text-white text-xl font-medium rounded hover:bg-[#19354F] transition-colors"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
