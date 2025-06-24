---
sidebar_position: 1
slug: /sprint-5/instrucao-de-execucao-do-projeto
description: "Instruções para rodar a solução"
---

# Instruções para Rodar Localmente

## Pré-requisitos:

- Ter o **arquivo .env** contendo NEXT_PUBLIC_SUPABASE_URL e NEXT_PUBLIC_SUPABASE_ANON_KEY - Enviado à parte

- Ter o **arquivo .pt** do modelo treinado swin-transformer - Enviado à parte

- **VSCode** - siga o tutorial de [instalação do programa](https://code.visualstudio.com/download) de acordo com seu sistema operacional;

- **Python versão 3.12** - siga o tutorial de [instalação do programa](https://www.python.org/downloads/) de acordo com seu sistema operacional.

- **Node.js versão 10.2.4** - siga o tutorial de [instalação do programa](https://www.alura.com.br/artigos/como-instalar-node-js-windows-linux-macos?srsltid=AfmBOoqVZEMYaSsrE_4sn2D9QqTGAvX3bEoZqMKl89EliXOpbcJedDGa) de acordo com seu sistema operacional

## Instruções de Uso - Aplicação WEB

Siga as etapas abaixo para executar o aplicativo corretamente.

### 1. Clonando este repositório

Para clonar o repositório, você pode seguir esse [tutorial](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository)

### 2. Incluindo os arquivos

#### 2.1. Arquivo de Configuração do Servidor 

Por meio de um arquivo de pastas, acesse o diretório do repositório clonado e inclua o arquivo ".env" no diretório ``src/sod-webapp``

#### 2.2. Arquivo do modelo Swin-Transformer-V2

Por meio de um arquivo de pastas, acesse o diretório do repositório clonado acesse a seguinte pasta: ``src/IA/IA_v2/src/swin-transformer-v2``. Em seguida, crie um diretório com o nome **models** e inclua dentro dele o seu arquivo ".pt".

### 3. Rodando o web app

#### 3.1. Instale as dependências do Node.js

No VSCode, abra o repostório clonado e abra o terminal. Em seguida, acesse o diretório ``src/sod-webapp`` colando o seguinte comando no terminal.

   ```bash
   cd src/sod-webapp
   ```

Então, para instalar as dependências do Node.js, cole o seguinte comando:

   ```bash
   npm install
   ```
#### 3.2. Inicie o servidor de desenvolvimento 

Rode o servidor Next.js:


```bash
npm run dev
```


O terminal exibirá uma mensagem semelhante a:


```
▲ Next.js 14.1.0
- Local:     http://localhost:3000
- Environments: .env.local
✓ Ready in 4s
```

:::warning[Aviso]

Para que a aplicação funcione corretamente, é necessário rodar o servidor em Flask. Essas instruções serão dadas abaixo. Caso tente rodar a aplicação sem ele, ao clicar "Iniciar Processamento" da IA, a tela permanecerá em carregamento infinito

:::

### 4. Rodando o servidor Flask

#### 4.1. Crie um ambiente virtual Python

Abra um novo terminal do VSCode, acesse o diretório ``src/IA_v2`` colando o seguinte comando no terminal.

   ```bash
   cd src/IA_v2
   ```

Em seguida, **a depender do seu sistema operacional** cole o seguinte comando:

> Linux

    ```bash
   python3 -m venv venv
   ```

> Windows 

    ```bash
   python -m venv venv
   ```

#### 4.2. Ative seu ambiente virtual

Então, para ativar seu ambiente virtual, cole o seguinte comando no mesmo terminal:

> Linux

    ```bash
   source venv/bin/activate
   ```

> Windows 

    ```bash
   .\venv\Scripts\activate
   ```

#### 4.3. Instale as dependências do projeto

Para instalar as dependências do projeto, cole o seguinte comando no mesmo terminal:

   ```bash
   pip install -r requirements.txt
   ```

#### 4.4. Inicie o servidor

Ainda no mesmo terminal, rode o servidor. Para tanto, cole o seguinte comando no mesmo terminal:

> Linux

    ```bash
   python3 ./src/server.py
   ```

> Windows 

    ```bash
   python ./src/server.py
   ```

Pronto, agora você pode aproveitar plenamente das funcionalidades da aplicação web do Sistema Óptico de Detecção.

## Instruções de Uso - Aplicativo do Drone



