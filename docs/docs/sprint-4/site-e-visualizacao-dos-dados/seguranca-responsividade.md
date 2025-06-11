---
sidebar_position: 1
slug: /sprint-4/seguranca-usabilidade
description: "Explicação da segurança e responsividade do sistema"
---

# Segurança e Usabilidade

&emsp; Esta seção apresenta as melhorias implementadas nos aspectos de **segurança** e **usabilidade** da plataforma. No tocante à segurança, foi adicionada a exigência de autorização para acesso às páginas da aplicação, conforme definido no requisito não funcional [RNF11](../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md). Quanto à usabilidade, a equipe SOD aprimorou a responsividade da interface, o tratamento de erros e a clareza na comunicação do estado atual do sistema ao usuário.

## Segurança

&emsp; Até o presente estágio do desenvolvimento, visando facilitar o progresso das funcionalidades principais, as páginas da aplicação não possuíam restrições de acesso. Bastava conhecer a URL de qualquer rota para navegar livremente entre as páginas, mesmo sem autenticação. Essa abordagem visava reduzir fricções durante o desenvolvimento e os testes.

&emsp; Contudo, com a aproximação da entrega final do projeto, foi implementado um sistema completo de autorização. A proteção agora ocorre de forma **dupla**, sendo aplicada tanto no **front-end** quanto no **back-end**. A principal verificação ocorre no servidor, por meio de um _middleware_ que intercepta todas as requisições às páginas protegidas.

&emsp; Este _middleware_ realiza uma checagem inicial pela presença de um token de login do Supabase nos cookies do usuário. Em seguida, valida o token utilizando a chave pública do Supabase. Caso o token esteja ausente ou inválido, a aplicação responde com um erro HTTP **401 - Não autorizado**, impedindo o acesso indevido.

&emsp; Com essa implementação, a aplicação passa a atender plenamente ao requisito [RNF11](../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md). As métricas de desempenho estabelecidas — como o tempo de resposta inferior a 2 segundos em acessos negados — foram satisfatoriamente atingidas em testes realizados em dois computadores distintos.








