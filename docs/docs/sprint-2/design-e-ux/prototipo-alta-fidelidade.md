---
sidebar_position: 1
custom_edit_url: null
---

# Protótipo de Alta Fidelidade do Sistema

## Visão Geral do Projeto

&emsp;Este documento apresenta o protótipo de alta fidelidade desenvolvido para o Sistema Óptico de Detecção (SOD), elaborado no Figma para guiar as funcionalidades do sistema. Este protótipo visual define a interface de usuário para uma solução de detecção e monitoramento automatizado de fissuras em revestimentos de argamassa em fachadas de edifícios, utilizando processamento digital de imagens e inteligência artificial.

&emsp;O protótipo de alta fidelidade estabelece as diretrizes visuais e funcionais que orientarão o desenvolvimento técnico posterior, garantindo que a solução final atenda às necessidades específicas dos usuários.

### 🎨 [Clique aqui](https://www.figma.com/design/e0U9SYE12jTbnNo0Vsk5wH/SOD--Prot%C3%B3tipo-de-Alta-Fidelidade?node-id=40-2&t=Bu3nD0T638fHJHYe-1) para acessar o Figma do projeto

## Design Centrado nas Personas

A interface foi projetada considerando as necessidades específicas de nossas duas principais [personas](../../sprint-1/ux-ui/Personas.md):

### Para Mariana Ribeiro (Pesquisadora)

Como pesquisadora sênior com doutorado em Engenharia de Materiais, Mariana necessita:
- Precisão técnica e confiabilidade nos diagnósticos
- Sistematização da análise de fissuras
- Rastreabilidade dos dados para pesquisas longitudinais
- Padronização de relatórios técnicos

### Para Carlos Eduardo (Técnico de Edificações)

Como técnico experiente em inspeção e monitoramento, Carlos necessita:
- Agilidade no processamento de grande volume de imagens
- Facilidade na geração de relatórios automáticos
- Interface intuitiva para uso em campo
- Automação da identificação de problemas estruturais

## Fluxo de Navegação e Interfaces

### 1. Tela de Login

&emsp;A tela de login foi projetada com simplicidade para acesso rápido por ambas as personas, oferecendo segurança sem comprometer a eficiência.

**Benefícios para Mariana:** Acesso seguro aos dados de pesquisa com credenciais específicas.

**Benefícios para Carlos:** Entrada rápida no sistema durante inspeções em campo.

<p style={{textAlign: 'center'}}>Figura 1: Tela de login</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/TeladeLogin.png").default} style={{width: 800}} alt="Tela de login" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 2: Tela de Cadastro</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/TeladeCadastro.png").default} style={{width: 800}} alt="Tela de Cadastro" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### 2. Tela Inicial (Home)

&emsp;A home page apresenta as funcionalidades mais utilizadas por ambas as personas, com design intuitivo e foco nas tarefas principais.

**Benefícios para Mariana:** Acesso direto ao histórico para análise comparativa de dados.

**Benefícios para Carlos:** Conexão rápida com drone e upload de imagens para otimizar o trabalho em campo.

<p style={{textAlign: 'center'}}>Figura 3: Home Page</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Home-Page-Inicial.png").default} style={{width: 800}} alt="Home page" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### 3. Tela de Upload de Imagens e seleção de I.A.

&emsp;Interface que permite tanto o upload manual quanto a captura em tempo real via drone, com visualização imediata das imagens, além de possibilitar ao usuário selecionar o modelo de inteligência artificial para realizar a análise das imagens.

**Benefícios para Mariana:** Organização sistemática das imagens para análise científica e autonomia para escolha do modelo de inteligência artificial desejado.

**Benefícios para Carlos:** Visualização rápida das capturas e processamento imediato, reduzindo o tempo de inspeção.

#### 3.1. Upload Manual de Imagens

