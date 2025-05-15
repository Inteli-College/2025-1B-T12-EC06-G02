import { Inter } from 'next/font/google'
import { AuthProvider } from '@/lib/auth-client'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'SOD - Sistema de Observação de Deformação',
  description: 'Sistema de análise de deformações estruturais',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
