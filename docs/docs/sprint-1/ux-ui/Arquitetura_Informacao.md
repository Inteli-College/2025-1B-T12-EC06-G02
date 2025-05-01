---
sidebar_position: 3
custom_edit_url: null
---

# Arquitetura da Informação

## Contexto

A arquitetura da informação é importante por seu papel de estruturar e organizar os conteúdos e funcionalidades de um sistema de forma clara que facilite a navegação e a compreensão por parte dos usuários. Em sistemas técnicos, como o de inspeção e análise de fissuras, essa organização é ajuda a garantir que os usuários encontrem rapidamente o que precisam, executem suas tarefas com precisão e mantenham o foco no objetivo principal: gerar relatórios técnicos confiáveis e precisos sobre as fissuras identificadas. Neste projeto, a arquitetura da informação foi pensada para refletir a lógica do trabalho de campo de técnicos e pesquisadores, organizando o fluxo desde o envio das imagens até a geração do relatório final. O resultado é um sistema intuitivo, funcional e preparado para o uso em ambiente local.

## Diagrama

A arquitetura da informação foi estruturada para garantir fluidez no fluxo de tarefas, clareza na navegação e controle total do usuário sobre os dados que estão sendo manipulados, com base na análise da arquitetura inicial do projeto, encontrada na seção que aborda o escopo técnico do projeto, e nas necessidades das personas, encontrada em um outro arquivo da seção de design centrado no usuário. Além disso, foi considerado que o sistema já utilizado pelo parceiro já contempla funcionalidades de armazenamento histórico, de modo que o escopo deste sistema local foca exclusivamente na inspeção, análise e geração de relatórios.

<p style={{textAlign: 'center'}}>Figura 1: Diagrama da Arquitetura da Informação</p>
<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/arquiteturaInfo.png").default} style={{width: 800}} alt="Imagem informativa de Mariana Ribeiro." />
        <br />
    </div>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

O ponto de entrada do sistema é a Tela Inicial, que apresenta duas funções principais: iniciar uma nova inspeção, acessar o relatório gerado. A funcionalidade de "Nova Inspeção" conduz o usuário por uma sequência organizada de tarefas, começando pelo preenchimento dos metadados da obra (nome da edificação, data da inspeção e observações relevantes). Em seguida, é realizado o upload das imagens capturadas das fachadas ou andares. O formulário exige que cada imagem seja associada a uma fachada específica (Norte, Sul, Leste ou Oeste) ou ao andar correspondente da edificação, permitindo assim uma segmentação espacial para uma leitura técnica e precisa, refletindo diretamente na distribuição das patologias identificadas para o relatório final.

Concluído o upload, as imagens são enviadas ao módulo local de Inteligência Artificial, que realiza a detecção de fissuras com base em um sistema treinado previamente para identificar padrões visuais relacionados a patologias construtivas. A IA também é responsável por classificar automaticamente as fissuras quanto à sua gravidade, com base em parâmetros como largura, extensão e distribuição. Cada imagem processada recebe uma nota de confiabilidade. Se a nota estiver acima de um limiar predefinido, a classificação é automaticamente aceita. Caso contrário, a imagem é destacada na interface para análise manual por parte do usuário.

A análise manual é um dos pontos fortes da arquitetura. A interface sinaliza visualmente as imagens com baixa acurácia, permitindo que o técnico ou pesquisador revise, confirme, corrija ou rejeite a classificação sugerida. A intenção com essa intervenção humana é garantir que o relatório final contenha apenas resultados validados, aumentando sua precisão e credibilidade.

Finalizado o processo de revisão (automático ou manual), o sistema gera automaticamente um relatório técnico, organizado por fachada e andar, contendo imagens com sobreposição de marcações, classificações atribuídas, observações complementares e dados da inspeção. A interface disponibiliza opções para visualização imediata ou download direto do arquivo.

Todo o conteúdo é organizado com base em uma estrutura hierárquica simples e intuitiva, com menus claros e rotulados em linguagem técnica, adaptada à rotina dos profissionais da área. O formulário de upload agrupa lógicamente os campos obrigatórios, enquanto o sistema de análise realiza a diferenciação das imagens com alta e baixa acurácia. Não há sobrecarga de informação ou elementos desnecessários, de forma a alcançar o resultado mais objetivo possível.

Importante destacar que não há funcionalidade de histórico incorporada neste sistema local, pois o sistema oficial utilizado pelo parceiro já contempla esse recurso. Dessa forma, este sistema atua de forma complementar e independente, mantendo foco na inspeção e análise pontual. O fluxo de informação respeita a ordem natural da tarefa dos usuários e garante controle, precisão e agilidade em todas as etapas do processo.

