---
sidebar_position: 6
custom_edit_url: null
---

# Diagramas de Sequência UML e Adaptação para a Produção

&emsp;Os diagramas de sequência UML são ferramentas visuais utilizadas para descrever como os objetos em um sistema interagem entre si ao longo do tempo. Eles são amplamente empregados para modelar o fluxo de mensagens ou eventos entre diferentes componentes de um sistema, ajudando a compreender e documentar o comportamento dinâmico de aplicações. Esses diagramas são especialmente úteis para identificar dependências, validar requisitos e planejar implementações, sendo uma parte importante para o processo de desenvolvimento de software.

## Funcionamento do Sistema (Em Desenvolvimento)
&emsp;Os diagramas de sequência descritos a seguir mostram como nosso sistema atual (que está em desenvolvimento) funcionará. Posteriormente, as tecnologias que terão que ser implementadas para colocar a solução em produção serão discutidas.

### Diagrama de Sequência do Web App

![Diagrama de Sequência do Web App](/img/diagramas-de-sequencia/web-app.svg)

&emsp;O diagrama acima apresenta o fluxo de funcionamento do Web App em ambiente de desenvolvimento. Neste cenário, o sistema está configurado para ser acessado localmente, utilizando um proxy de tunelamento para permitir o acesso externo de forma temporária.

* **Fluxo de Operação:**

  1. O usuário acessa o Web App através do navegador.
  2. O navegador se comunica com o Proxy de Tunelamento, que estabelece um canal seguro temporário.
  3. O Proxy encaminha a requisição ao servidor local.
  4. O servidor consulta o Banco de Dados, que também está em ambiente local.
  5. O Banco de Dados retorna os dados ao servidor.
  6. O servidor envia a resposta ao Proxy, que redireciona ao navegador.
  7. O navegador apresenta a resposta ao usuário.

### Diagrama de Sequência do Algoritmo de IA

![Diagrama de Sequência do Algoritmo de IA](/img/diagramas-de-sequencia/ia.svg)

&emsp;Este diagrama apresenta o fluxo de funcionamento do Algoritmo de IA em ambiente de desenvolvimento. O processamento é realizado diretamente na aplicação, e os dados são armazenados e consultados em um banco de dados local.

* **Fluxo de Geração de Relatório:**

  1. O usuário solicita o processamento de um novo relatório.
  2. A aplicação inicia o processamento com o Algoritmo de IA.
  3. O IA processa os dados e publica variáveis no Banco de Dados.
  4. O IA retorna os resultados para a aplicação.
  5. A aplicação apresenta os resultados ao usuário.

* **Fluxo de Recuperação de Relatório:**

  1. O usuário solicita a visualização de relatórios já gerados.
  2. A aplicação requisita os dados ao Banco de Dados.
  3. O Banco de Dados fornece os dados ao IA para processamento.
  4. O IA processa os dados e retorna os resultados para a aplicação.
  5. A aplicação apresenta os resultados ao usuário.

---

## Adaptação para o Ambiente de Produção

&emsp;Nesta seção, abordaremos como o sistema será adaptado para funcionar de forma segura, escalável e eficiente em produção, garantindo que o Web App e o Algoritmo de IA possam operar em um ambiente propriamente configurado.

### Servidor Proxy Reverso

&emsp;A Proxy de Tunelamento utilizado em desenvolvimento será substituído por um servidor proxy reverso (NGINX, Apache ou Cloudflare). O proxy reverso será responsável por:
  * **Proteção HTTPS:** Gerenciar certificados SSL/TLS (Let's Encrypt com renovação automática).
  * **Desempenho:** Realizar cache de conteúdo e balanceamento de carga.
  * **Segurança Adicional:** Atuar como um Web Application Firewall (WAF) para bloquear ataques de rede.
  * **Compatibilidade:** Suporte a IPv4 e IPv6 (Dual-Stack).

### Endereço IP Público
&emsp;Para que o Web App seja acessível na internet, será configurado um endereço IP público. Existem duas opções principais:

  * **IP Público Estático:** Um endereço IP fixo atribuído ao servidor, garantindo que o endereço não mude. Ideal para ambientes de produção.
  * **DNS Dinâmico:** Utilizado em casos onde o IP pode mudar, configurado com um serviço de DNS dinâmico (Cloudflare, AWS Route 53).

* Nos provedores de nuvem (AWS, Azure, Google Cloud):
  * O IP público geralmente é atribuído automaticamente, mas pode ser configurado como **IP estático (Elastic IP no AWS)**.
  * Suporte a **dual-stack (IPv4 e IPv6)**, garantindo compatibilidade com todas as redes.

### Banco de Dados
  * **Segurança:** Comunicação criptografada (TLS/SSL) e autenticação segura.
  * **Desempenho:** Backup automático, alta disponibilidade (Multi-AZ) e escalabilidade.
  * **Tipo de Banco de Dados:** SQL (PostgreSQL) para dados estruturados.
  * **Controle de Acesso:** Utilizando autenticação segura com **tokens JWT** (JSON Web Tokens) para usuários autenticados.
  * **Auditoria:** Registros de acesso e modificação de dados serão monitorados para segurança.

### Algoritmo de IA
&emsp;O Algoritmo de IA será executado em um **serviço de computação em nuvem (AWS SageMaker, Google AI Platform, Azure ML)**. Configurações para produção:

  * **Escalabilidade:** Configurado para lidar com múltiplas solicitações simultâneas (serviços serverless ou instâncias dedicadas).
  * **Treinamento Contínuo:** O modelo será versionado e re-treinado periodicamente com novos dados.
  * **Segurança:** Acesso controlado por autenticação segura (OAuth 2.0) e comunicação criptografada.
  * **Armazenamento de Dados:** Resultados e variáveis serão armazenados em um banco de dados seguro (SQL ou NoSQL).

### Fluxo em Produção do Web App
1. O usuário acessa o Web App em uma URL pública com HTTPS.
2. O servidor proxy reverso (NGINX, Cloudflare) recebe a requisição e aplica regras de segurança (WAF).
3. O proxy encaminha a requisição ao servidor de aplicação na nuvem.
4. O servidor consulta o Banco de Dados na nuvem de forma segura.
5. O Banco de Dados retorna os dados ao servidor.
6. O servidor processa a resposta e a envia de volta ao proxy reverso.
7. O proxy reverso entrega a resposta ao usuário.

### Fluxo em Produção da IA
1. O usuário acessa o Web App e realiza a autenticação segura (OAuth 2.0).
2. A aplicação envia uma solicitação ao servidor, que realiza a verificação do usuário.
3. O servidor aciona o serviço de IA na nuvem (AWS SageMaker, Azure ML).
4. O IA processa os dados recebidos e retorna os resultados.
5. O servidor armazena os resultados no banco de dados na nuvem.
6. O usuário visualiza os relatórios de forma segura no Web App.