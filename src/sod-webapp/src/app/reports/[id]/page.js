import React from 'react';
import AuthGuard from '../../../components/AuthGuard';

export default function ReportDetailsPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Detalhes do Relatório</h1>
      </div>
    </AuthGuard>
  );
}