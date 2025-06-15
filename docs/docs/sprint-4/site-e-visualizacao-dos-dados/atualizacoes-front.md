---
sidebar_position: 2
slug: /sprint-4/atualizacoes-front
description: "Novas funcionalidades implementadas no frontend"
---

# Novas Features do Frontend

&emsp; Esta seção apresenta as principais **novas funcionalidades** implementadas no frontend da plataforma durante a Sprint 4. Além das melhorias de segurança e usabilidade documentadas na seção [Segurança e Usabilidade](./seguranca-usabilidade), foram desenvolvidas duas features essenciais que atendem diretamente às necessidades identificadas pelo parceiro: o **Sistema de Projetos** e o **Sistema de Organização por Drag and Drop**.

&emsp; Essas funcionalidades foram projetadas para resolver dores específicas relatadas durante as interações com o parceiro, especialmente a necessidade de organizar rachaduras por andar e direção, permitindo maior controle e precisão na análise dos dados coletados pelos drones.

## Sistema de Projetos

&emsp; Uma das principais demandas identificadas durante o desenvolvimento foi a necessidade de organizar os trabalhos de análise de forma mais estruturada. Até então, todas as análises eram processadas de forma isolada, sem agrupamento ou contexto organizacional, dificultando o controle e acompanhamento de múltiplas inspeções.

&emsp; Para resolver essa questão, foi implementado um **Sistema de Projetos** completo, que permite aos usuários criar, organizar e gerenciar diferentes projetos de inspeção de forma centralizada. Cada projeto funciona como um contêiner que agrupa todas as análises relacionadas a uma edificação ou conjunto de edificações específicas.

### Funcionalidades do Sistema de Projetos

&emsp; O sistema oferece as seguintes funcionalidades principais:

- **Criação de Projetos**: Os usuários podem criar novos projetos fornecendo informações como nome, descrição, número identificador, CEP, CNPJ e endereço completo
- **Listagem Organizada**: Todos os projetos são exibidos em uma interface limpa e organizada, mostrando informações essenciais e data de criação
- **Associação de Análises**: Cada análise de imagens realizada fica automaticamente associada ao projeto selecionado
- **Contexto Geográfico**: Integração com dados de localização para melhor organização territorial dos projetos

## Sistema de Organização por Drag and Drop

&emsp; A segunda funcionalidade implementada foi o **Sistema de Organização por Drag and Drop**, desenvolvido especificamente para atender uma dor crítica identificada pelo parceiro: a necessidade de separar e categorizar rachaduras por andar e direção durante a análise.

&emsp; Este sistema redefine a forma como as imagens são organizadas antes do processamento, oferecendo uma interface intuitiva e visual que permite aos usuários agrupar imagens de acordo com critérios específicos de localização dentro da edificação.

### Funcionalidades do Drag and Drop

&emsp; O sistema de organização oferece uma experiência completa de manipulação de imagens:

#### Interface Inicial de Três Colunas
- **Primeira Coluna**: Exibe todas as imagens enviadas para upload, prontas para organização
- **Segunda Coluna**: Visualização detalhada do grupo selecionado com suas imagens organizadas
- **Terceira Coluna**: Botão de "+" para criação de novas colunas

#### Criação Dinâmica de Grupos
- Os usuários podem criar quantos grupos desejarem
- Cada grupo pode ser nomeado e categorizado por **andar** e **direção** (Norte, Sul, Leste, Oeste, etc.)

#### Funcionalidades Avançadas de Seleção
- **Seleção Múltipla com Shift**: Permite selecionar um intervalo contínuo de imagens
- **Seleção Individual com Ctrl**: Permite selecionar imagens específicas não contíguas
- **Arrastar e Soltar**: Interface intuitiva para mover imagens entre grupos
- **Reorganização**: Possibilidade de mover imagens entre diferentes grupos após a organização inicial

### Impacto na Geração de Relatórios

&emsp; A organização realizada através do sistema de drag and drop tem impacto na geração dos relatórios finais. Cada grupo criado pelos usuários é considerado durante o processamento das análises, permitindo que os relatórios finais sejam mais específicos por micro regiões.

## Próximos Passos e Melhorias Futuras

&emsp; Com base no feedback contínuo do parceiro e do nosso orientador na experiência de uso das novas funcionalidades, foram identificadas algumas oportunidades de melhoria para a próxima sprint:

### Melhorias no Drag and Drop
- **Campo de Andar Opcional**: Tornar o campo de seleção de andar opcional, pois é provável que uma imagem seja capaz de capturar mais do que apenas um pavimento, oferecendo maior flexibilidade na categorização

## Conclusão

&emsp; As funcionalidades implementadas nesta sprint representam um avanço na capacidade da plataforma de atender às necessidades específicas do parceiro. O **Sistema de Projetos** oferece a organização estrutural necessária para gerenciar múltiplas inspeções, enquanto o **Sistema de Organização por Drag and Drop** resolve diretamente a dor identificada de categorização por localização.

&emsp; Essas implementações, combinadas com as melhorias de segurança e usabilidade, consolidam a plataforma como uma solução robusta e user-friendly para inspeção de rachaduras em edificações. A atenção aos detalhes de usabilidade, como as funcionalidades de seleção múltipla e a interface intuitiva, demonstra o compromisso da equipe SOD em entregar uma experiência de usuário excepcional.

&emsp; Os próximos passos identificados garantem que a plataforma continue evoluindo de acordo com as necessidades reais dos usuários, mantendo sempre o foco na qualidade, precisão e facilidade de uso que caracterizam a solução desenvolvida.