&emsp;A Figura 4 apresenta a interface da página inicial do sistema, que confere ao usuário total autonomia para realizar o upload de múltiplas imagens simultaneamente, sem qualquer limitação quanto à quantidade de arquivos. Esta funcionalidade permite que, caso o usuário possua um banco de imagens pré-existente, todos os arquivos possam ser carregados facilmente no sistema para posterior geração de relatórios analíticos.

<p style={{textAlign: 'center'}}>Figura 4: Home Page com funcionalidade de upload manual de imagens</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Home-Page-Com-Upload.png").default} style={{width: 800}} alt="Home page com upload de imagens" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025).</p>

#### 3.2. Integração com Drone

&emsp;Conforme ilustrado na Figura 5, quando o sistema está conectado ao drone, as fotografias capturadas pelo equipamento são transmitidas e integradas em tempo real à interface do usuário. As imagens são automaticamente adicionadas ao campo de preenchimento da página inicial. Uma vez que o usuário considere suficiente a quantidade de imagens obtidas, pode prosseguir diretamente para o processamento, não sendo necessário desconectar o drone antes de acionar o botão "Iniciar processamento".

<p style={{textAlign: 'center'}}>Figura 5: Home Page com imagens capturadas via integração com drone</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Home-page-conectada-ao-drone.png").default} style={{width: 800}} alt="Home Page com upload de imagens realizadas por conexão com o drone" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025).</p>

#### 3.3. Seleção de Modelo de Inteligência Artificial

&emsp;A Figura 6 demonstra como o sistema proporciona ao usuário completa autonomia para selecionar, dentre os modelos de inteligência artificial disponíveis, aquele que melhor atende às suas necessidades analíticas. O processamento será realizado utilizando o modelo especificamente selecionado pelo usuário, garantindo assim resultados personalizados de acordo com as características particulares de cada análise.

<p style={{textAlign: 'center'}}>Figura 6: Interface de seleção de modelo de inteligência artificial</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Home-Page-Com-Seleção-de-IA.png").default} style={{width: 800}} alt="Seleção de inteligência artificial desejada" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025).</p>

### 4. Tela de Auditoria de Imagens

&emsp;Interface que exibe imagens cujo processamento automatizado não atingiu o limiar mínimo de 75% de acurácia, permitindo avaliação individual pelo usuário. Esta etapa garante a qualidade da análise, combinando a automação com a expertise humana.

**Benefícios para Mariana:** Controle de qualidade científico sobre o processo automatizado, possibilitando ajustes metodológicos e validação técnica dos resultados.

**Benefícios para Carlos:** Capacidade de aplicar sua experiência prática para casos ambíguos, garantindo que seu conhecimento técnico agregue valor onde a automação encontra limitações.

<p style={{textAlign: 'center'}}>Figura 7: Tela de auditoria de imagem</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Processodeauditoria.png").default} style={{width: 800}} alt="Tela de auditoria de imagens" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 8: Processo de auditoria de uma imagem</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Analiseminunciosa.png").default} style={{width: 800}} alt="Tela de auditoria de uma imagem" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### 5. Tela de Insights e Relatório

&emsp;Esta interface apresenta informações técnicas categorizadas, atendendo à necessidade de precisão diagnóstica.

**Benefícios para Mariana:** Categorização científica das fissuras (retração, térmicas) permitindo análises aprofundadas e comparativas.

**Benefícios para Carlos:** Visualização direta e quantitativa dos problemas identificados, facilitando a elaboração de recomendações técnicas.

<p style={{textAlign: 'center'}}>Figura 9: Tela de insights do relatório</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Insightsdorelatorio.png").default} style={{width: 800}} alt="Tela de insights do relatório" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### 6. Tela de Conexão com Drone

&emsp;Interface simplificada para conexão com dispositivos de captura, atendendo à necessidade de inspeções remotas.

**Benefícios para Mariana:** Padronização da captura de imagens para maior consistência nas análises.

**Benefícios para Carlos:** Acesso remoto a áreas de difícil inspeção manual, aumentando a segurança e eficiência.

