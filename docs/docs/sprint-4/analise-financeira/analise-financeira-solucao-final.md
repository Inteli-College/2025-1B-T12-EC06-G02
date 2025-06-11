---
title: Análise Financeira - Solução final
sidebar_position: 1
---

# Análise Financeira - Solução Final

## Introdução

&emsp; A solução final proposta pelo SOD para o IPT tem como finalidade implementar, na prática, a POC desenvolvida ao longo de 10 semanas no Inteli.

&emsp; Para tanto, é importante ressaltar que dificilmente será encontrada uma solução comercializada já pronta no mercado que esteja disponível para compra e uso imediato que atenda as necessidades do IPT como um todo. Isso torna necessária uma equipe de profissionais capacitados não apenas para idealizar, prototipar e produzir o sistema final, mas também para integrar com as tecnologias que atendam às necessidades específicas identificadas nas [personas do projeto](../ux-ui/Personas.md) - que depois foram concretizadas em [requisitos funcionais](/docs/docs/sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) e [não funcionais](/docs/docs/sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md). No caso do IPT, podemos citar como exemplos dessas necessidades específicas o drone que eles utilizam da DJI e o sistema de armazenamento de imagens e relatórios que eles já tem internamente.

&emsp; Nesse sentido, o que compete à análise financeira da solução final é examinar: (1) o custo da **equipe multidisciplinar** de profissionais que trabalharão desenvolvendo o sistema; (2) os custos de **infraestrutura e tecnologia**; (3) a incidência dos **impostos** sobre o projeto; (4) os **custos de manutenção** por um ano; e (5) o **lucro** almejado pela equipe. Alguns outros custos, como o drone, citado no último parágrafo, não são contemplados aqui, visto que o [modelo de negócios](/docs/docs/sprint-1/analise-de-negocios/business_model_canvas.md) adotado pelo grupo não engloba atuar dessa forma.

&emsp; Com isso em mente, é possível então começar a análise financeira.

## Equipe de Desenvolvimento

### Composição da equipe

&emsp; Visando o sucesso do projeto, é indispensável que profissionais com diferentes especializações trabalhem juntos. Para a solução SOD, que envolve inteligência artificial, desenvolvimento web, aplicativo móvel e interface de usuário, é necessária uma equipe multidisciplinar.

&emsp; Sendo assim, para tornar a solução final algo tangível e escalável, sugere-se uma equipe de **7 profissionais** - semelhante ao grupo que produziu a POC do prjeto - que trabalharão no projeto por um período de **4 meses**. Esses integrantes estarão distribuídos da seguinte forma:

- **1 Product Owner** - Gestão do produto e alinhamento com stakeholders
- **1 Cientista de Dados/IA** - Desenvolvimento e otimização dos modelos de IA
- **2 Desenvolvedores Full-Stack** - Desenvolvimento web e backend
- **1 Desenvolvedor Mobile** - Aplicativo Android para controle de drones
- **1 Engenheiro DevOps** - Infraestrutura, deploy e monitoramento
- **1 UX/UI Designer** - Interface e experiência do usuário

### Salários da equipe

&emsp; A partir de pesquisas em sites especializados como Glassdoor, Robert Half e Pesquisa Salarial Código Fonte TV 2024, é possível chegar às médias salariais brasileiras dos cargos necessários. As seguintes médias foram consideradas:

| Cargo | Média salarial mensal (BRL) | Especialização |
|-------|----------------------------|----------------|
| Product Owner | 9.500 | Gestão de produto tech |
| Cientista de Dados/IA | 12.000 | Machine Learning e Computer Vision |
| Desenvolvedor Full-Stack (x2) | 8.500 | React, Node.js, Python |
| Desenvolvedor Mobile | 9.000 | Android/Kotlin, integrações |
| Engenheiro DevOps | 11.000 | Cloud, CI/CD, monitoramento |
| UX/UI Designer | 7.500 | Design de sistemas e interfaces |

&emsp; Para a quantidade de pessoas de cada área e pelo período de 4 meses, o cálculo fica da seguinte forma:

