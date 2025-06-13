import { jwtVerify } from 'jose';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const SUPABASE_JWT_SECRET = process.env.SUPABASE_JWT_SECRET;

if (!SUPABASE_JWT_SECRET) {
  throw new Error('SUPABASE_JWT_SECRET não está definida no .env');
}

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('sb-access-token')?.value;

  const isLoginPage = request.nextUrl.pathname === '/login';

  if (!token) {
    // Se está tentando acessar a página de login e não tem token, deixa passar
    if (isLoginPage) {
      return NextResponse.next();
    }

    return new NextResponse(JSON.stringify({ error: 'Não autorizado: faça login na plataforma' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const encoder = new TextEncoder();
    const { payload } = await jwtVerify(token, encoder.encode(SUPABASE_JWT_SECRET), {
      issuer: `${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1`,
    });

    // Se já está logado e tentando acessar o login, redireciona para a home
    if (isLoginPage) {
      return NextResponse.redirect(new URL('/home', request.url));
    }

    // Token válido, segue normalmente
    return NextResponse.next();
  } catch (err) {
    console.error('Token inválido ou expirado:', err);

    // Mesmo com token inválido, pode acessar o login
    if (isLoginPage) {
      return NextResponse.next();
    }

    return new NextResponse(JSON.stringify({ error: 'Não autorizado: faça login na plataforma' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export const config = {
  matcher: [
    '/home',
    '/results',
    '/history',
    '/upload',
    '/login', // Adicione o /login para interceptar também
  ],
};
