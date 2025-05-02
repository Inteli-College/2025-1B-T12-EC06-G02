---
sidebar_position: 3
custom_edit_url: null
---

# Canvas Proposta de Valor

## Introdução

&nbsp;&nbsp;&nbsp;&nbsp;O Value Proposition Canvas é uma ferramenta fundamental para alinhar as necessidades dos clientes com a oferta de valor de um produto ou serviço. Desenvolvido por Alexander Osterwalder como complemento ao [Business Model Canvas](../analise-de-negocios/Business_Model_Canvas.md), este framework ajuda a estruturar e visualizar como uma solução resolve problemas específicos dos usuários. No contexto do projeto de desenvolvimento do algoritmo para processamento digital de imagens na identificação de fissuras em revestimentos de argamassa, o Value Proposition Canvas nos permite mapear claramente como a solução tecnológica proposta pelo IPT atenderá às necessidades dos demais [stakeholders](../analise-de-negocios/analise_de_stakeholder.md]), complementando a visão técnica detalhada nos [Requisitos Funcionais](../especificacoes-tecnicas/Requisitos_Funcionais.md) e [Requisitos Não Funcionais](../especificacoes-tecnicas/Requisitos_Nao_Funcionais.md).

<p style={{textAlign: 'center'}}>Figura 1 - Canvas Proposta de Valor</p>

<div style={{margin: 25}}>
    <div style={{textAlign: 'center'}}>
        <img src={require("../../../static/img/canvas-proposta-de-valor.png").default} style={{width: 800}} alt="Canva Proposta de valor" />
        <br />
    </div>
</div>

<p style={{textAlign: 'center'}}>Fonte: Os autores (2025)</p>

## Segmento de Clientes

### Perfil do Cliente
&nbsp;&nbsp;&nbsp;&nbsp;O lado direito do canvas representa o perfil do cliente e é composto por três seções principais que descrevem em detalhes quem são os usuários-alvo da solução. Esta caracterização está diretamente alinhada com as [Personas](../ux-ui/Personas.md) desenvolvidas para o projeto, fornecendo uma visão complementar dos mesmos stakeholders:

#### Quem São
- Empresas de construção civil e manutenção predial
- Engenheiros civis e técnicos de inspeção
- Consultorias de fiscalização de obras

Este perfil foi desenvolvido com base na [Análise de Stakeholders](../analise-de-negocios/analise_de_stakeholder.md), que identificou os principais interessados no projeto e suas respectivas necessidades.

#### Dores dos Clientes
&nbsp;&nbsp;&nbsp;&nbsp;As dores representam os problemas, obstáculos e riscos que os clientes enfrentam atualmente.

- Identificação tardia de fissuras que leva a danos estruturais maiores
- Custos elevados em manutenções corretivas quando problemas não são detectados precocemente
- Inspeções manuais imprecisas que dependem da experiência visual dos técnicos
- Ausência de histórico documentado da evolução das patologias
- Dificuldade em priorizar intervenções devido à falta de dados quantitativos

#### Ganhos Esperados
&nbsp;&nbsp;&nbsp;&nbsp;Os ganhos descrevem os benefícios e resultados positivos que os clientes desejam alcançar:

- Detecção automatizada e precisa de patologias estruturais
- Economia significativa em manutenções através de intervenções preventivas
- Aumento da segurança estrutural das edificações
- Melhor alocação de recursos de manutenção
- Decisões baseadas em dados concretos e análises técnicas

## Proposta de Valor

### Mapa de Valor
&nbsp;&nbsp;&nbsp;&nbsp;O lado esquerdo do canvas representa a proposta de valor e é composto por três seções que descrevem como o produto atende às necessidades identificadas. Esta proposta de valor se traduz em funcionalidades concretas, detalhadas na [Arquitetura Inicial](../especificacoes-tecnicas/Arquitetura_Inicial.md) do sistema:

#### Produtos e Serviços
&nbsp;&nbsp;&nbsp;&nbsp;Os principais elementos da solução que serão oferecidos, envolvendo interfaces e fluxos:

- Software de análise automática para identificação de fissuras
- Interface de visualização intuitiva para apresentação dos resultados
- Relatórios automatizados sobre o estado das patologias
- Sistema de alertas para casos críticos
- Banco de dados histórico para monitoramento da evolução

#### Criadores de Ganho
&nbsp;&nbsp;&nbsp;&nbsp;Aspectos da solução que geram os benefícios esperados pelos clientes:

- Algoritmos de IA especializados para detecção precisa
- Integração simplificada com drones e câmeras de alta resolução
- Classificação automatizada da gravidade das fissuras
- Capacidade de previsão da evolução das patologias
- Geração de relatórios técnicos customizáveis

#### Aliviadores de Dor
&nbsp;&nbsp;&nbsp;&nbsp;Elementos da solução que resolvem os problemas identificados:

- Redução significativa do tempo necessário para inspeções
- Detecção precoce de problemas estruturais antes de agravamento
- Monitoramento contínuo e sistemático das edificações
- Priorização eficiente de intervenções baseada em dados
- Minimização dos riscos associados a falhas estruturais

## Conclusão

&nbsp;&nbsp;&nbsp;&nbsp;O Value Proposition Canvas desenvolvido para o projeto de identificação de fissuras em edificações demonstra um claro alinhamento entre as necessidades do mercado da construção civil e a solução tecnológica proposta. A combinação de processamento digital de imagens com inteligência artificial apresenta potencial para transformar significativamente os processos de inspeção e manutenção predial, oferecendo ganhos tanto em eficiência operacional quanto em segurança estrutural.

&nbsp;&nbsp;&nbsp;&nbsp;A implementação deste projeto pelo IPT, com sua credibilidade e expertise de 125 anos no setor, representa uma oportunidade de introduzir uma inovação disruptiva no mercado brasileiro de manutenção predial. O desenvolvimento iterativo, começando com um MVP focado nas funcionalidades essenciais e evoluindo com base no feedback dos usuários, permitirá validar a proposta de valor na prática e realizar ajustes conforme necessário. Este processo de desenvolvimento está alinhado com os cenários de uso representados nas [User Stories](../ux-ui/User_Stories.md).

## Referências Bibliográficas
&nbsp;&nbsp;&nbsp;&nbsp;Osterwalder, A., Pigneur, Y., Bernarda, G., & Smith, A. (2014). Value Proposition Design: How to Create Products and Services Customers Want. John Wiley & Sons.