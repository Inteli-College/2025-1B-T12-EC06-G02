---
sidebar_position: 2
slug: /sprint-3/como-rodar
description: "Instruções para rodar a solução"
---

# Instruções para Rodar Localmente

## Estado atual do projeto

&emsp; Nessa sprint, a equipe SOD aprimorou a solução a ponto de torná-la viável do início ao fim via plataforma. Apesar de a solução não estar em sua versão de mercado, ela já apresenta recursos como login, cadastro, envio de fotos ([RF01](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md)), processamento de imagem ([RF02](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md)), classificação pelo tipo de fissura ([RF03](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md)) e até geração de relatórios ([RF04](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md)). Além disso, adicinou-se um requisito não presente no escopo até essa sprint:

:::note[RF08 - Upload de Imagens via servidor]
**Descrição**:  
O usuário deve conseguir puxar as imagens do servidor que foram enviadas pelo aplicativo do drone.

**Tipo de usuário**:  
Operador técnico / Especialista.

**Propósito**:  
Garantir a facilidade no processo de análise de imagem desde o uso do drone.

:::

&emsp; Este requisito está quase finalizado. O fluxo necessário para o seu funcionamento já acontece: é possível enviar imagens do aplicativo SOD para o servidor e recuperá-las via *webapp*. Entretanto, é necessário aumentar a usabilidade, principalmente no que tange à quais imagens recuperar.

&emsp; Os requisitos não funcionais [RNF02, RNF03 e RNF08](../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md) também foram cumpridos nessa sprint.

&emsp; Entretanto, devido ao aumento da complexidade do aplicativo, aumentou-se também suas instruções de uso, conforme demonstrado abaixo.

:::warning[Aviso]

Devido a não finalização do app, ainda não será possível testá-lo nessa sprint

:::

## Pré-requisitos:

- Ter o **arquivo .env** contendo NEXT_PUBLIC_SUPABASE_URL e NEXT_PUBLIC_SUPABASE_ANON_KEY - Enviado à parte
- Ter o **arquivo .pt** do modelo treinado swin-transformer - Enviado à parte
- **VSCode** - siga o tutorial de [instalação do programa](https://code.visualstudio.com/download) de acordo com seu sistema operacional;
- **Python versão 3.12** - siga o tutorial de [instalação do programa](https://www.python.org/downloads/) de acordo com seu sistema operacional.
- **Node.js versão 10.2.4** - siga o tutorial de [instalação do programa](https://www.alura.com.br/artigos/como-instalar-node-js-windows-linux-macos?srsltid=AfmBOoqVZEMYaSsrE_4sn2D9QqTGAvX3bEoZqMKl89EliXOpbcJedDGa) de acordo com seu sistema operacional

## Instruções de Uso

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





