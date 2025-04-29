---
sidebar_position: 2
custom_edit_url: null
---

# User Stories

## Conceito

&emsp;Dentro de um projeto, as User Stories são fundamentais para traduzir as necessidades dos usuários em requisitos claros e focados. Elas descrevem, de maneira simples e eficaz, o que o usuário precisa realizar na plataforma e qual benefício espera alcançar. Isso garante que as funcionalidades desenvolvidas estejam alinhadas com os fluxos reais de trabalho e objetivos da persona.

## User Stories - Mariana Ribeiro

&emsp;No contexto deste projeto, as User Stories representam as principais interações da pesquisadora Mariana Ribeiro, detalhando suas atividades na análise de fissuras em fachadas e gestão de relatórios técnicos. 

A seguir, estão as User Stories elaboradas para guiar o desenvolvimento do sistema para atender às suas necessidades específicas.


####  Login no sistema de análise
| - | 01 |
| --- | --- |
| Persona | Mariana Ribeiro - Pesquisadora |
| User Story | "Como pesquisadora, quero realizar login de forma segura e rápida para acessar o sistema de análise de fissuras sem perder tempo no início do trabalho." |
| Critério de aceite 1 | CR1: Carolina deve poder inserir suas credenciais (e-mail institucional e senha) para acessar o sistema. |
| Critério de aceite 2 | CR2: Em caso de erro de login, o sistema deve oferecer a opção de recuperação de senha via e-mail institucional. |
---

#### Analisar imagens de fachadas para detecção de fissuras

| -- | 02 |
| --- | --- |
| Persona | Mariana Ribeiro - Pesquisadora |
| User Story | "Como pesquisadora, quero visualizar e analisar imagens de fachadas para identificar automaticamente fissuras e classificá-las por gravidade." |
| Critério de aceite 1 | CR1: Carolina deve poder carregar imagens capturadas por drones ou câmeras. |
| Critério de aceite 2 | CR2: O sistema deve detectar fissuras automaticamente e apresentar a classificação de gravidade e tipos de fissuras na tela de análise. |
---


#### Gerar relatórios técnicos automáticos
| -- | 03 |
| --- | --- |
| Persona | Mariana Ribeiro - Pesquisadora|
| User Story | "Como pesquisadora, quero gerar relatórios técnicos automáticos a partir das análises de fissuras para documentar o estado das fachadas de forma prática e padronizada." |
| Critério de aceite 1 | CR1: Carolina deve poder gerar relatórios a partir dos resultados das análises com informações como localização da fissura, tipo e grau de severidade. |
| Critério de aceite 2 | CR2: O relatório deve ser exportável em formato PDF e compatível para anexação em laudos técnicos. |

---

## User Stories - Carlos Eduardo

#### 01 \- Upload de Imagens

| \- | 01 |
| :---- | :---- |
| Persona | Carlos Eduardo \- Técnico em Edificações |
| User Story | "Como técnico em edificações, quero carregar facilmente imagens de alta resolução (capturadas por drone ou câmera) para que o sistema possa analisá-las em busca de fissuras." |
| Critério de aceite 1 | CR1: Carlos deve poder selecionar múltiplas imagens de seu dispositivo ou de um diretório específico para upload. |
| Critério de aceite 2 | CR2: O sistema deve indicar o progresso do upload e confirmar quando as imagens foram carregadas com sucesso. |
| Critério de aceite 3 | CR3: O sistema deve aceitar formatos comuns de imagem (JPG, PNG, TIFF) e informar caso um formato não seja suportado ou a resolução seja inadequada. |

---

#### 02 \- Iniciar Análise de Fissuras

| \- | 02 |
| :---- | :---- |
| Persona | Carlos Eduardo \- Técnico em Edificações |
| User Story | "Como técnico em edificações, quero iniciar a análise das imagens carregadas para que o algoritmo identifique e marque automaticamente as fissuras presentes nos revestimentos." |
| Critério de aceite 1 | CR1: Carlos deve poder selecionar as imagens ou um lote de imagens carregadas (associadas a um projeto/inspeção) para iniciar o processo de análise. |
| Critério de aceite 2 | CR2: O sistema deve fornecer uma estimativa do tempo de processamento e notificar Carlos (ex: via e-mail ou notificação no sistema) quando a análise estiver concluída. |

---

#### 03 \- Visualização dos Resultados

| \- | 03 |
| :---- | :---- |
| Persona | Carlos Eduardo \- Técnico em Edificações |
| User Story | "Como técnico em edificações, quero visualizar as fissuras detectadas sobrepostas nas imagens originais para entender sua localização, padrão e extensão exatas." |
| Critério de aceite 1 | CR1: O sistema deve exibir a imagem original com as fissuras detectadas claramente marcadas (ex: contornos coloridos, segmentação). |
| Critério de aceite 2 | CR2: Carlos deve poder aplicar zoom e navegar pela imagem de forma fluida para inspecionar as fissuras em detalhe. |
| Critério de aceite 3 | CR3: Deve ser possível alternar a visualização das marcações (ligar/desligar) para comparar com a imagem original limpa. |

---

#### 04 \- Detalhes e Classificação das Fissuras

| \- | 04 |
| :---- | :---- |
| Persona | Carlos Eduardo \- Técnico em Edificações |
| User Story | "Como técnico em edificações, quero acessar informações detalhadas sobre cada fissura detectada, como sua classificação de gravidade e dimensões estimadas, para embasar meu diagnóstico técnico." |
| Critério de aceite 1 | CR1: Ao selecionar uma fissura marcada na imagem (ou em uma lista), o sistema deve exibir suas propriedades calculadas (ex: comprimento, largura média/máxima, área, orientação, classificação de risco/gravidade). |
| Critério de aceite 2 | CR2: O sistema deve permitir que Carlos valide a classificação de gravidade proposta pelo algoritmo, justificando a alteração se necessário. |

---


#### 05 \- Monitoramento Histórico

| \- | 05 |
| :---- | :---- |
| Persona | Carlos Eduardo \- Técnico em Edificações |
| User Story | "Como técnico em edificações, quero comparar a análise atual de uma fachada com análises anteriores armazenadas no sistema para monitorar a evolução das fissuras ao longo do tempo e planejar manutenções preventivas." |
| Critério de aceite 1 | CR1: O sistema deve permitir associar análises a um mesmo edifício/fachada/setor e visualizá-las cronologicamente. |
| Critério de aceite 2 | CR2: O sistema deve oferecer uma ferramenta de comparação visual (lado a lado ou sobreposição) entre imagens de diferentes datas, destacando mudanças (novas fissuras, aumento de tamanho, etc.). |
| Critério de aceite 3 | CR3: O sistema deve gerar gráficos ou tabelas que mostrem a evolução de indicadores chave (ex: número de fissuras, comprimento total, índice de gravidade) ao longo do tempo para a área monitorada. |
