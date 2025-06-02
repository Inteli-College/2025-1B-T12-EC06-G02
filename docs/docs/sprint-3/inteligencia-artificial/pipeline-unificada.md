---
sidebar_position: 3
slug: /inteligencia-artificial/pipeline-unificada
description: "Sistema unificado para inferência com múltiplos modelos"
---

# Pipeline de Inferência Unificada

&emsp; Para atender ao [RF01](../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), foi desenvolvido um sistema unificado de inferência capaz de operar com ambos os modelos (ResNet-18 e Swin Transformer V2) de forma transparente, garantindo flexibilidade operacional.

## Contexto de Desenvolvimento

&emsp; O sistema unificado foi desenvolvido para suportar tanto o ResNet-18 (modelo experimental com limitações) quanto o Swin Transformer V2 (modelo implementado no frontend). Embora apenas o Swin Transformer V2 seja utilizado em produção devido às limitações de generalização identificadas no ResNet-18, a arquitetura permite flexibilidade para futuras expansões.

## Arquitetura do Sistema

&emsp; O sistema utiliza uma classe principal `UnifiedCrackClassifier` que gerencia automaticamente:

1. **Detecção automática** do tipo de modelo baseado no caminho
2. **Carregamento dinâmico** dos módulos específicos  
3. **Configuração automática** das transformações adequadas
4. **Interface padronizada** para resultados consistentes

### Fluxo de Execução

```
Modelo + Imagem → Detecção Tipo → Carregamento Dinâmico → 
Pré-processamento → Inferência → Resultado Padronizado
```

## Pré-processamento Específico

&emsp; Cada modelo aplica transformações otimizadas:

**ResNet-18:**
- Resize direto para 224×224
- Normalização ImageNet padrão
- CLAHE opcional baseado na configuração

**Swin Transformer V2:**
- Resize para 224×224
- CLAHE com parâmetros específicos
- Normalização otimizada
- Filtros avançados quando disponíveis

## Performance

<p style={{textAlign: 'center'}}>Tabela 1: Tempos de Inferência</p>
<div style={{margin: 25, textAlign: 'center', display: 'flex'}}>
    <table style={{margin: 'auto'}}>
        <thead>
          <tr>
            <th>Operação</th>
            <th>ResNet-18</th>
            <th>Swin Transformer V2</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Carregamento inicial</td>
            <td>~2s</td>
            <td>~5s</td>
          </tr>
          <tr>
            <td>Inferência (GPU)</td>
            <td>~0.05s</td>
            <td>~0.15s</td>
          </tr>
          <tr>
            <td>Batch 10 imagens</td>
            <td>~0.2s</td>
            <td>~0.8s</td>
          </tr>
        </tbody>
    </table>
</div>
<p style={{textAlign: 'center'}}>Fonte: Produzida pelos Autores (2025). </p>

## Integração com Sistema SOD

### API REST
```python
from modules.inference import classify_for_frontend

def classify_endpoint(request):
    results = classify_for_frontend(
        request.json['image_paths'],
        request.json['image_ids'], 
        request.json['preview_urls'],
        "models/best_model.pth"
    )
    return {"predictions": results}
```

## Tratamento de Erros

&emsp; O sistema implementa tratamento robusto:

- **Imagens corrompidas**: Fallback com resultado de erro
- **Modelos indisponíveis**: Mensagens informativas
- **Configurações ausentes**: Valores padrão seguros
- **Isolamento**: Erros por modelo não afetam outros

## Recomendações de Uso

- **Produção**: Sempre utilizar Swin Transformer V2
- **Desenvolvimento**: Pipeline unificada permite testes com ambos os modelos
- **Validação**: ResNet-18 mantido apenas para comparação e aprendizado
- **Futuro**: Arquitetura preparada para novos modelos

## Conclusões

&emsp; A pipeline unificada atende completamente ao [RF01](../../sprint-1/especificacoes-tecnicas/Requisitos_Funcionais.md), fornecendo:

- **Flexibilidade**: Suporte transparente a múltiplos modelos
- **Simplicidade**: Interface consistente e fácil de usar
- **Robustez**: Tratamento abrangente de erros
- **Extensibilidade**: Fácil adição de novos modelos

&emsp; Esta solução garante base sólida para classificação automática no sistema SOD com capacidade de evolução futura.

### Integração com Desenvolvimento Geral

&emsp; A pipeline unificada representa a culminação técnica desta sprint de IA, conectando o [primeiro modelo](./primeiro-modelo-s3) com o [segundo modelo de produção](./segundo-modelo) em uma solução coesa. Esta arquitetura facilita a transição para as próximas sprints, onde a integração com o sistema de drones e a validação em campo serão os focos principais do desenvolvimento contínuo do sistema SOD.