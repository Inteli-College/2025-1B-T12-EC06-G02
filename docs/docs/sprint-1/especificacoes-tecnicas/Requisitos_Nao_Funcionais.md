---
sidebar_position: 2
custom_edit_url: null
---

# Requisitos Não Funcionais

## Introdução
Os requisitos não funcionais, diferente dos requisitos funcionais, especificam os padrões de qualidade que o sistema deve seguir, abordando aspectos como desempenho, usabilidade, confiabilidade e escalabilidade. Embora não definam funcionalidades diretas, são essenciais para assegurar que o nosso sistema opere corretamente, sendo eficiente e de alta qualidade para a experiência do usuário.

Esses requisitos foram definidos considerando:
- A necessidade de rapidez e confiabilidade no ambiente de inspeções prediais.
- A precisão exigida no tratamento de dados.
- A necessidade de usabilidade para operadores técnicos com perfis variados de experiência.

## Requisitos

### RNF01 - Usabilidade da Interface
**Descrição**:  
A interface gráfica deve ser intuitiva, amigável e acessível, permitindo que usuários com conhecimentos técnicos básicos operem o sistema de forma eficiente.

---

### RNF02 - Velocidade de Processamento
**Descrição**:  
O processamento de cada imagem enviada deve ser concluído em, no máximo, 10 segundos, para garantir fluidez na operação, considerando imagens de resolução padrão.

---

### RNF03 - Precisão Mínima de Identificação
**Descrição**:  
O algoritmo de identificação de fissuras deve alcançar uma acurácia mínima de 75% nas imagens analisadas, conforme validação por inspeções humanas.

---

### RNF04 - Confiabilidade no Sistema de Notificações
**Descrição**:  
O sistema de notificações para revisão manual de imagens deve garantir taxa de entrega de 100% para os casos que não atingirem a acurácia mínima, sem perdas ou falhas.

---

### RNF05 - Armazenamento de Histórico de Processamentos
**Descrição**:  
O sistema deve manter um registro local das imagens processadas, incluindo suas classificações, acurácias e localizações.

---

### RNF06 - Compatibilidade com Imagens de Alta Resolução
**Descrição**:  
O sistema deve aceitar e processar imagens de alta resolução sem perdas significativas de desempenho ou qualidade de análise.

---

### RNF07 - Erros de Upload
**Descrição**:  
Em caso de falha no envio de imagens pelo usuário, o sistema deve apresentar mensagens claras de erro e permitir o reenvio sem a necessidade de reiniciar toda a operação.

---

### RNF08 - Precisão Mínima de Classificação
**Descrição**:  
O algoritmo de classificação de fissuras deve alcançar uma acurácia mínima de 85% nas imagens analisadas, conforme validação por inspeções humanas.

---

## Conclusão
Garantir que o sistema seja rápido, confiável e fácil de usar é tão importante quanto oferecer boas funcionalidades. Esses requisitos ajudam a criar uma experiência de uso que faz diferença na prática, tornando o sistema mais fluido, seguro e eficiente. Ao seguir essas diretrizes, entregamos não apenas um sistema funcional, mas também um produto capaz de ser utilizado em ambientes reais de operação, atendendo às necessidades práticas e expectativas dos usuários.
