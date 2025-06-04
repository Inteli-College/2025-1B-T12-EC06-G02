---
title: Análise Financeira - Solução final
sidebar_position: 4
---

# Análise Financeira - Solução Final

## Introdução

A solução final proposta pelo SOD para o IPT tem como finalidade implementar, na prática, o conceito teórico demonstrado de forma resumida na prova de conceito.

Para tanto, é importante ressaltar que dificilmente será encontrada uma solução comercializada já pronta no mercado que esteja disponível para compra e uso imediato neste domínio específico. Isso torna necessária uma equipe de profissionais capacitados não apenas para idealizar, prototipar e produzir o sistema final, mas também para integrar com as tecnologias que atendam às necessidades específicas identificadas nas [personas do projeto](../ux-ui/Personas.md) - que depois foram concretizadas em [requisitos funcionais](/docs/docs/sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) e [não funcionais](/docs/docs/sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md). No caso do IPT, podemos citar como exemplo dessa parte o drone que eles utilizam da DJI e o sistema de armazenamento de imagens e relatórios que eles já tem internamente.

Nesse sentido, o que compete à análise financeira da solução final é examinar: (1) o custo da **equipe multidisciplinar** de profissionais que trabalharão desenvolvendo o sistema; (2) os custos de **infraestrutura e tecnologia**; (3) a incidência dos **impostos** sobre o projeto; (4) os **custos de manutenção** por um ano; e (5) o **lucro** almejado pela equipe. Alguns outros custos, como o drone, citado no último parágrafo, não são contemplados aqui, visto que o [modelo de negócios](/docs/docs/sprint-1/analise-de-negocios/business_model_canvas.md) adotado pelo grupo não engloba atuar dessa forma.

Dito isso, é possível então começar a análise financeira.

## Equipe de Desenvolvimento

### Composição da equipe

Visando o sucesso do projeto, é indispensável que profissionais com diferentes especializações trabalhem juntos. Para a solução SOD, que envolve inteligência artificial, desenvolvimento web, aplicativo móvel e interface de usuário, é necessária uma equipe multidisciplinar que contenha as seguintes especialidades:

Para tornar a solução final algo tangível e escalável, sugere-se uma equipe de **máximo 7 profissionais** - semelhante ao grupo que produziu a POC do prjeto - que trabalharão no projeto por um período de **4 meses**. Esses integrantes estarão distribuídos da seguinte forma:

- **1 Product Owner** - Gestão do produto e alinhamento com stakeholders
- **1 Cientista de Dados/IA** - Desenvolvimento e otimização dos modelos de IA
- **2 Desenvolvedores Full-Stack** - Desenvolvimento web e backend
- **1 Desenvolvedor Mobile** - Aplicativo Android para controle de drones
- **1 Engenheiro DevOps** - Infraestrutura, deploy e monitoramento
- **1 UX/UI Designer** - Interface e experiência do usuário

### Salários da equipe

A partir de pesquisas em sites especializados como Glassdoor, Robert Half e Pesquisa Salarial Código Fonte TV 2024, é possível chegar às médias salariais brasileiras dos cargos necessários. As seguintes médias foram consideradas:

| Cargo | Média salarial mensal (BRL) | Especialização |
|-------|----------------------------|----------------|
| Product Owner | 9.500 | Gestão de produto tech |
| Cientista de Dados/IA | 12.000 | Machine Learning e Computer Vision |
| Desenvolvedor Full-Stack (x2) | 8.500 | React, Node.js, Python |
| Desenvolvedor Mobile | 9.000 | Android/Kotlin, integrações |
| Engenheiro DevOps | 11.000 | Cloud, CI/CD, monitoramento |
| UX/UI Designer | 7.500 | Design de sistemas e interfaces |

Para a quantidade de pessoas de cada área e pelo período de 4 meses, o cálculo fica da seguinte forma:

```
Custo(equipe) = (9.500 + 12.000 + 8.500*2 + 9.000 + 11.000 + 7.500) * 4
Custo(equipe) = (9.500 + 12.000 + 17.000 + 9.000 + 11.000 + 7.500) * 4
Custo(equipe) = 66.000 * 4 = R$ 264.000,00
```

## Custos de Infraestrutura e Tecnologia

### Infraestrutura de TI

