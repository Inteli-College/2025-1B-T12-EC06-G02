import React from 'react';
import AuthGuard from '../../components/AuthGuard';

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Página de Dashboard</h1>
      </div>
    </AuthGuard>
  );
}