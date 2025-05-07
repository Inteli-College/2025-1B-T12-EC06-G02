---
sidebar_position: 2
custom_edit_url: null
---

# Especificações Técnicas da Identidade Visual

## Introdução

Este documento apresenta as especificações técnicas de design da solução, complementando o [protótipo de alta fidelidade](./prototipo-alta-fidelidade.md) desenvolvido no [Figma](https://www.figma.com/design/e0U9SYE12jTbnNo0Vsk5wH/SOD--Prot%C3%B3tipo-de-Alta-Fidelidade?node-id=40-2&t=Bu3nD0T638fHJHYe-1). Estas diretrizes foram cuidadosamente elaboradas para garantir consistência visual e funcional durante o desenvolvimento, atendendo às necessidades das personas identificadas no projeto.

## Tipografia

Todo o sistema utiliza a família tipográfica **Inter**, escolhida por sua excelente legibilidade em diferentes tamanhos e por seu design neutro e contemporâneo, ideal para interfaces técnicas.

| Elemento | Fonte | Estilo/Força | Utilização |
|----------|-------|--------------|------------|
| Títulos | Inter | Semi Bold | Cabeçalhos e títulos principais |
| Placeholders | Inter | Italic | Campos de formulário e áreas de input |
| Botões | Inter | Medium | Textos em elementos interativos |
| Texto de conteúdo | Inter | Regular | Corpo de texto e conteúdo geral |

### Escalas Tipográficas

- **H1**: 24px/32px
- **H2**: 20px/28px
- **H3**: 18px/24px
- **Texto de parágrafo**: 16px/24px
- **Texto secundário**: 14px/20px
- **Texto de botão**: 16px/24px
- **Placeholder**: 14px/20px
- **Caption**: 12px/16px

## Paleta de Cores

A paleta de cores foi cuidadosamente selecionada para refletir profissionalismo e confiabilidade, atributos essenciais para um sistema técnico de diagnóstico.

| Cor | Código Hexadecimal | Utilização |
|-----|-------------------|------------|
| Azul Principal | #2D608D | Cor primária da identidade visual, utilizada em cabeçalhos, botões principais e elementos de destaque |
| Branco | #FFFFFF | Fundo das telas e texto sobre áreas coloridas |
| Verde | #00C939 | Feedbacks positivos, confirmações e indicadores de sucesso |
| Vermelho | #FF0004 | Alertas, erros e indicadores de falha |

### Variações de Cor

- **Azul Escuro** (hover): #245179
- **Azul Claro** (background secundário): #EAF2F8
- **Cinza Escuro** (texto principal): #333333
- **Cinza Médio** (texto secundário): #666666
- **Cinza Claro** (bordas, separadores): #DDDDDD

## Elementos de Interface

### Botões

- **Bordas**: Arredondamento de 5px em todos os botões

### Caixas e Painéis

- **Efeito Visual**: Background Blur aplicado em painéis flutuantes e modais
- **Bordas**: Arredondamento de 5px
- **Sombras**: Leve elevação com sombra suave (8px blur, 2px y-offset, opacidade 15%)

### Imagens de Background

O sistema utiliza imagens de topos de prédios sem direitos autorais como background nas demais áreas da aplicação. Estas imagens passam por um tratamento de opacidade (sobreposição com cor branca a 85% de opacidade) para não interferir na legibilidade do conteúdo. As imagens foram selecionadas de bancos gratuitos e passaram por processo de otimização para garantir carregamento rápido.

## Princípios de Design

O design do SOD segue princípios claros que devem ser mantidos durante o desenvolvimento:

1. **Hierarquia Visual**: Informações críticas sempre em destaque
2. **Consistência**: Elementos similares mantêm aparência e comportamento idênticos
3. **Feedback Imediato**: Toda ação do usuário recebe feedback visual claro
4. **Acessibilidade**: Contraste adequado entre texto e fundo (mínimo AA WCAG)
5. **Responsividade**: Adaptação a diferentes tamanhos de tela, com breakpoints em 768px e 1280px

## Conclusão

Este documento de identidade visual e especificações técnicas serve como referência para a implementação do protótipo de alta fidelidade do Sistema Óptico de Detecção. Seguindo estas diretrizes, garantimos a consistência visual e funcional da aplicação, proporcionando uma experiência de usuário otimizada tanto para pesquisadores quanto para técnicos de campo.

As especificações aqui documentadas resultam da análise das necessidades específicas das personas identificadas e do contexto de uso da aplicação, tendo sido validadas através de testes de usabilidade preliminares durante a fase de prototipação.