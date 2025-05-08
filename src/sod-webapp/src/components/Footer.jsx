import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-primary text-white py-6 mt-auto">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-lg font-semibold">Sistema Óptico de Detecção</p>
            <p className="text-sm">Detecte fissuras em edificações de forma simplificada com nossa IA</p>
          </div>
          
          <div className="flex space-x-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Links</h3>
              <ul className="space-y-1">
                <li><a href="/about" className="text-sm hover:underline">Sobre nós</a></li>
                <li><a href="/contact" className="text-sm hover:underline">Contato</a></li>
                <li><a href="/terms" className="text-sm hover:underline">Termos de uso</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Suporte</h3>
              <ul className="space-y-1">
                <li><a href="/faq" className="text-sm hover:underline">FAQ</a></li>
                <li><a href="/documentation" className="text-sm hover:underline">Documentação</a></li>
                <li><a href="/help" className="text-sm hover:underline">Ajuda</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="mt-6 pt-4 border-t border-white/20 text-center text-sm">
          <p>© {new Date().getFullYear()} Sistema Óptico de Detecção. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}