| Item | Descrição | Custo Mensal (R$) | Custo 4 meses (R$) |
|------|-----------|------------------|-------------------|
| Supabase Pro | Database, Auth, Storage | 150,00 | 600,00 |
| Servidor AI/ML | GPU para treinamento modelos | 800,00 | 3.200,00 |
| CDN e Storage | Armazenamento de imagens | 200,00 | 800,00 |
| Monitoramento | Logs, métricas, alertas | 100,00 | 400,00 |
| Backup e Segurança | Backup automatizado | 150,00 | 600,00 |

**Total Infraestrutura 4 meses: R$ 5.600,00**

### Licenças e Ferramentas

| Item | Descrição | Custo (R$) |
|------|-----------|------------|
| Licenças IDE | JetBrains, Visual Studio | 2.000,00 |
| Ferramentas AI/ML | MLflow, Weights & Biases | 1.500,00 |
| Design Tools | Figma Pro, Adobe Creative | 1.200,00 |
| Certificados SSL | Segurança do sistema | 500,00 |
| Ferramentas DevOps | Docker, Kubernetes | 800,00 |

**Total Licenças: R$ 6.000,00**

### Hardware e Equipamentos

| Item | Descrição | Custo (R$) |
|------|-----------|------------|
| Workstations | 7 estações de trabalho adequadas | 35.000,00 |
| Equipamentos de teste | Tablets, smartphones para testes | 8.000,00 |
| Equipamentos de rede | Switches, roteadores | 3.000,00 |

**Total Hardware: R$ 46.000,00**

## Custo Total da Solução Final

```
Custo(equipe + infraestrutura + licenças + hardware) = 264.000 + 5.600 + 6.000 + 46.000
Custo(equipe + infraestrutura + licenças + hardware) = R$ 321.600,00
```

### Custos gerais adicionais (30%)

Conforme especificado, aplicamos um adicional de 30% sobre os custos diretos para cobrir despesas gerais:

```
Custos gerais = 321.600,00 * 0,30 = R$ 96.480,00
```

## Incidência de impostos

A Classificação Nacional de Atividades Econômicas é um código utilizado para identificar quais são as atividades econômicas exercidas por uma empresa. O projeto da solução SOD pode se enquadrar no CNAE 6201-5/00 (Desenvolvimento de programas de computador sob encomenda), o que sujeita o negócio a diferentes impostos como PIS, COFINS, ISS, entre outros.

Para esta análise financeira, será considerado sobre o custo um imposto único, cujo valor será de **18%**.

```
Custo(com impostos) = (321.600,00 + 96.480,00) / (1 - 0,18)
Custo(com impostos) = 418.080,00 / 0,82 = R$ 509.853,66
```

## Custos de Manutenção (1 ano)

Para garantir o funcionamento adequado do sistema após a implementação, os seguintes custos anuais de manutenção devem ser considerados:

### Infraestrutura Recorrente (anual)

| Item | Custo Anual (R$) |
|------|------------------|
| Supabase Pro | 1.800,00 |
| Servidor AI/ML | 9.600,00 |
| CDN e Storage | 2.400,00 |
| Monitoramento | 1.200,00 |
| Backup e Segurança | 1.800,00 |
| **Total Infraestrutura** | **16.800,00** |

### Suporte e Manutenção

| Item | Descrição | Custo Anual (R$) |
|------|-----------|------------------|
| Suporte Técnico | 2 desenvolvedores meio período | 120.000,00 |
| Atualizações de Segurança | Patches e correções | 24.000,00 |
| Melhorias no modelo IA | Retreinamento e otimizações | 36.000,00 |
| Suporte ao usuário | Help desk e documentação | 18.000,00 |
| **Total Suporte** | | **198.000,00** |

**Total Manutenção Anual: R$ 214.800,00**

## Lucro

O lucro é um aspecto fundamental a ser considerado na análise financeira do projeto. É importante calcular o que se pretende faturar após os descontos, inclusive os tributos. A margem de lucratividade planejada para este projeto é de **20%**.

```
Valor final = (Desenvolvimento + Manutenção anual) * 1,20
Valor final = (509.853,66 + 214.800,00) * 1,20
Valor final = 724.653,66 * 1,20 = R$ 869.584,39
```

