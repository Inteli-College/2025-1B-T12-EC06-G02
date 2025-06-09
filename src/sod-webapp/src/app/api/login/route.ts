import { serialize } from 'cookie';
import { NextResponse } from 'next/server';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export async function POST(req: Request) {
  const { email, password } = await req.json();

  // Chamada direta à API REST de autenticação do Supabase
  const response = await fetch(`${SUPABASE_URL}/auth/v1/token?grant_type=password`, {
    method: 'POST',
    headers: {
      'apikey': SUPABASE_ANON_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    return NextResponse.json({ error: data.error_description || data.error || 'Login inválido' }, { status: 401 });
  }

  // Cria cookies HTTP only com os tokens
  const accessToken = serialize('sb-access-token', data.access_token, {
    httpOnly: true,
    path: '/',
    maxAge: 60 * 60 * 24 * 7,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
  });

  const refreshToken = serialize('sb-refresh-token', data.refresh_token, {
    httpOnly: true,
    path: '/',
    maxAge: 60 * 60 * 24 * 30,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
  });

  const res = NextResponse.json({ message: 'Login com sucesso' });
  res.headers.append('Set-Cookie', accessToken);
  res.headers.append('Set-Cookie', refreshToken);

  return res;
}
