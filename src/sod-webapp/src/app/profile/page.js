import React from 'react';
import AuthGuard from '../../components/AuthGuard';

export default function ProfilePage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Perfil</h1>
      </div>
    </AuthGuard>
  );
}