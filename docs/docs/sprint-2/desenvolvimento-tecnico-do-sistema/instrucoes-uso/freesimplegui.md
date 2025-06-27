---
sidebar_position: 2
slug: /desenvolvimento-tecnico/instrucoes/freesimplegui
---

# Interface Simples

## PySimpleGUI

&emsp; [PySimpleGUI](https://pysimplegui.readthedocs.io/) é uma biblioteca Python voltada para a criação de interfaces gráficas (GUIs) de maneira simples e intuitiva. Ela permite o desenvolvimento de janelas, botões, campos de texto e outros componentes visuais com uma sintaxe acessível mesmo para quem está começando na programação. Neste projeto, a SOD utilizou essa biblioteca para criar uma interface simples para testar sua IA.

&emsp; Na interface você poderá fazer o _upload_ de uma imagem e ela retornará os resultados de acordo com o modelo da IA. Para rodar essa interface, siga os seguintes passos:

## Pré-Requisitos

1. Faça o download dos seguintes programas:

&emsp; **VSCode** - siga o tutorial de [instalação do programa](https://code.visualstudio.com/download) de acordo com seu sistema operacional;
&emsp; **Python versão 3.12** - siga o tutorial de [instalação do programa](https://www.python.org/downloads/) de acordo com seu sistema operacional.


## Instruções de Uso

Siga as etapas abaixo para executar o aplicativo corretamente.

### 1. Clone este repositório

Para clonar o repositório você pode seguir esse [tutorial](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository)

### 2. Acesse o diretório do nosso repositório no VSCode

### 3. Acesse o diretório src/IA_classificacao

Abra o terminal do VSCode e rode o comando:
```bash

cd src/IA_v1

```

### Crie a sua venv

No terminal, rode o comando:
1. Windows
```bash

python -m venv venv

```

2. Linux/Mac

```bash

python3 -m venv venv

```

### 3. Ative a sua venv

Rode no terminal o seguinte comando:
1. Windows
```bash

.\venv\Scripts\activate

```

2. Linux/Mac

```bash

source venv/bin/activate

```

### 4. Instale as dependências

Para instalar todas as depedências necessárias para a interface, rode no terminal:
```bash

pip install -r requirements.txt

```

### 5. Rode a interface

Agora, você já está no último passo. Basta rodar:
1. Windows
```bash

python main.py

```

2. Linux/Mac
```bash

python3 main.py

```

E a interface se abrirá. Agora, basta fazer o upload da sua fissura e ver o resultado da IA. O resultado da IA será como abaixo:

<div style={{textAlign: 'center'}}>
A fissura é do tipo: Retração <br/>
Nível de confiança: 100.00%
</div>


:::warning[Aviso]

Esta IA foi treinada apenas para identificar fissuras térmicas ou de retração.
Outros tipos de fissura ou imagens fora do escopo podem resultar em erro ou análise incorreta.
:::




