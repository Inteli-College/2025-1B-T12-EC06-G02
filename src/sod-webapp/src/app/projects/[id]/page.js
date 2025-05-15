import React from 'react';
import AuthGuard from '../../../components/AuthGuard';

export default function ProjectDetailsPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Detalhes do Projeto</h1>
      </div>
    </AuthGuard>
  );
}