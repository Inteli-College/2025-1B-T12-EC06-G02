---
sidebar_position: 1
slug: /sprint-4/seguranca-usabilidade
description: "Explicação da segurança e responsividade do sistema"
---

# Segurança e Usabilidade

&emsp; Esta seção apresenta as melhorias implementadas nos aspectos de **segurança** e **usabilidade** da plataforma. No tocante à segurança, foi adicionada a exigência de autorização para acesso às páginas da aplicação, conforme definido no requisito não funcional [RNF11](../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md). Quanto à usabilidade, a equipe SOD aprimorou a responsividade da interface, o tratamento de erros e a clareza na comunicação do estado atual do sistema ao usuário.

## Segurança

&emsp; Até as etapas iniciais do desenvolvimento, as páginas da aplicação estavam acessíveis sem qualquer tipo de restrição, bastando conhecer a URL da rota desejada para acessá-la, mesmo sem autenticação. Essa abordagem visava acelerar o desenvolvimento das funcionalidades principais, reduzindo a fricção durante testes e iterações.

&emsp; Contudo, com a aproximação da entrega final do projeto, foi implementado um sistema completo de controle de acesso. A proteção agora ocorre **em dois níveis**, sendo aplicada tanto no **front-end** quanto no **back-end**. A principal verificação se dá no servidor, por meio de um _middleware_ que intercepta todas as requisições às rotas protegidas.

&emsp; Este _middleware_ realiza uma verificação inicial quanto à presença de um token de autenticação do Supabase nos cookies do usuário. Em seguida, o token é validado com base na chave pública da plataforma. Caso o token esteja ausente ou inválido, a aplicação retorna um erro HTTP **401 - Não autorizado**, bloqueando o acesso indevido de forma eficiente.

&emsp; Com essa implementação, a aplicação passa a atender plenamente ao requisito [RNF11](../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md), elaborado com base na norma ISO/IEC 25010 no que diz respeito à **confidencialidade** e **autenticidade**. As métricas de desempenho definidas — como o tempo de resposta inferior a 2 segundos para acessos negados — foram plenamente atendidas em testes realizados em dois dispositivos distintos.

## Usabilidade

### Responsividade

&emsp; A norma ISO/IEC 25010 também define que sistemas devem ser adaptáveis a diferentes ambientes e plataformas. Até esta sprint, o sistema apresentava um desempenho razoável apenas em telas com largura entre 800 e 1200 pixels. Em telas menores, diversos problemas eram observados: o botão de _logout_ se tornava inacessível, textos ultrapassavam os limites dos botões, e o download de relatórios era dificultado. Esses problemas estavam inicialmente justificados pelo escopo original do sistema, pensado como uma aplicação _desktop-only_.

&emsp; No entanto, conforme documentado na seção [Atualizações do Aplicativo de Controle do Drone](../aplicativo-e-integracao-com-o-drone/Atualizacoes_App.md), identificou-se a necessidade de uso da plataforma em dispositivos móveis, principalmente para envio de imagens capturadas localmente pelos drones. A partir disso, foi criado o requisito [RNF09](../../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md), voltado à responsividade da plataforma.

::: info[Informação]
As métricas desse requisito serão detalhadas na seção de Testes e Validação. Esta seção descreve apenas como as exigências foram incorporadas ao sistema.
:::

&emsp; Apesar de o projeto não ter sido concebido sob a arquitetura _mobile-first_, foram feitas adaptações nas principais telas para suportar larguras entre 600 e 800 pixels. As telas adaptadas incluem: **home**, **histórico**, **envio de imagens** e **resultados**. As comparações entre a responsividade mobile no passado e agora estão disponíveis abaixo.

