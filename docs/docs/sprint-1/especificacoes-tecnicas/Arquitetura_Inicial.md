---
sidebar_position: 3
custom_edit_url: null
---

# Arquitetura Inicial

Apresenta a proposta arquitetural do sistema, descrevendo os módulos principais, suas responsabilidades, as interfaces entre componentes e as tecnologias previstas, acompanhada de diagramas explicativos.

```mermaid
flowchart TB
    %% Dispositivos físicos
    subgraph "Componentes Físicos"
        drone("Drone/Robô")
        camera("Câmera")
        drone --- camera
    end

    %% Sistema de IA
    subgraph "IA de Detecção Rachaduras"
        ia["Processamento de Imagens"]
        detect["Detecção de Fissuras"]
        classify["Classificação de Gravidade"]
        ia --> detect --> classify
    end

    %% Armazenamento
    db[(Database)]

    %% Interface
    subgraph "Website"
        subgraph "Backend"
            api["API"]
            proc["Processador de Dados"]
            control["Sistema de Controle do Robô"]
            api --- proc
            api --- control
        end
        
        subgraph "Frontend"
            ui["Interface do Usuário"]
            reports["Gerador de Relatórios"]
            alerts["Sistema de Alertas"]
            robotControl["Interface de Controle do Robô"]
            ui --- reports
            ui --- alerts
            ui --- robotControl
        end
        
        Backend <---> Frontend
    end

    %% Fluxo de dados
    camera -->|"Imagens"| api
    api -->|"Dados para Análise"| ia
    classify -->|"Resultados"| proc
    proc <--->|"Armazenamento/Consulta"| db
    proc -->|"Dados Processados"| ui
    
    %% Fluxo de controle do robô
    control <-->|"Comandos de Controle"| drone
    robotControl -->|"Instruções de Operação"| control
```