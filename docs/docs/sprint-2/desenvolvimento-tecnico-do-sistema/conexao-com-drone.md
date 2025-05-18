---
sidebar_position: 4
custom_edit_url: null
---

# Conexão com o Drone

:::caution Conclusão da Análise
Após os testes realizados, concluímos que será necessário desenvolver uma aplicação de streaming dedicada para o drone na próxima sprint, devido às limitações encontradas no modelo Tello. Esta decisão permite avançar com o desenvolvimento do algoritmo de detecção de fissuras enquanto mantemos flexibilidade para futura integração com drones profissionais DJI.
:::

## 1. Introdução

Este documento apresenta a análise e os testes realizados com o drone Tello para avaliar sua viabilidade na captura de imagens. O projeto visa desenvolver um algoritmo especializado em processamento digital de imagens (PDI) para identificação e classificação dessas fissuras, conforme requisitado pelo Instituto de Pesquisas Tecnológicas do Estado de São Paulo (IPT).

Esta análise é essencial para complementar nossa [proposta de arquitetura](./proposta-da-arquitetura.md), considerando as necessidades específicas dos usuários identificados em nossas [personas](../../sprint-1/ux-ui/Personas.md).

### 1.1 Objetivo dos Testes com Drone

Avaliar se a implementação de um drone como ferramenta de captura de imagens é viável e agrega valor ao projeto, considerando:
- Qualidade das imagens capturadas
- Facilidade de operação
- Limitações técnicas
- Viabilidade de integração com o algoritmo de PDI

Estes testes são fundamentais para validar as hipóteses levantadas durante a elaboração do [protótipo de alta fidelidade](../design-e-ux/prototipo-alta-fidelidade.md).

## 2. Equipamentos Utilizados

### 2.1 Drone Educacional: Tello Just for Fun
- **Fabricante**: Ryze Technology
- **Características**:
  - Câmera de 5MP (720p)
  - Peso: 80g
  - Tempo de voo: ~13 minutos
  - Comunicação: Wi-Fi

### 2.2 Drone Profissional (Cliente): DJI
- Modelos profissionais da DJI possuem:
  - Câmeras de alta resolução (até 4K)
  - Maior estabilidade
  - APIs mais robustas
  - SDK completo para desenvolvimento

## 3. Testes Realizados

### 3.1 Teste de Transmissão de Vídeo (`videoStreamTest.py`)

#### Cenário de Teste
Avaliação da qualidade do streaming de vídeo do Tello e sua viabilidade para identificação de fissuras.

#### Resultados
- **Qualidade de Imagem**: Qualidade de 720p.
- **Estabilidade de Conexão**: Estável, sucessível a interferências.
- **Latência**: Variações entre 400ms e 600ms.

### 3.2 Teste de Movimentação Básica (`app.py`)

#### Cenário de Teste
Avaliação da estabilidade do drone durante movimentos programados, essencial para captura de imagens nítidas de fachadas.

#### Resultados
- **Precisão de Movimentos**: Desvios de 10-20cm em movimentos laterais
- **Estabilidade**: Oscilações perceptíveis durante voo estacionário
- **Tempo de Bateria**: Suficiente para pequenas inspeções

### 3.3 Teste de Controle Remoto via PC (`remotePCControlTest.py`)

#### Cenário de Teste
Avaliação da facilidade de controle manual do drone via teclado para posicionamento preciso diante de áreas com fissuras.

#### Resultados
- **Facilidade de Controle**: Razoavelmente complicado para iniciantes, requer costume com utilização de controles a base de WASD.
- **Responsividade**: Responsivo, possui latência parecida ao video (400ms a 600ms).
- **Captura de Fotos**: Funcional.
- **Qualidade em Movimento**: Movimento simplificado, sem variações de velocidade, rotação (esquerda e direita) consideravelmente "robótica" em vez de constante.

Estes resultados foram essenciais para definir o [diagrama de sequência](./diagrama-de-sequencia.md) e compreender as limitações que devemos considerar na implementação.

## 4. Limitações Identificadas

### 4.1 Limitações do Tello Just for Fun

1. **Limitação de Streaming**:
   - Não permite dois streamings de vídeo simultâneos
   - Apenas um dispositivo pode visualizar o stream por vez (PC ou smartphone)

2. **Captura de Imagens**:
   - Não possui função nativa para tirar fotos através da API
   - Fotos podem ser capturadas salvando frames do streaming

3. **Qualidade de Câmera**:
   - Resolução de 720p para detecção de fissuras 

