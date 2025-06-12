// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  // Verifica tanto o token de acesso quanto o de refresh
  const accessToken = request.cookies.get('sb-access-token')?.value;
  const refreshToken = request.cookies.get('sb-refresh-token')?.value;

  // Se não houver nenhum dos tokens, redireciona para o login
  if (!accessToken && !refreshToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Se estiver na página de login com tokens válidos, redireciona para home
  if (request.nextUrl.pathname === '/login' && accessToken && refreshToken) {
    return NextResponse.redirect(new URL('/home', request.url));
  }

  return NextResponse.next();
}

// Defina as rotas protegidas
export const config = {
  matcher: [
    '/home',
    '/results',
    '/history',
    '/upload',
  ],
};