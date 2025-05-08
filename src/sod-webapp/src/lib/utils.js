import { clsx } from "clsx";
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

// Funções de utilidade gerais

// Função para formatar datas
export function formatDate(date) {
  // Formata uma data para exibição
}

// Função para formatar valores de severidade
export function formatSeverity(severity) {
  // Formata e traduz valores de severidade
}

// Função para validar entradas de formulário
export function validateInput(type, value) {
  // Valida diferentes tipos de entrada de formulário
}

// Função para tratar erros
export function handleError(error) {
  // Tratamento padronizado de erros
}

// Função para criar URLs de imagem
export function getImageUrl(path) {
  // Cria URL completa para uma imagem
}
