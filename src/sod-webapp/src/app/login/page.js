import React from 'react';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-primary-light">
      <div className="max-w-md w-full bg-white shadow-md rounded p-8">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-semibold text-primary">Sistema Óptico de Detecção</h1>
          <p className="text-gray-medium">Acesse sua conta para continuar</p>
        </div>
        
        <form>
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-dark mb-2">Email</label>
            <input 
              type="email" 
              id="email"
              placeholder="Seu email"
              className="form-input"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-dark mb-2">Senha</label>
            <input 
              type="password" 
              id="password"
              placeholder="Sua senha"
              className="form-input"
            />
          </div>
          
          <button 
            type="submit" 
            className="btn w-full mb-4"
          >
            Entrar
          </button>
          
          <div className="text-center">
            <a href="/forgot-password" className="text-primary hover:underline">
              Esqueceu sua senha?
            </a>
          </div>
        </form>
        
        <div className="mt-6 pt-6 border-t border-gray-light text-center">
          <p>Não tem uma conta? <a href="/register" className="text-primary hover:underline">Registre-se</a></p>
        </div>
      </div>
    </div>
  );
}