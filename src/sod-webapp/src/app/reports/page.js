import React from 'react';
import Layout from '../../components/Layout';
import AuthGuard from '../../components/AuthGuard';

export default function ReportsPage() {
  return (
    <AuthGuard>
      <Layout>
        <div>
          <h1 className="text-2xl font-semibold">Página de Relatórios</h1>
        </div>
      </Layout>
    </AuthGuard>
  );
}