4. **Estabilidade**:
   - Oscilações em voo estacionário
   - Sensibilidade a ventos leves

### 4.2 Diferenças para o DJI Profissional

1. **Qualidade de Câmera**:
   - Drones DJI profissionais possuem câmeras de até 4K
   - Melhor performance em condições adversas de iluminação

2. **Estabilidade**:
   - Melhores sistemas de estabilização (gimbal de 3 eixos)
   - Maior resistência a ventos

3. **SDK e API**:
   - SDK mais completo com mais recursos
   - Melhor documentação e suporte

4. **Comunicação**:
   - Desconhecimento da comunicação direta entre o aplicativo e o drone DJI
   - Potenciais dificuldades de integração

## 5. Possíveis Soluções

### 5.1 Desenvolvimento de Aplicativo Proprietário

#### Descrição
Desenvolver um aplicativo específico para comunicação com o drone que integre:
- Controle de voo
- Captura de imagens de alta qualidade
- Processamento preliminar das imagens
- Envio para servidor para análise de fissuras

#### Requisitos
- Desenvolvimento para Android/iOS
- Integração com SDK do DJI
- Interface amigável para operadores
- Capacidade de armazenamento local e sincronização

#### Benefícios
- Maior controle sobre o processo
- Experiência do usuário otimizada
- Possibilidade de processamento em tempo real
- Melhor integração com o sistema de análise de fissuras

### 5.2 Adaptação para Uso com Imagens Pré-capturadas

#### Descrição
Modificar a abordagem para trabalhar com imagens já capturadas por drones, sem necessidade de integração direta:
- Criação de módulo de upload de imagens
- Interface para organização das imagens por prédio/fachada
- Algoritmo de análise focado em processamento posterior

#### Requisitos
- Interface web para upload
- Sistema de organização e categorização
- Processamento em lote

#### Benefícios
- Independência de hardware específico
- Compatibilidade com diversas fontes de imagens
- Menor complexidade técnica
- Foco no core do projeto (análise de fissuras)

## 6. Análise de Risco

### 6.1 Riscos do Uso de Drones
- **Regulatórios**: Necessidade de licenças e autorizações para voo em áreas urbanas
- **Climáticos**: Condições de vento e chuva podem impedir operações
- **Técnicos**: Falhas de hardware/software durante inspeções
- **Operacionais**: Necessidade de operadores treinados
- **Autonomia**: Limitação de tempo de voo para grandes edificações

### 6.2 Riscos da Solução, independente dos Drones
- **Qualidade de Imagem**: Dependência da fonte de captura
- **Padronização**: Variação no ângulo e distância das imagens
- **Cobertura**: Dificuldade em acessar áreas elevadas ou de difícil acesso
- **Consistência**: Variação nas condições de iluminação

## 7. Conclusão

Após testes e análises com o drone Tello, identificamos limitações significativas que impactam diretamente a implementação do projeto de detecção de fissuras em revestimentos de argamassa. A principal restrição observada foi a **impossibilidade de manter dois streamings de vídeo simultâneos, permitindo apenas que um dispositivo visualize o stream por vez.**

Diante dessas limitações e considerando os objetivos do projeto para o Instituto de Pesquisas Tecnológicas do Estado de São Paulo (IPT), decidimos que na próxima sprint iremos desenvolver uma aplicação de streaming dedicada para o drone. Esta solução permitirá:

1. Contornar a limitação de streaming único através de uma arquitetura cliente-servidor que redistribua o fluxo de vídeo
2. Implementar funcionalidade de captura de imagens em tempo real com qualidade otimizada
3. Criar um canal de comunicação direto entre o streaming e nossa aplicação principal de detecção de fissuras
4. Estabelecer um buffer local que permita armazenar temporariamente as imagens antes do envio ao servidor de processamento

Esta abordagem representa um passo que nos permite avançar no desenvolvimento do algoritmo de detecção de fissuras com imagens reais, enquanto mantemos a flexibilidade para futura integração com equipamentos mais avançados como os drones profissionais DJI que o cliente dispõe.

Essa conclusão está alinhada com as definições apresentadas no [protótipo de alta fidelidade](../design-e-ux/prototipo-alta-fidelidade.md) e com as necessidades identificadas na [arquitetura da informação](../design-e-ux/arquitetura-da-informacao.md).

## 8. Referências

- Documentação DJI SDK: https://developer.dji.com/
- Documentação Tello SDK: https://github.com/dji-sdk/Tello-Python
- Biblioteca DJITelloPy: https://github.com/damiafuentes/DJITelloPy
- OpenCV para processamento de imagens: https://opencv.org/