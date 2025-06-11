// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify, createRemoteJWKSet } from 'jose';

const JWKS = createRemoteJWKSet(
  new URL(`${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1/.well-known/jwks.json`)
);

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('sb-access-token')?.value;

  if (!token) {
    return new NextResponse(JSON.stringify({ error: 'Unauthorized: token not found' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    await jwtVerify(token, JWKS, {
      issuer: `${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1`,
    });

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
  matcher: [
    '/home',
    '/results',
    '/history',
    '/upload',
  ],
}
