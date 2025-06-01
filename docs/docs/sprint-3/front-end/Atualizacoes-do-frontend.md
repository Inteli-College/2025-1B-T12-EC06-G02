# Fluxo do usuário na interface

## Introdução

&emsp; Esta documentação descreve o fluxo de uso da plataforma de análise de imagens, que permite aos usuários identificar e classificar rachaduras em fotografias. Nesse sentido, o processo é composto por quatro etapas principais: primeiramente, o Cadastro e Login, onde o usuário pode criar uma conta ou aceder à plataforma; em seguida, a Home, que apresenta as opções de carregar imagens do dispositivo local ou selecionar do servidor; posteriormente, o Upload, fase em que as imagens são efetivamente selecionadas e submetidas ao modelo para identificação e classificação das fissuras, e, por fim, a página de Resultados, que exibe as conclusões da análise realizada pelo modelo. Dessa forma, segue a descrição de cada etapa desse fluxo.

### 1. Cadastro e login

&emsp; A etapa inicial de interação com a plataforma envolve o acesso através da tela de login. O usuário deve inserir o seu email e senha nos campos correspondentes. Caso ainda não possua uma conta, é necessário realizar o cadastro na plataforma; após este processo, um email de confirmação é enviado e, uma vez confirmado, a conta torna-se ativa. Ao submeter as credenciais de login, se a autenticação for bem-sucedida, o usuário será redirecionado para a página Home. Contudo, se as credenciais forem inválidas, será exibida uma mensagem de erro informativa, oferecendo ao usuário a possibilidade de tentar novamente ou de solicitar a recuperação da senha.

<div align="center" width="100%">

<sub>Figura 1 - Tela cadastro</sub>

![Tela cadastro](/img/telaCadastro.png)

<sup>Fonte: Autoria própria </sup>

</div>

<div align="center" width="100%">

<sub>Figura 2 - Tela login</sub>

![Tela login](/img/telaLogin.png)

<sup>Fonte: Autoria própria </sup>

</div>

### 2. Home

&emsp; Após um login bem-sucedido, o usuário acede à página Home, que funciona como o ponto central para dar início ao processo de análise de imagens. Nesta secção, são apresentadas ao usuário duas opções fundamentais para o carregamento das fotografias: efetuar o upload a partir do armazenamento local do seu dispositivo ou selecionar imagens que já se encontram armazenadas no servidor. 

<div align="center" width="100%">

<sub>Figura 3 - Tela home</sub>

![Tela home](/img/telaHome.png)

<sup>Fonte: Autoria própria </sup>

</div>

### 3. Upload

&emsp; Seguindo a escolha feita na home, a etapa de upload permite ao usuário selecionar as imagens específicas que deseja analisar. Se a opção selecionada foi 'upload local', a interface apresentará um mecanismo para que o usuário navegue pelos diretórios do seu dispositivo e selecione um ou mais arquivos de imagem . Caso a opção tenha sido 'carregar do servidor', a interface deverá exibir uma galeria das imagens disponíveis no servidor, permitindo ao usuário marcar aquelas que serão processadas. Após a seleção das imagens, independentemente da origem, o usuário confirma a sua escolha.

<div align="center" width="100%">

<sub>Figura 3 - Tela upload</sub>

![Tela upload](/img/telaUpload.png)

<sup>Fonte: Autoria própria </sup>

</div>

### 4. Resultados

&emsp; Após o processamento das imagens pelo modelo, o usuário é direcionado para a página de resultados, onde são exibidas as conclusões da análise. Esta página apresenta as imagens originais acompanhadas das classificações das rachaduras detectadas, especificando a quantidade de rachaduras classificadas como de retração e térmicas.

<div align="center" width="100%">

<sub>Figura 3 - Tela resultados</sub>

![Tela resultados](/img/telaResultados.png)

<sup>Fonte: Autoria própria </sup>

</div>

