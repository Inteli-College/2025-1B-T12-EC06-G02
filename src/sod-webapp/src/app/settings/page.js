import React from 'react';
import AuthGuard from '../../components/AuthGuard';

export default function SettingsPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Configurações</h1>
      </div>
    </AuthGuard>
  );
}