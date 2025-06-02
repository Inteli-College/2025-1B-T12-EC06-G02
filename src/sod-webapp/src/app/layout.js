import { Inter } from 'next/font/google'
import { AuthProvider } from '../backend/lib/auth-client'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'SOD - Sistema Óptico de Detecção',
  description: 'Sistema de análise de deformações estruturais',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <AuthProvider>
          <div id="modal-root"></div>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