## Funcionalidades complementares

&emsp; Além das funcionalidades apresentadas anteriormente no fluxo básico do usuário, foi identificado que a experiência do usuário poderia ser significativamente enriquecida com o desenvolvimento de funcionalidades complementares. Durante o processo de análise de uso e definição dos [requisitos](/docs/docs/sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), observou-se que algumas necessidades adicionais não estavam sendo plenamente contempladas no escopo inicial da aplicação.

&emsp; Entre essas necessidades, destacam-se a possibilidade de acesso a um histórico de relatórios gerados, e a visualização prévia dos relatórios gerados pela plataforma. Assim, conseguimos não só garantir mais controle do usuário, como também contribuimos para a rastreabilidade dos dados e a verificação dos resultados antes de sua utilização final.

&emsp; Assim, com o objetivo de oferecer uma solução mais robusta, intuitiva e funcional, foram desenvolvidas as seguintes telas e recursos complementares:

### 1. Tela de Histórico

&emsp; A "Tela de Histórico" permite ao usuário consultar os registros dos relatórios que ja foram gerados anteriormente no sistema. Essa funcionalidade promove a rastreabilidade das ações realizadas, facilitando o acompanhamento da evolução dos dados ao longo do tempo e do acesso ao mesmo caso necessário, evitando que o usuário precise gerar o mesmo relatório duas vezes. Para acessar a tela de histórico, é preciso que o usuário clique no botão "Histórico", que pode ser encontrado na tela inicial, e sera redirecionado para o acesso ao histórico.

<div align="center" width="100%">

<sub>Figura 4 - Tela Histórico</sub>

![Tela Histórico](/img/historico.png)

<sup>Fonte: Autoria própria </sup>

</div>


### 2. Preview do Relatório

&emsp; O recurso de "Preview do Relatório" permite que o usuário visualize o conteúdo do relatório assim que gerado, junto com a opção de exportação do mesmo. Assim, permite-se a revisão dos dados, verificação de formatações, é possível identificar possíveis inconsistências ou erros, e garantir que o conteúdo está de acordo com as expectativas ou padrões desejados, facilitando também o acesso a versão final do relatório. Para acessar essa funcionalidade, o usuário deve clicar no botão "Preview do Relatório", que está presente na tela de resultados do sistema, e assim abrirá uma pagina com o relatório gerado.

<div align="center" width="100%">

<sub>Figura 4 - Tela Histórico</sub>

![Preview do Relatório](/img/preview.png)

<sup>Fonte: Autoria própria </sup>

</div>

&emsp; É importante destacar que, na imagem apresentada, o relatório ainda não está em sua versão final, uma vez que o desenvolvimento final do layout do relatório não constava no escopo de desenvolvimento da Sprint 3. Logo, a imagem representa a demonstração da funcionalidade apenas.

## Conclusão

&emsp; O fluxo principal do usuário no sistema, composto pelas etapas de cadastro, navegação na home, upload de imagens, mandar para o nosso modelo de IA e a visualização dos resultados, cobre o essencial para a realização da tarefa de identificação e classificação de fissuras na fachada dos predios, gerando relatórios e resultados satisfatórios para o usuário. Porem, analisando o funcionamento do sistema e as necessidades do usuário, a expansão das funcionalidades da plataforma era essencial para a evolução e progresso do sistema, uma vez que as mesmas alterações ampliam as possibilidades de uso da ferramenta e fortalecem sua confiabilidade e valor prático.

&emsp; Com isso, a plataforma evolui de uma solução básica de processamento de imagens para um sistema mais completo e adaptável, alinhado às necessidades reais de seus usuários e aos padrões de qualidade esperados em aplicações de análise automatizada. Etapas futuras poderão contemplar o refinamento visual dos relatórios, melhorias na performance do sistema e integração com outros módulos de apoio à decisão, garantindo a continuidade do aprimoramento da ferramenta.