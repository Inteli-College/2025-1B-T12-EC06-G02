import React from 'react';
import AuthGuard from '../../../../components/AuthGuard';

export default function EditProjectPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Edição de Projeto</h1>
      </div>
    </AuthGuard>
  );
}