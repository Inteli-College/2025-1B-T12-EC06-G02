---
sidebar_position: 1
custom_edit_url: null
---

# Requisitos Funcionais

## Introdução
Os requisitos funcionais representam as funcionalidades específicas que o sistema deve possuir para atender às necessidades dos usuários e cumprir seus objetivos. Esses requisitos são formados a base da nossa visão geral da função do software e da [Arquitetura Inicial](./Arquitetura_Inicial.md). Eles descrevem de forma clara e objetiva o que o nosso software deve realizar, orientando o desenvolvimento e garantindo que os resultados esperados sejam alcançados.

Cada funcionalidade a seguir é acompanhada do seu propósito e identifica o tipo de usuário que irá interagir com ela.

## Requisitos

### RF01 - Upload Manual de Imagens
**Descrição**:  
O sistema deve permitir que o usuário insira manualmente imagens capturadas de fachadas no software.

**Tipo de usuário**:  
Operador técnico / Especialista.

**Propósito**:  
Possibilitar o envio de imagens capturadas externamente para análise pelo sistema.

---

### RF02 - Processamento de Imagem
**Descrição**:  
O software deve analisar as imagens inseridas utilizando um algoritmo para identificar fissuras em revestimentos de argamassa, disponibilizando também a acurácia das identificações de cada imagem.

**Tipo de usuário**:  
Operador técnico / Sistema automático.

**Propósito**:  
Garantir a identificação de fissuras e fornecer uma medida de confiança da análise realizada.

---

### RF03 - Classificação do Tipo das Fissuras
**Descrição**:  
As fissuras detectadas devem ser automaticamente classificadas por tipo.

**Tipo de usuário**:  
Sistema automático.

**Propósito**:  
Organizar e categorizar os tipos de fissuras para facilitar o entendimento técnico e priorização de ações.

---

### RF04 - Geração Automática de Relatórios
**Descrição**:  
O sistema deve gerar relatórios automáticos com as fissuras detectadas, suas localizações, classificações e acurácia.

**Tipo de usuário**:  
Operador técnico / Especialista / Gestores.

**Propósito**:  
Facilitar o acompanhamento, registro e tomada de decisão baseada em dados objetivos.

---

### RF05 - Inserção da Localização da Imagem
**Descrição**:  
O sistema deve permitir que o usuário insira a localização onde a imagem da fissura foi capturada.

**Tipo de usuário**:  
Operador técnico.

**Propósito**:  
Assegurar o correto mapeamento espacial das fissuras detectadas, possibilitando rastreamento futuro e organização geral das imagens.

---

### RF06 - Sistema de Separação de Imagem
**Descrição**:  
O sistema deve ser capaz de separar as imagens processadas entre as que atingiram a acurácia mínima definida e as que ficaram abaixo desse limite.

**Tipo de usuário**:  
Sistema automático.

**Propósito**:  
Facilitar a gestão de imagens confiáveis e sinalizar aquelas que requerem revisão.

---

### RF07 - Sinalização de Necessidade de Revisão Humana
**Descrição**:  
Para imagens com acurácia abaixo da definida, o sistema deve possuir um mecanismo de notificação local para o operador, solicitando que um especialista realize a análise manual.

**Tipo de usuário**:  
Operador técnico / Especialista.

**Propósito**:  
Garantir a qualidade final da análise, evitando erros de interpretação nas imagens de baixa confiança.

---

## Conclusão
Ter um conjunto claro de requisitos funcionais é o que nos garante que o sistema vai atender ao que é esperado pelos usuários. Cada funcionalidade listada foi pensada para tornar o processo de identificação e classificação de fissuras mais rápido, preciso e confiável. Seguindo essas diretrizes, o sistema terá uma base sólida para entregar valor real no dia a dia de quem vai utilizá-lo.