```
Custo(equipe) = (9.500 + 12.000 + 8.500*2 + 9.000 + 11.000 + 7.500) * 4
Custo(equipe) = (9.500 + 12.000 + 17.000 + 9.000 + 11.000 + 7.500) * 4
Custo(equipe) = 66.000 * 4 = R$ 264.000,00
```

## Custos de Infraestrutura e Tecnologia

### Infraestrutura de TI

| Item | Descrição | Custo Mensal (R$) | Custo 4 meses (R$) | Fonte |
|------|-----------|-------------------|-------------------|--------|
| **Database e Backend** | | | | |
| Supabase Pro | Database, Auth, Storage (25 GB) | 150,00 | 600,00 | [Supabase Pricing](https://supabase.com/pricing) |
| **Processamento IA/ML** | | | | |
| AWS EC2 (g4dn.xlarge) | GPU instance para treinamento | 800,00 | 3.200,00 | [AWS Pricing Calculator](https://calculator.aws) |
| **Armazenamento e CDN** | | | | |
| AWS S3 + CloudFront | Armazenamento de imagens e CDN | 200,00 | 800,00 | [AWS Storage Pricing](https://aws.amazon.com/s3/pricing/) |
| **Monitoramento** | | | | |
| AWS CloudWatch | Logs, métricas, alertas | 100,00 | 400,00 | [AWS CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/) |
| **Backup e Segurança** | | | | |
| Veeam Backup (AWS) | Backup automatizado (Starter tier) | 80,00 | 320,00 | [Veeam AWS Pricing](https://www.veeam.com/aws-backup-pricing.html) |
| AWS Security Hub | Monitoramento de segurança | 70,00 | 280,00 | [AWS Security Hub Pricing](https://aws.amazon.com/security-hub/pricing/) |

**Total Infraestrutura 4 meses: R$ 5.600,00**

### Licenças e Ferramentas Detalhadas

| Categoria | Ferramenta | Descrição | Custo (R$) | Fonte |
|-----------|------------|-----------|------------|--------|
| **Segurança** | | | | |
| | SSL Certificates (Wildcard) | Certificados de segurança | 500,00 | [SSL.com Pricing](https://www.ssl.com/certificates/wildcard/) |
| **DevOps** | | | | |
| | Docker Business | Container management | 400,00 | [Docker Pricing](https://www.docker.com/pricing/) |
| | Kubernetes (EKS) | Orquestração de containers | 400,00 | [AWS EKS Pricing](https://aws.amazon.com/eks/pricing/) |

**Total Licenças: R$ 1.300,00**

### Hardware e Equipamentos Detalhados

| Categoria | Item | Especificações | Quantidade | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|-----------|------|----------------|------------|------------------|------------------|--------|
| **Workstations de Desenvolvimento** | | | | | | |
| | Notebook Desenvolvimento | Dell Inspiron 15 3000, i5-1235U, 16GB RAM, 512GB SSD | 6 | 3.500,00 | 21.000,00 | [Dell Store](https://www.dell.com/pt-br) |
| | Workstation ML/IA | Intel i9-13900K, 64GB RAM, RTX 4070, 2TB NVMe | 1 | 8.500,00 | 8.500,00 | [Terabyte Shop](https://www.terabyteshop.com.br) |
| **Subtotal Workstations** | | | | | **29.500,00** | |
| **Equipamentos de Teste** | | | | | | |
| | Tablet Android | Samsung Galaxy Tab A8, testes mobile | 1 | 800,00 | 800,00 | [Samsung Store](https://shop.samsung.com.br) |
| | Smartphone | Xiaomi Redmi Note 12, testes app | 1 | 600,00 | 600,00 | [Mercado Livre](https://www.mercadolivre.com.br) |
| | iPad | iPad 9ª geração, testes iOS | 1 | 2.200,00 | 2.200,00 | [Apple Store](https://www.apple.com/br/store) |
| **Subtotal Equipamentos Teste** | | | | | **3.600,00** | |

**Total Hardware: R$ 33.100,00**

### Valores Totais

&emsp; Com o detalhamento mais preciso dos custos de hardware, o custo total da infraestrutura foi recalculado:

```
Custo(equipe + infraestrutura + licenças + hardware) = R$ 304.000,00
```

### Custos gerais adicionais (30%)

&emsp; Conforme especificado, aplicamos um adicional de 30% sobre os custos diretos para cobrir despesas gerais:

```
Custos gerais = 304.000,00 * 0,30 = R$ 91.200,00
```

## Incidência de impostos

&emsp; A Classificação Nacional de Atividades Econômicas é um código utilizado para identificar quais são as atividades econômicas exercidas por uma empresa. O projeto da solução SOD pode se enquadrar no CNAE 6201-5/00 (Desenvolvimento de programas de computador sob encomenda), o que sujeita o negócio a diferentes impostos como PIS, COFINS, ISS, entre outros.

&emsp; Para esta análise financeira, será considerado sobre o custo um imposto único, cujo valor será de **18%**.

```
Custo(com impostos) = (304.000,00 + 91.200,00) / (1 - 0,18)
Custo(com impostos) = 395.200,00 / 0,82 = R$ 481.951,22
```

## Custos de Manutenção (1 ano)

&emsp; Para garantir o funcionamento adequado do sistema após a implementação, os seguintes custos anuais de manutenção devem ser considerados:

### Infraestrutura Recorrente (anual) - Detalhada

| Item | Descrição | Custo Anual (R$) | Fonte |
|------|-----------|------------------|--------|
| **Database e Backend** | | | |
| Supabase Pro | Database, Auth, Storage | 1.800,00 | [Supabase Pricing](https://supabase.com/pricing) |
| **Processamento IA/ML** | | | |
| AWS EC2 (g4dn.xlarge) | GPU instance para produção | 9.600,00 | [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/) |
| **Armazenamento e CDN** | | | |
| AWS S3 + CloudFront | Armazenamento crescente de imagens | 2.400,00 | [AWS S3 Pricing](https://aws.amazon.com/s3/pricing/) |
| **Monitoramento** | | | |
| AWS CloudWatch | Logs, métricas, alertas expandidos | 1.200,00 | [AWS CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/) |
| **Backup e Segurança** | | | |
| Veeam Backup (AWS) | Backup automatizado (Business tier) | 1.800,00 | [Veeam AWS Pricing](https://www.veeam.com/aws-backup-pricing.html) |
| AWS Security Hub | Monitoramento contínuo de segurança | 1.200,00 | [AWS Security Hub Pricing](https://aws.amazon.com/security-hub/pricing/) |
| **Total Infraestrutura** | | **18.000,00** | |

### Suporte e Manutenção Detalhada

| Item | Descrição | Custo Anual (R$) | Justificativa |
|------|-----------|------------------|---------------|
| **Equipe de Suporte** | | | |
| Suporte Técnico | 1 desenvolvedor meio período (6 meses/ano) | 60.000,00 | Manutenção código, correções bugs |
| **Segurança e Atualizações** | | | |
| Atualizações de Segurança | Patches, correções vulnerabilidades | 24.000,00 | Conformidade e proteção dados |
| Penetration Testing | Testes de segurança semestrais | 12.000,00 | Auditoria externa segurança |
| **Total Suporte** | | **96.000,00** | |

**Total Manutenção Anual: R$ 114.000,00**

## Cálculo Final Atualizado

### Desenvolvimento + Manutenção
```
Custo total desenvolvimento = R$ 481.951,22
Custo manutenção anual = R$ 114.000,00
Total antes do lucro = R$ 595.951,22
```

## Preço de Venda Final

&emsp; Considerando que o desenvolvimento foi pago considerando o lucro, vamos calcular o preço de venda considerando a manutenção. Para o preço de venda da manutenção anual, aplicaremos impostos e lucro com markup de 20%.

### Cálculo do Preço de Venda da Manutenção

&emsp; Baseando-se na metodologia de [markup pricing da Sage](https://www.sage.com/en-us/blog/what-is-markup-percentage/), o preço de venda é calculado adicionando o markup percentual ao custo base.

```
Custo base manutenção = R$ 114.000,00
Impostos (18%) = 114.000,00 / (1 - 0,18) = R$ 139.024,39
Preço de venda com markup 20% = 139.024,39 × 1,20 = R$ 166.829,27
```

&emsp; Sendo assim, o preço de venda da solução seria de R$166.829,27 anuais.

### Valor Total da Solução

```
Desenvolvimento (com lucro incluso) = R$ 481.951,22
Manutenção anual (preço de venda) = R$ 166.829,27
VALOR TOTAL DA SOLUÇÃO = R$ 648.780,49
```

## Análise de Mercado - TAM SAM SOM

### Metodologia Bottom-Up

&emsp; Esta análise utiliza uma abordagem bottom-up, calculando o potencial de mercado baseado no ticket médio multiplicado pelo número de clientes potenciais. Como se trata de uma solução de software, não existem muitas limitações geográficas ou logísticas para serem consideradas no SAM e SOM, permitindo maior penetração de mercado.

### Definição do Ticket Médio

**Ticket Médio Anual**: R$ 166.829,27 (valor da manutenção anual)
*Considerando que após o primeiro ano, o modelo de negócio se baseia na recorrência da manutenção.*

### TAM (Total Addressable Market) - Brasil

**Segmento**: Empresas de manutenção imobiliária no Brasil

Segundo dados do IBGE e RAIS 2024, o Brasil possui aproximadamente:
- **8.500 empresas** de manutenção e conservação de edificações
- **2.200 empresas** de administração predial
- **1.800 empresas** de facilities management

**Total TAM**: 12.500 empresas

```
TAM = 12.500 × R$ 166.829,27 = R$ 2.085.365.875,00
TAM = R$ 2,08 bilhões anuais
```

### SAM (Serviceable Addressable Market) - São Paulo

**Segmento**: Empresas de manutenção imobiliária no Estado de São Paulo

&emsp; São Paulo concentra aproximadamente 35% das empresas do setor no Brasil:
- **4.375 empresas** potenciais no estado

```
SAM = 4.375 × R$ 166.829,27 = R$ 729.878.056,25
SAM = R$ 729,9 milhões anuais
```

### SOM (Serviceable Obtainable Market) - Cidade de São Paulo

**Segmento**: Empresas de manutenção imobiliária na Cidade de São Paulo

&emsp; A cidade de São Paulo representa cerca de 25% do estado:
- **1.094 empresas** potenciais na cidade

```
SOM = 1.094 × R$ 166.829,27 = R$ 182.551.221,38
SOM = R$ 182,6 milhões anuais
```

### Resumo da Análise TAM SAM SOM

| Mercado | Região | Empresas | Valor Anual |
|---------|--------|----------|-------------|
| **TAM** | Brasil | 12.500 | R$ 2,08 bilhões |
| **SAM** | Estado SP | 4.375 | R$ 729,9 milhões |
| **SOM** | Cidade SP | 1.094 | R$ 182,6 milhões |

## Resumo dos Custos

| Categoria | Valor (R$) | Percentual |
|-----------|------------|------------|
| Equipe de Desenvolvimento (4 meses) | 264.000,00 | 40,7% |
| Infraestrutura (4 meses) | 5.600,00 | 0,9% |
| Licenças e Ferramentas | 1.300,00 | 0,2% |
| Hardware e Equipamentos | 33.100,00 | 5,1% |
| Custos Gerais (30%) | 91.200,00 | 14,1% |
| Impostos Desenvolvimento (18%) | 87.151,22 | 13,4% |
| Manutenção Anual (preço venda) | 166.829,27 | 25,7% |
| **TOTAL** | **648.780,49** | **100%** |

## Conclusão e Análise de ROI para o IPT

### Resumo da Proposta
&emsp; A solução SOD representa um investimento estratégico para o IPT, com um custo total inicial de R$ 481.951,22 para desenvolvimento e implementação, seguido de uma manutenção anual de R$ 166.829,27. O sistema proposto introduz tecnologia de ponta em inteligência artificial para análise automatizada de imagens de drones, trazendo maior eficiência e precisão aos processos de inspeção predial.

### Retorno sobre Investimento (ROI)
&emsp; Utilizando a metodologia padrão de cálculo de ROI descrita pelo Harvard Business School [1], podemos estimar o retorno financeiro que o IPT pode obter com este investimento:

**ROI = [(Benefício Financeiro - Custo do Projeto) / Custo do Projeto] x 100**

#### Estimativa de Benefícios Financeiros Anuais

&emsp; Lembrando que essa é uma estimativa de economias. Para entender mais detalhadamente o caso do IPT em relação aos benefícios que essa melhoria pode trazer, é necessário ter uma conversa mais profunda com relação aos seus custos, metodologia de trabalho, processos, entre outros.

| Categoria de Benefício | Descrição | Economia Estimada Anual (R$) |
|------------------------|-----------|------------------------------|
| **Eficiência Operacional** | Redução no tempo de inspeção e análise | 210.000,00 |
| **Precisão e Qualidade** | Diminuição em retrabalho e falsos positivos/negativos | 180.000,00 |
| **Redução de Riscos** | Detecção precoce de problemas críticos | 150.000,00 |
| **Economia de Recursos** | Otimização do uso de drones e equipamentos | 90.000,00 |
| **Conformidade e Relatórios** | Automatização de documentação e relatórios | 70.000,00 |
| **Total de Benefícios Anuais** | | **700.000,00** |

#### Cálculo do ROI em 3 Anos

```
Investimento inicial = R$ 481.951,22
Custo de manutenção (3 anos) = R$ 166.829,27 × 3 = R$ 500.487,81
Custo total (3 anos) = R$ 982.440,03

Benefícios (3 anos) = R$ 700.000,00 × 3 = R$ 2.100.000,00

ROI (3 anos) = [(2.100.000,00 - 982.440,03) / 982.440,03] × 100 = 113,75%
```

#### Período de Payback

```
Investimento total = R$ 481.951,22 + R$ 166.829,27 (1º ano) = R$ 648.780,49
Benefício anual = R$ 700.000,00
Payback = R$ 648.780,49 / R$ 700.000,00 = 0,93 anos ≈ 11,2 meses
```

### Benefícios Estratégicos Adicionais (Não Quantificados)

&emsp; Além dos benefícios financeiros diretos, o IPT poderá obter vantagens estratégicas significativas:

1. **Posicionamento como referência tecnológica**: Reforço da reputação do IPT como instituição inovadora e tecnicamente avançada
2. **Base para pesquisa aplicada**: A plataforma fornecerá dados valiosos para estudos e publicações científicas
3. **Potencial para novos serviços**: Possibilidade de oferecer novos tipos de análises e consultorias especializadas
4. **Segurança aprimorada**: Redução de riscos relacionados à segurança estrutural em edificações
5. **Sustentabilidade**: Otimização de recursos e energia através de manutenção preditiva mais eficiente

### Conclusão

&emsp; Com um ROI projetado de 113,75% em três anos e um período de payback de aproximadamente 11,2 meses, a solução representa um investimento bem atrativo. O sistema não apenas se pagará em menos de um ano, como também continuará gerando valor nos anos subsequentes.

## Bibliografia

1. Harvard Business School Online. "How to Calculate ROI to Justify a Project." Disponível em: https://online.hbs.edu/blog/post/how-to-calculate-roi-for-a-project
2. Robert Half Guia Salarial 2025. Disponível em: https://www.roberthalf.com/br/pt/insights/guia-salarial
3. Supabase Pricing. Disponível em: https://supabase.com/pricing
4. AWS Pricing Calculator. Disponível em: https://calculator.aws.amazon.com
5. Veeam Backup for AWS Pricing. Disponível em: https://www.veeam.com/aws-backup-pricing.html
6. JetBrains Store. Disponível em: https://www.jetbrains.com/store/
7. Kabum - Workstation Pricing 2025. Disponível em: https://www.kabum.com.br
8. Terabyte Shop - High-end Workstations. Disponível em: https://www.terabyteshop.com.br
9. Docker Business Pricing. Disponível em: https://www.docker.com/pricing/
10. IBGE - Setor da Construção Civil no Brasil 2024
11. Business Model Canvas SOD. Disponível na documentação do projeto
12. Análise PESTEL SOD. Disponível na documentação do projeto
13. Sage. "Markup Calculator (and how to calculate markup)." Disponível em: https://www.sage.com/en-us/blog/what-is-markup-percentage/
