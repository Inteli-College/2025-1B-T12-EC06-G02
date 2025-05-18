---
sidebar_position: 3
slug: /desenvolvimento-tecnico/instrucoes/rodando-webapp
---

# Estrutura Web App
&emsp;Para entender como a estrutura do Web App funciona e como ela se integra com o algoritmo de IA, acessar a seguinte seção: [Estrutura Web App](../estrutura-webapp.md)

## Como Rodar a Aplicação

### 1. **Acesse o diretório do projeto** 
&emsp;No terminal, navegue até a pasta do webapp (deve ser algo parecido com):

```bash
cd 2025-1B-T12-EC06-G02/src/sod-webapp
```

### 2. **Ative o ambiente virtual Python** 
&emsp;Para instalar dependências de Python sem criar conflitos de pacote, crie um ambiente virtual e o ative:
- Para Linux:
   ```bash
   python3 -m venv .venv
   ```
   ```bash
   source ../../.venv/bin/activate
   ```


- Para Windows:
   ```bash
   python -m venv .venv
   ```


   ```bash
   .venv\Scripts\activate
   ```


- Após isso, instale as dependências necessárias para rodar o algoritmo de IA presentes no diretório *src/IA_classificacao/requirements.txt*:
  
   ```bash
   pip install -r requirements.txt
   ```


### 3. **Instale as dependências do Node.js** 
&emsp;Navegue até o diretório `src/sod-webapp` xecute o comando abaixo para instalar as dependências do projeto:


   ```bash
   npm install
   ```


### 4. **Inicie o servidor de desenvolvimento** 
&emsp;Rode o servidor Next.js:


```bash
npm run dev
```


&emsp;O terminal exibirá uma mensagem semelhante a:


```
▲ Next.js 14.1.0
- Local:     http://localhost:3000
- Environments: .env.local
✓ Ready in 4s
```
> **Observação:**  
> Até o momento da Sprint 2, a solução está em desenvolvimento. Portanto, será necessário inserir as variáveis de ambiente em um arquivo `.env.local` dentro do diretório da aplicação para que o servidor funcione corretamente.


### 5. **Acesse a aplicação no navegador** 
&emsp;Abra o navegador e acesse: [http://localhost:3000](http://localhost:3000)

> **Observação:** 
> Durante o uso de funcionalidades de IA, mensagens do TensorFlow e logs do Python podem aparecer no terminal. Isso é esperado e indica o processamento dos modelos de Machine Learning integrados ao backend.