import { jwtVerify } from 'jose';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const SUPABASE_JWT_SECRET = process.env.SUPABASE_JWT_SECRET;

if (!SUPABASE_JWT_SECRET) {
  throw new Error('SUPABASE_JWT_SECRET não está definida no .env');
}

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('sb-access-token')?.value;

  if (!token) {
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

    // (Opcional) Você pode acessar payload.role, payload.email, etc.
    return NextResponse.next();
  } catch (err) {
    console.error('Token inválido ou expirado:', err);
    return new NextResponse(JSON.stringify({ error: 'Unauthorized: invalid or expired token' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export const config = {
  matcher: ['/home', '/results', '/history', '/upload'],
};
