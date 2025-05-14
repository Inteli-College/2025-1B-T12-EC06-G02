import React from 'react';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-primary-light">
      <div className="max-w-md w-full bg-white shadow-md rounded p-8">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-semibold text-primary">Criar uma nova conta</h1>
          <p className="text-gray-medium">Preencha os campos abaixo para se registrar</p>
        </div>
        
        <form>
          <div className="mb-4">
            <label htmlFor="name" className="block text-gray-dark mb-2">Nome completo</label>
            <input 
              type="text" 
              id="name"
              placeholder="Seu nome completo"
              className="form-input"
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-dark mb-2">Email</label>
            <input 
              type="email" 
              id="email"
              placeholder="Seu email"
              className="form-input"
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-dark mb-2">Senha</label>
            <input 
              type="password" 
              id="password"
              placeholder="Sua senha"
              className="form-input"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="confirmPassword" className="block text-gray-dark mb-2">Confirmar senha</label>
            <input 
              type="password" 
              id="confirmPassword"
              placeholder="Confirme sua senha"
              className="form-input"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="role" className="block text-gray-dark mb-2">Função</label>
            <select
              id="role"
              className="form-input"
            >
              <option value="">Selecione sua função</option>
              <option value="researcher">Pesquisador</option>
              <option value="technician">Técnico</option>
              <option value="manager">Gerente</option>
            </select>
          </div>
          
          <button 
            type="submit" 
            className="btn w-full mb-4"
          >
            Registrar
          </button>
        </form>
        
        <div className="mt-6 pt-6 border-t border-gray-light text-center">
          <p>Já possui uma conta? <a href="/login" className="text-primary hover:underline">Faça login</a></p>
        </div>
      </div>
    </div>
  );
}