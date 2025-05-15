'use client'

import { useState, useEffect } from 'react'
import Image from "next/image"
import Link from "next/link"
import { useRouter, useSearchParams } from 'next/navigation'
import { supabase } from '../../lib/supabase'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams();
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showInvalidLink, setShowInvalidLink] = useState(false);

  const code = searchParams.get('code');
  const accessToken = searchParams.get('access_token');
  // const hasToken = !!(code || accessToken); // Removed hasToken

  useEffect(() => {
    async function handleCodeExchange() {
      const { data: userData } = await supabase.auth.getUser();
      if (!userData?.user && code) {
        // Exchange code for session only if not authenticated
        const { error } = await supabase.auth.exchangeCodeForSession(code);
        if (error) {
          setShowInvalidLink(true);
          setTimeout(() => {
            setShowInvalidLink(false);
            router.replace('/login');
          }, 8000);
          return;
        }
      }
      // If neither code nor access_token, show invalid link page for 8s then redirect
      if (!code && !accessToken) {
        setShowInvalidLink(true);
        setTimeout(() => {
          setShowInvalidLink(false);
          router.replace('/login');
        }, 8000);
        return;
      }
    }
    handleCodeExchange();
  }, [router, code, accessToken]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    if (password !== confirmPassword) {
      setError("As senhas não coincidem.");
      setIsLoading(false);
      return;
    }

    try {
      const { error } = await supabase.auth.updateUser({
        password,
      })

      if (error) {
        throw error
      }

      router.push('/login')
      router.refresh()
    } catch (error) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  if (showInvalidLink) {
    return (
      <main className="relative min-h-screen w-full flex items-center justify-center p-4">
        <div className="w-full max-w-md bg-white/80 backdrop-blur-sm p-8 md:p-12 rounded shadow-lg text-center">
          <h2 className="text-2xl font-medium mb-4 text-[#434343]">Link inválido ou expirado</h2>
          <p className="mb-6 text-gray-700">O link de redefinição de senha é inválido, expirou ou já foi utilizado.</p>
          <Link href="/forgot-password" className="inline-block px-8 py-3 bg-[#2d608d] text-white text-lg font-medium rounded hover:bg-[#245179] transition-colors">
            Solicitar novo link
          </Link>
        </div>
      </main>
    );
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
            Atualize sua
            <br />
            senha
          </h1>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                placeholder="Nova senha"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400 pr-12"
                required
                disabled={isLoading}
                value={password}
                onChange={e => setPassword(e.target.value)}
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

            <div className="relative">
              <input
                name="confirmPassword"
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Confirme a nova senha"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400 pr-12"
                required
                disabled={isLoading}
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                tabIndex={-1}
                onClick={() => setShowConfirmPassword(v => !v)}
                aria-label={showConfirmPassword ? 'Ocultar senha' : 'Ver senha'}
              >
                {showConfirmPassword ? (
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
              {isLoading ? 'Atualizando...' : 'Atualizar'}
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
              Criar nova conta
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
