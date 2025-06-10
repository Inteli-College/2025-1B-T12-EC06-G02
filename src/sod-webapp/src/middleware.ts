// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('sb-access-token')?.value;

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
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