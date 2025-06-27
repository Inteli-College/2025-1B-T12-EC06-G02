---
sidebar_position: 4
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

## Requisitos

* **Sistema Operacional:** Windows 10 ou 11
* **IDE:** [Android Studio](https://developer.android.com/studio)
* **Dispositivo Android:** Tablet ou smartphone
* **Cabo USB:** Para conexão entre o PC e o dispositivo Android

---

## Passo a Passo para Executar o App

### 1. Clone o Repositório

Clone o repositório principal que contém o aplicativo:

Para clonar o repositório, você pode seguir esse [tutorial](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository)

---

### 2. Abra o Projeto no Android Studio

1. Inicie o Android Studio
2. Vá em **File > Open**
3. Navegue até o diretório clonado
4. Acesse a pasta `src/droneApp` e selecione-a

### A raiz do app **deve ser o "droneApp"**

---

### 3. Faça o Sync do Gradle

Após abrir o projeto:

* Aguarde ou clique em **"Sync Now"** para o Gradle baixar as dependências automaticamente.

Se o Sync não acontecer automaticamente, clique no icone do elefante com uma seta no topo direito!

---

### 4. Configure o arquivo `local.properties`

No diretório `droneApp`, abra o arquivo `local.properties` e adicione suas credenciais Supabase logo abaixo do `sdk.dir`:

```properties
sdk.dir=C:exemplo

// Adicione assim:
BASE_URL=https://sua-supabase-url.supabase.co
SUPABASE_API_KEY=sua-api-key
SUPABASE_BEARER_TOKEN=seu-bearer-token
```

> Importante: Essas credenciais são sensíveis. Não compartilhe esse arquivo em repositórios públicos.

---

### 5. Conecte seu Dispositivo Android

* Use um cabo USB para conectar seu tablet ou celular ao computador.
* Certifique-se de que a **depuração USB** esteja ativada nas configurações do dispositivo Android.

---

### 6. Configure o Dispositivo no Android Studio

1. No Android Studio, vá até a seção **"Device Manager"** no canto superior direito
2. Clique no botão **"+"**
3. Selecione o seu dispositivo Android real (ele deve aparecer listado)
4. Aguarde a conexão e autorização do dispositivo

---

### 7. Compile e Rode o App

* Clique no ícone de play (seta) no topo da janela do Android Studio
* O projeto será compilado e implantado diretamente no dispositivo conectado

---

## Links Úteis

* [Download do Android Studio](https://developer.android.com/studio)
* [Documentação da Supabase](https://supabase.com/docs)
* [Como ativar a Depuração USB](https://developer.android.com/studio/debug/dev-options)


## Requisitos das Funcionalidades

### Envio de Imagens

* Permite selecionar e enviar imagens da galeria do dispositivo para um banco de dados na nuvem (Supabase).
* **Requisitos para funcionar corretamente:**

  * O Supabase deve estar configurado corretamente no arquivo `local.properties`.
  * O dispositivo Android precisa estar conectado à internet (Wi-Fi ou dados móveis).

### Controle do Drone

* Oferece uma interface para controlar um drone Tello diretamente pelo aplicativo.
* **Requisitos para funcionar corretamente:**

  * O dispositivo Android deve estar conectado à rede Wi-Fi gerada pelo drone Tello.
  * É necessário que o drone esteja ligado e com a conexão ativa no momento da execução do app.
