import React from 'react';

export default function Navbar() {
  return (
    <header className="bg-white border-b border-gray-light">
      <nav className="container mx-auto flex items-center justify-between py-4">
        <div className="flex items-center">
          <img src="/logo.png" alt="SOD Logo" className="h-8" />
          <span className="ml-2 text-xl font-semibold text-primary">SOD</span>
        </div>
        
        <div className="flex items-center space-x-4">
          <a href="/dashboard" className="text-gray-dark hover:text-primary">Dashboard</a>
          <a href="/projects" className="text-gray-dark hover:text-primary">Projetos</a>
          <a href="/reports" className="text-gray-dark hover:text-primary">Relatórios</a>
          <button className="btn">Minha Conta</button>
        </div>
      </nav>
    </header>
  );
}