<p style={{textAlign: 'center'}}>Figura 10: Tela de conexão com o drone</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/ConectandocomoDrone.png").default} style={{width: 800}} alt="Figura 8: Tela de conexão com o drone" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 11: Sucesso na conexão com o drone</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Sucessonaconexao.png").default} style={{width: 800}} alt="Figura 8: Tela de sucesso na conexão com o drone" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

<p style={{textAlign: 'center'}}>Figura 12: Falha na conexão com o drone</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Falhanacomunicacao.png").default} style={{width: 800}} alt="Figura 8: Tela de falha na conexão com o drone" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

### 7. Tela de Histórico de Relatórios

&emsp;Interface que permite acesso organizado a todos os relatórios anteriormente gerados pelo sistema, apresentando-os em ordem cronológica com data e hora precisas para fácil identificação.

**Benefícios para Mariana:** Acesso estruturado a relatórios datados com precisão, permitindo correlacionar resultados com diversas variáveis, essencial para estabelecer padrões científicos de evolução das fissuras.

**Benefícios para Carlos:** Acesso rápido aos relatórios mais recentes, com possibilidade de download imediato através dos ícones intuitivos, otimizando o tempo em campo e facilitando a apresentação de dados durante visitas técnicas aos clientes.

<p style={{textAlign: 'center'}}>Figura 13: Tela de histórico de relatórios</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/wireframe/Abadehistorico.png").default} style={{width: 800}} alt="Tela de histórico de relatórios" />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

## Principais Funcionalidades Projetadas

### Automação da Análise de Imagens

**Impacto para Mariana:** Redução do tempo dedicado à análise manual, permitindo foco na interpretação avançada dos resultados e em pesquisas mais aprofundadas.

**Impacto para Carlos:** Eliminação da necessidade de análise manual de extensos conjuntos de imagens, aumentando sua produtividade em campo.

### Sistema de Auditoria com Limiar de Acurácia

**Impacto para Mariana:** Garantia de rigor científico ao estabelecer um mecanismo de validação para casos onde o algoritmo apresenta menor confiança, mantendo a integridade metodológica da pesquisa.

**Impacto para Carlos:** Combinação ideal entre eficiência e confiabilidade, permitindo intervenção humana apenas nos casos realmente necessários, otimizando seu tempo em campo.

### Categorização Padronizada

**Impacto para Mariana:** Sistematização da classificação de fissuras, garantindo consistência entre diferentes análises e estudos longitudinais.

**Impacto para Carlos:** Maior precisão nos diagnósticos técnicos, fortalecendo a confiabilidade de seus relatórios e recomendações.

### Geração Automática de Relatórios

**Impacto para Mariana:** Padronização dos relatórios técnicos, facilitando a comparação entre estudos e a publicação de resultados científicos.

**Impacto para Carlos:** Redução drástica do tempo dedicado à elaboração de documentação, permitindo atender mais clientes e projetos.

## Conclusão

&emsp;O protótipo de alta fidelidade desenvolvido no Figma para o Sistema Óptico de Detecção representa um guia visual e funcional completo para o desenvolvimento da solução final. Este protótipo materializa a visão de uma ferramenta que integra as necessidades específicas tanto da pesquisadora Mariana Ribeiro quanto do técnico Carlos Eduardo, estabelecendo uma ponte entre o rigor científico e a praticidade operacional.

&emsp;As funcionalidades projetadas através deste protótipo de alta fidelidade incluem automação de análise de imagens com sistema de auditoria para casos de baixa acurácia, categorização padronizada de fissuras, geração automática de relatórios e monitoramento longitudinal: elementos essenciais para transformar a experiência de ambas as personas.

&emsp;O sistema de auditoria com limiar de 75% de acurácia representa um diferencial, pois combina a eficiência da automação com a expertise técnica humana, garantindo resultados confiáveis mesmo em casos de difícil interpretação algorítmica.

&emsp;Este protótipo de alta fidelidade estabelece as bases para o desenvolvimento de uma solução digital que pode transformar os processos de inspeção predial, integrando as necessidades de diferentes perfis profissionais em uma interface coesa e eficiente.