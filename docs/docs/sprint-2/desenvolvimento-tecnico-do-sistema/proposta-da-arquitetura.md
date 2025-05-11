---
sidebar_position: 1
custom_edit_url: null
---

# Atualizações na Arquitetura

## Atualização da Arquitetura da Solução

&emsp; Na seção da [arquitetura inicial](/docs/docs/sprint-1/especificacoes-tecnicas/Arquitetura_Inicial.md), foi apresentada uma proposta para a estrutura da solução no estágio inicial do projeto. No entanto, com o avanço do entendimento das necessidades do sistema e a inclusão de novas funcionalidades, tornou-se necessária a atualização da arquitetura. A principal motivação para essa reestruturação foi a introdução do drone como fonte automatizada para a coleta de imagens.

&emsp; A arquitetura atual foi reorganizada em três blocos principais: front-end, servidor e dispositivos de captura de imagens O *front-end* abrange toda a interface com a qual o usuário interage, destacando-se os seguintes módulos: envio de imagens — sejam capturadas pelo drone ou por outros dispositivos —, visualização de relatórios gerados e acesso ao sistema de alertas em casos críticos. Além disso, o sistema permite a auditoria de casos em que a predição apresenta resultado inferior a 75%.

```mermaid

flowchart TB

 subgraph Drone["Drone"]
  end
 subgraph API["API REST"]
  end
 subgraph Modelo["Modelo"]
  end
 subgraph Gerar_Relatorios["Gerar Relatorios"]
  end
 subgraph Relatorio["Visualização dos relatórios"]
  end
 subgraph Upload["Upload das imagens"]
  end

 subgraph FrontEnd["Interfase do usuário"]

        Relatorio
        Upload
  end
  

 subgraph subGraph4["Servidor"]
        API
        Modelo
        Gerar_Relatorios
        db[("Database")]
  end
    Drone -- Upload das imagens --> API
    API -- Input dos dados --> Modelo
    Modelo -- Output dos dados --> Gerar_Relatorios & db
    Gerar_Relatorios <-- Armazenar/consultar os dados --> db
    API --> db
    API <-- Requisições / Respostas --> FrontEnd
    Gerar_Relatorios --> Relatorio

```

&emsp; O servidor foi segmentado em três módulos independentes:

* **API**: responsável pela mediação das requisições e pelo armazenamento dos dados;

* **Modelo**: executa o processamento das imagens e a análise por meio de inteligência artificial;

* **Geração de Relatórios**: organiza os resultados de forma compreensível para o usuário final.

&emsp; Todos os módulos do servidor se conectam a uma base de dados central, que funciona como repositório unificado das informações do sistema.

&emsp; Portanto, a atualização da arquitetura proporcionou avanços nos aspectos de integração, automação e organização do sistema, com enfâse para a integração de drones na coleta de imagens. Assim, essas mudanças são essenciais para a continuidade e evolução do projeto.

## Atualização da Arquitetura da Informação

&emsp; Anteriormente, a arquitetura da solução era composta por um fluxo de inspeção segmentado em três etapas principais: inserção de metadados, upload de imagens e análise técnica. O preenchimento dos metadados (local, data, observações) e o envio das imagens eram realizados manualmente pelo usuário. Além disso, não havia integração com APIs para armazenamento centralizado das informações, o que limitava a escalabilidade e dificultava a persistência estruturada dos dados. A visualização de relatórios era possível com opções básicas de download, sem a disponibilização de um histórico consolidado das inspeções anteriores.

<div align="center" width="100%">

<sub>Figura 1 - Arquitetura da informação atualizada</sub>

![Arquitetura da informação atualizada](/img/arquiteturaInfoSprint2.png)

<sup>Fonte: Autoria própria </sup>

</div>

&emsp; Com a arquitetura atualizada, o fluxo da funcionalidade de "Nova Inspeção" foi completamente reestruturado, passando a ser dividido em três etapas principais: inserção de metadados, upload das imagens e validação automatizada. No entanto, a nova solução passou a integrar APIs específicas para o armazenamento eficiente das informações em banco de dados. Além disso,  para garantir a confiabilidade dos resultados, a arquitetura contempla um mecanismo no qual as imagens são encaminhadas para análise manual por técnicos em casos em que o sistema identifica baixa acurácia nas previsões do modelo. Por fim, a interface de relatórios foi aprimorada com a inclusão de um histórico de inspeções, permitindo acesso contínuo e organizado aos registros anteriores.