---
sidebar_position: 2
slug: /entrega-final/solucao
---

# Solução

&emsp; Em vias de resolver o problema descrito acima, criou-se o Sistema de Detecção de Fissuras da SOD. Retomando a introdução dessa documentação:

> "Um sistema para a detecção de fissuras em edificações que utiliza técnicas avançadas de processamento de imagens e inteligência artificial para identificar fissuras, permitindo manutenções preventivas e aumentando a segurança das edificações."

&emsp; Destrincharemos abaixo o significado desse resumo da solução em três partes:
- Sistema para Detecção de Fissuras;
- Processamento de imagem e IA
- Resultados do Sistema

## Sistema para Detecção de Fissuras

&emsp; Na primeira sprint do projeto, definiu-se os [requisitos funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md) e [não funcionais](../sprint-1/especificacoes-tecnicas/Requisitos_Nao_Funcionais.md) de um sistema que seria capaz de detectar fissuras em edificações. Além disso, concebeu-se a sua [arquitetura inicial](../sprint-1/especificacoes-tecnicas/Arquitetura_Inicial.md), a qual foi iterada na sprint 2 - ver [Atualizações na Arquitetura](../sprint-2/desenvolvimento-tecnico-do-sistema/proposta-da-arquitetura.md). Contemplava-se nessas seções um sistema dividido em três partes: Captura, Processamento e Análise.

&emsp; A primeira parte, integrada ao sistema _a posteriori_ e _ad captandum_, reserva-se ao piloto. À ele, é dada a tarefa de capturar fotos de fissuras por meio de drones como as que se seguem:

FOTO 1
FOTO 2 JUNTAS

&emsp; Essas imagens são, então, enviadas para a cloud (servidor no [Supabase](https://supabase.com/)). Desta forma, o pesquisador no IPT é capaz de recuperá-las para inserí-las no sistema.

&emsp; Na sprint 3, conforme a arquitetura final, essa funcionalidade foi adicionada ao sistema. Para tanto, criou-se o SOD App via Android Studio - ver [Instruções de como rodar o aplicativo](./instrucoes-app.md). Esse aplicativo permite ao usuário se conectar de forma segura com um drone da DIJ chamado Tello. Nele, o usuário pode capturar imagens e enviar ao servidor diretamente. Vê-se, portanto, como a captura se integrou ao sistema. Essa parte do sistema foi finalizada nesta sprint.

&emsp; Após a captura, dá-se o processamento da imagem. Esse processo acontece, na visão do usuário, em conjunto com a análise. Antes, porém, o pesquisador separa as imagens recebidas manualmente em andar e direção da fachada, como no vídeo a seguir.

Vídeo 1

Então, o sistema entra a etapa do processamento. Para cada imagem, uma inteligência artificial detecta onde estão as fissuras. Então, cada imagem de fissura passa por um processamento que a padroniza para ser adequamente recebida pela próxima IA. Essa padronização transforma a imagem como no vídeo 2.

Vídeo 2

&emsp; Imagens como as que estão acima são enviadas para a análise. Esse processo foi finalizado na [sprint 4](../sprint-4/inteligencia-artificial/modelos/yolov8.md).

&emsp; A última etapa do processo é a análise, responsável pelo auxílio real ao pesquisador. Após o processamento, outra inteligência artificial recebe essas imagens. Ela, então, analisa cada uma para decidir:
- É uma fissura **de retração**;
- ou é uma fissura **térmica**.

&emsp; Essas decisões individuais são condensadas em um relatório conforme _template_ do IPT. Essa etapa foi finalizada na sprint 3 e integrada na última sprint.

&emsp; Em relação à satisfação do usuário do sistema, em testes de usabilidade atingiu-se a métrica X. Em relação à IA de análise, atingiu-se a acurácia de X.

## Processamento de Imagem e IA









