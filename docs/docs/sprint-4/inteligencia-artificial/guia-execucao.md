---
sidebar_position: 1
slug: /inteligencia-artificial/guia-de-execucao
description: "Guia de Execução dos Modelos"
---

# Guia de Execução

## YOLOv8 Ultralytics

Este guia explica como configurar o ambiente para executar o YOLOv8 Ultralytics, incluindo a instalação do Python 3.11 via Deadsnakes, criação de um ambiente virtual, configuração do kernel no Jupyter e instalação das dependências. Para executar os comandos abaixo, é necessário ter o Ubuntu ou executar esses comandos pelo [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/pt-br/windows/wsl/install)

### 1. Instalar o repositório Deadsnakes e Python 3.11

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### 2. Criar e ativar um ambiente virtual com Python 3.11

No diretório do projeto:

```bash
cd /home/inteli/projetos/inteli/2025-1B-T12-EC06-G02/src/IA/IA_v2/src/yolo
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar o Jupyter e o IPython kernel

```bash
pip install --upgrade pip
pip install jupyter ipykernel
python -m ipykernel install --user --name=ia-yolo-venv --display-name="Python 3.11 (YOLO)"
```

### 4. Instalar as dependências do projeto

```bash
pip install -r requirements.txt
```

### 5. Selecionar o kernel no Jupyter

1. Inicie o Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
2. Ao abrir um notebook, selecione o kernel chamado **Python 3.11 (YOLO)**.

#### Maneira alternativa de seleção de Kernel
&emsp; Caso o venv não seja reconhecido como um kernel, é possível realizar esse fluxo para que ele seja rastreado corretamente:

1. Ative o ambiente virtual pelo terminal conforme ensinado anteriormente
    ```bash
    source .venv/bin/activate
    ```

2. Abra o VS Code no diretório do projeto
    ```bash
    code .
    ```

3. No VS Code, o interpretador Python correspondente ao ambiente virtual `.venv` já será reconhecido (normalmente aparece no canto inferior esquerdo). Assim, os notebooks e scripts utilizarão o Python 3.11 configurado.

---

## Segment Anything (SAM)

Para executar o SAM, siga os passos abaixo para criar um ambiente virtual e instalar as dependências:

### 1. Criar e ativar um ambiente virtual

No diretório do SAM:

```bash
cd /home/inteli/projetos/inteli/2025-1B-T12-EC06-G02/src/IA/IA_v2/src/sam
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Observações
&emsp;Para poder rodar o fluxo do Segment Anything propriamente, é necessário ter o arquivo .pt de 1GB.