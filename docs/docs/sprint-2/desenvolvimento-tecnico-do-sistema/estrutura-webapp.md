---
sidebar_position: 4
custom_edit_url: null
---

# Estrutura Geral do Web App

&emsp;O projeto é uma aplicação web desenvolvida com Next.js e Tailwind CSS. Abaixo está a estrutura de pastas baseada no diretório `2025-1B-T12-EC06-G02/src/sod-webapp`:

## Estrutura de Pastas

* **`public/`**: Arquivos estáticos acessíveis publicamente, como imagens, favicon e outros recursos.
* **`src/`**: Código-fonte principal da aplicação.
   * **`app/`**: Contém as páginas e componentes principais do Next.js.
       * **`layout.tsx`**: Define o layout global da aplicação.
       * **`page.tsx`**: Página inicial.
       * **`analysis/`**: Funcionalidades relacionadas às análises.
           * **`[id]/page.tsx`**: Página dinâmica para exibir detalhes de uma análise específica.
           * **`new/page.tsx`**: Página para criar uma nova análise.
   * **`api/`**: Rotas de API do Next.js.
       * **`images/`**: Manipulação e processamento de imagens.
* **`styles/`**: Arquivos de estilos globais, como `globals.css`.
* **Configurações e dependências:**
   * **`package.json` e `package-lock.json`**: Gerenciamento de dependências e scripts.
   * **`next.config.mjs`**: Configurações do Next.js.
   * **`tailwind.config.js` e `postcss.config.js`**: Configurações do Tailwind CSS e PostCSS.

## Como o Algoritmo de IA é Processado

&emsp;O aplicativo utiliza algoritmos de IA integrados às rotas da API localizadas em `src/sod-webapp/api/`. O fluxo geral é:

1. O usuário interage com a interface web, enviando dados ou imagens por meio das páginas de análise.
2. A solicitação é encaminhada para a API, especialmente para rotas como `api/images/`, responsáveis pelo processamento de imagens.
3. O backend executa o processamento utilizando modelos de Machine Learning e bibliotecas como TensorFlow.js e outras dependências presentes no projeto.
4. O resultado do processamento (por exemplo, uma classificação ou análise) é retornado à interface e exibido ao usuário.

&emsp;Os modelos de IA podem ser treinados previamente e integrados ao projeto, ou utilizar APIs externas, conforme definido na implementação das rotas da API. Todo o processamento ocorre de forma assíncrona.

## Conclusão
&emsp;Para entender como rodar a aplicação, acessar o documento sobre [Instruções de Uso](./instrucoes-uso/rodar-webapp.md)