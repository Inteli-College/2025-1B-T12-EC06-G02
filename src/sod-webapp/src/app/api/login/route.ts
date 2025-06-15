import { serialize } from 'cookie';
import { NextResponse } from 'next/server';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export async function POST(req: Request) {
  try {
    if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
      console.error('Missing Supabase environment variables');
      return NextResponse.json(
        { error: 'Configuration error' },
        { status: 500 }
      );
    }

    const { email, password } = await req.json();

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

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
  // Cria uma resposta com os cookies
  const res = NextResponse.json({
    message: 'Login com sucesso',
    session: {
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      user: data.user
    }
  });
  
  // Adiciona os cookies
  res.headers.append('Set-Cookie', accessToken);
  res.headers.append('Set-Cookie', refreshToken);
  
  return res;
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'An error occurred during login' },
      { status: 500 }
    );
  }
}
