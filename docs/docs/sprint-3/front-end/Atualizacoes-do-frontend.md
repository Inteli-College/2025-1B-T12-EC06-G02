# Fluxo do usuário na interfase

## Introdução

&emsp; Esta documentação descreve o fluxo de uso da plataforma de análise de imagens, que permite aos usuários identificar e classificar rachaduras em fotografias. Nesse sentido, o processo é composto por quatro etapas principais: primeiramente, o Cadastro e Login, onde o usuário pode criar uma conta ou aceder à plataforma; em seguida, a Home, que apresenta as opções de carregar imagens do dispositivo local ou selecionar do servidor; posteriormente, o Upload, fase em que as imagens são efetivamente selecionadas e submetidas ao modelo para identificação e classificação das fissuras, e, por fim, a página de Resultados, que exibe as conclusões da análise realizada pelo modelo. Dessa forma, segue a descrição de cada etapa desse fluxo.

## 1. Cadastro e login

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

## 2. Home

&emsp; Após um login bem-sucedido, o usuário acede à página Home, que funciona como o ponto central para dar início ao processo de análise de imagens. Nesta secção, são apresentadas ao usuário duas opções fundamentais para o carregamento das fotografias: efetuar o upload a partir do armazenamento local do seu dispositivo ou selecionar imagens que já se encontram armazenadas no servidor. 

<div align="center" width="100%">

<sub>Figura 3 - Tela home</sub>

![Tela home](/img/telaHome.png)

<sup>Fonte: Autoria própria </sup>

</div>

## 3. Upload

&emsp; Seguindo a escolha feita na home, a etapa de upload permite ao usuário selecionar as imagens específicas que deseja analisar. Se a opção selecionada foi 'upload local', a interface apresentará um mecanismo para que o usuário navegue pelos diretórios do seu dispositivo e selecione um ou mais arquivos de imagem . Caso a opção tenha sido 'carregar do servidor', a interface deverá exibir uma galeria das imagens disponíveis no servidor, permitindo ao usuário marcar aquelas que serão processadas. Após a seleção das imagens, independentemente da origem, o usuário confirma a sua escolha.

<div align="center" width="100%">

<sub>Figura 3 - Tela upload</sub>

![Tela upload](/img/telaUpload.png)

<sup>Fonte: Autoria própria </sup>

</div>

## 4. Resultados

&emsp; Após o processamento das imagens pelo modelo, o usuário é direcionado para a página de resultados, onde são exibidas as conclusões da análise. Esta página apresenta as imagens originais acompanhadas das classificações das rachaduras detectadas, especificando a quantidade de rachaduras classificadas como de retração e térmicas.

<div align="center" width="100%">

<sub>Figura 3 - Tela resultados</sub>

![Tela resultados](/img/telaResultados.png)

<sup>Fonte: Autoria própria </sup>

</div>