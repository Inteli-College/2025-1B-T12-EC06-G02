---
sidebar_position: 1
slug: /sprint-3/escopo
description: "Escopo da sprint 3 no projeto"
---

# Escopo da Sprint

&emsp; Durante a Sprint 3, o grupo SOD concentrou seus esforços no desenvolvimento de novas funcionalidades e na implementação de mudanças fundamentais para o avanço do projeto. Os principais focos dessa etapa foram: o início do desenvolvimento do aplicativo de controle do drone, a atualização do sistema web com funcionalidades relevantes e o desenvolvimento de novos modelos de inteligência artificial (IA) para classificação de imagens.

&emsp; É importante destacar que, conforme o escopo definido para a sprint, não era prevista a finalização ou entrega oficial do aplicativo de controle do drone, mas sim o início da sua implementação e a definição da estratégia de integração com o restante do sistema.

&emsp; No sistema web, foram realizadas melhorias significativas na interface com o objetivo de torná-la mais completa e intuitiva para o usuário. Entre as novidades, destaca-se a [Mini Galeria](./Atualizacoes-do-frontend.md), que permite a visualização prévia de todas as imagens selecionadas para análise — seja por upload local ou recebimento direto do servidor. Também foi implementado um botão de [carregamento via servidor](./Atualizacoes-do-frontend.md), que possibilita a importação automática de imagens capturadas pelo aplicativo do drone diretamente do servidor, facilitando o fluxo de trabalho e a usabilidade da plataforma.

&emsp; Outra funcionalidade adicionada foi a de [preview de relatório](./Atualizacoes-do-frontend.md), que apresenta ao usuário a opção de visualizar o relatório com os resultados da análise gerada pela IA, essa funcionalidade é encontrada na tela de resultados junto com a opção de download e a visualização quantitativa dos diferentes tipos de fissuras identificadas. Além disso, foi criada uma tela de [histórico](./Atualizacoes-do-frontend.md) de relatórios, permitindo o acesso aos relatórios já gerados, com possibilidade de visualização e novo download a qualquer momento.

&emsp; No campo da [inteligência artificial](./inteligencia-artificial/preprocessamento-imagens.md), a equipe desenvolveu uma pipeline modular para o treinamento e avaliação de novos modelos de classificação. Essa abordagem permitiu testar diferentes filtros e modelos de IA de forma flexível e estruturada. Como resultado, dois novos [modelos](./inteligencia-artificial/modelos/primeiro-modelo-s3.md) foram treinados, e um deles já foi integrado ao backend do sistema, viabilizando a geração automática de relatórios a partir das análises — embora o layout final do relatório ainda esteja em fase de desenvolvimento.

## Equipes Responsáveis

&emsp; Para garantir um desenvolvimento organizado e eficiente, o grupo foi estruturado em equipes de trabalho, de forma que cada área de entrega recebesse a devida atenção. Distribuindo as responsabilidades entre os integrantes da equipe, otimizamos o progresso nas diferentes frentes do projeto. A composição das equipes ficou definida da seguinte forma:

**Davi Abreu e Pablo Azevedo** - Criação do pipeline e tudo que é relacionado aos dois novos modelos de IA  
**Julia Lika e Marcelo Conde** - Desenvolvimento do aplicativo de controle do drone e conexão com o sistema  
**Isabelle Dantas, Lucas Nepomuceno e Luiza Petenazzi** - Mudanças na interface e atualização com as novas funcionalidades do sistema  

**Apresentação** - Marcelo Conde e Luiza Petenazzi


