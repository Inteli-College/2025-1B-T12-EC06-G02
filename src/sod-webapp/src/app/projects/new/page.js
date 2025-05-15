import React from 'react';
import AuthGuard from '../../../components/AuthGuard';

export default function NewProjectPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Novo Projeto</h1>
      </div>
    </AuthGuard>
  );
}