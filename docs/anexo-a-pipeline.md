# Anexo A – Documentação Técnica do Pipeline de Simulação

## 1. Revisão das Métricas Atuais

| Métrica | Cálculo | Significado |
|---------|---------|-------------|
| Taxa de aprovação por gênero | `mean(aprovado) * 100` agrupado por gênero | Percentual de aprovados em cada grupo. |
| Disparate Impact (DI) | `taxa_feminino / taxa_masculino` | Razão entre aprovações femininas e masculinas. Aceitável ≥ 0,80. |
| Correlação score × aprovação | `corr(score_num, aprovado)` | Força da relação entre nota e aprovação. |
| Inconsistências de funil | contagem de contradições | Identifica registros com aprovado inconsistente com etapa. |

## 2. Passo a Passo para Executar a Simulação

**Pré‑requisitos:** Python 3.7+, pandas, numpy.

### Etapas

1. Crie um arquivo `pipeline_kraira.py` e cole o script fornecido.
2. Execute no terminal:
   ```bash
   python pipeline_kraira.py
   ```

### Interpretação (exemplo com seed=42)

- Taxas de aprovação: Feminino 41,7% | Masculino 58,3% | Não informado 35,0% | Outro 45,0%
- **DI = 0,715** → impacto adverso.
- Correlações: portfolio 0,62 | técnico 0,78.
- Inconsistências: ~25 registros.

### Conexão com Power BI

Importar `dados_limpos.csv` e criar:

- Gráfico de barras por gênero
- Cartão de Disparate Impact (DI)
- Funil de recrutamento
- Gráfico de dispersão entre scores e aprovação
