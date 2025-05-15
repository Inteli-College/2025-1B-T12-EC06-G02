import React from 'react';
import AuthGuard from '../../../components/AuthGuard';

export default function ResultDetailsPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Detalhes do Resultado</h1>
      </div>
    </AuthGuard>
  );
}