<p style={{textAlign: 'center'}}>Figura 1: Comparação Home</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/comparacoes/comparacao-home.png").default} style={{width: 800}} alt="Comparação entre a tela de home sem responsividade (à esquerda) e com responsividade (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 2: Comparação Histórico</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/comparacoes/comparacao-historico.png").default} style={{width: 800}} alt="Comparação entre a tela de histórico sem responsividade (à esquerda) e com responsividade (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 3: Comparação Upload</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/comparacoes/comparacao-upload.png").default} style={{width: 800}} alt="Comparação entre a tela de upload sem responsividade (à esquerda) e com responsividade (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 4: Comparação Resultados</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/comparacoes/comparacao-results.png").default} style={{width: 800}} alt="Comparação entre a tela de resultados sem responsividade (à esquerda) e com responsividade (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### Melhorias nas Heurísticas

&emsp; Com relação à usabilidade, o desenvolvimento da interface seguiu as heurísticas de Nielsen, fundamentais para garantir uma boa experiência do usuário (Moma, 2017). Nesta sprint, deu-se ênfase especial à **prevenção de erros**, conforme a heurística 5, segundo a qual "Boas mensagens de erro são importantes, mas os melhores designs previnem cuidadosamente que os problemas ocorram" (Nielsen, 1994).

&emsp; Especificamente, foram feitas melhorias no fluxo de envio de imagens. Primeiramente, evitou-se o envio de conjuntos vazios de imagens para organização. Em seguida, o sistema passou a impedir o envio de imagens não alocadas em grupos para análise. Para isso, botões de ação foram desabilitados até que as condições corretas fossem atendidas, como ilustrado abaixo:

<p style={{textAlign: 'center'}}>Figura 5: Usabilidade nos botões</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/usabilidade.png").default} style={{width: 800}} alt="Demonstração de usabilidade com os botões desabilitados na tela de uploads (à esquerda) e na tela de organização de imagens (à direita)" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>
<small style={{textAlign: 'center'}}>Legenda: À esquerda, tela de envio de imagens com o botão "Organizar e Processar" desabilitado até que o usuário insira imagens. À direita, tela de organização, com o botão "Iniciar processamento" desabilitado até que todas as imagens sejam alocadas.</small>

&emsp; Além disso, em casos onde não foi possível evitar o erro, aplicou-se a recomendação complementar da heurística: verificar e apresentar ao usuário uma opção de confirmação antes da ação (Nielsen, 1994). Isso foi implementado na exclusão de imagens já enviadas para organização, conforme ilustrado na Figura 3, onde é solicitado um diálogo de confirmação ao usuário.

<p style={{textAlign: 'center'}}>Figura 6: Prevenção de Erros</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/usabilidade-1.png").default} style={{width: 800}} alt="A imagem mostra uma caixa de diálogo para o usuário confirmar se deseja realmente deletar uma imagem" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

:::info[Informação]
Seguindo boas práticas de usabilidades, a SOD previniu ainda mais o deslize do usuário colocar o botão de confirmação ('Sim') à esquerda, com cor vermelha e sem preenchimento, para reduzir sua atratividade visual.
:::

## Conclusão

&emsp; As melhorias implementadas nesta sprint consolidam a evolução da plataforma tanto em termos de **segurança** quanto de **usabilidade**. O sistema agora está protegido contra acessos não autorizados, atendendo aos princípios de segurança estabelecidos pela norma ISO/IEC 25010. Além disso, adaptações significativas foram feitas na interface para garantir uma experiência mais fluida, responsiva e intuitiva — especialmente em dispositivos com telas menores. O uso das heurísticas de Nielsen guiou decisões de design centradas no usuário, reforçando o compromisso da equipe SOD com a qualidade e confiabilidade da solução.


## Bibliografia

NIELSEN, J. 10 Heuristics for User Interface Design. Disponível em: https://www.nngroup.com/articles/ten-usability-heuristics/. 

MOMA, G. 10 heurísticas de Nielsen para o design de interface. Disponível em: https://brasil.uxdesign.cc/10-heur%C3%ADsticas-de-nielsen-para-o-design-de-interface-58d782821840. 






