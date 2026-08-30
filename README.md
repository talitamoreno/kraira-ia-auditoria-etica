# Projeto Kraira IA – Relatório de Impacto Social e Auditoria Ética

**Auditoria ética para recrutamento algorítmico: redução de vieses de gênero com IA explicável e governança.**

---

## Problema

Algoritmos de recrutamento treinados com dados históricos perpetuam desigualdades sob falsa neutralidade. No Brasil, mulheres ocupam apenas **10,58%** das posições de IA, setor que paga **56%** a mais que a média. Essa "Barreira de Vidro Algorítmica" exclui talentos diversos, reduz a inovação e expõe empresas a riscos jurídicos crescentes com o Marco Legal da IA (PL 2338/2023).

---

## Solução

A Kraira IA é uma plataforma de auditoria de equidade em recrutamento que opera em cinco etapas:

1. **Coleta** – aceita dados brutos do funil sem preparação prévia.
2. **Limpeza e padronização** – corrige inconsistências automaticamente.
3. **Auditoria** – calcula Disparate Impact (DI), taxas de aprovação por gênero e correlações. <span class="badge">Interseccional</span>
4. **Relatório executivo** – diagnóstico claro e recomendações práticas.
5. **Acompanhamento** – dashboard contínuo para monitorar indicadores.

> A auditoria incorpora **perspectiva interseccional**, considerando raça, idade, escolaridade e deficiência, evitando que vieses cruzados passem despercebidos.

---

##  Métricas e Impacto

### Impacto direto (empresas clientes)
- **Disparate Impact (DI) médio:** de 0,65–0,70 para **≥ 0,80** em 12 meses.
- **Paridade recomendadas vs. contratadas:** de 0,60 para **≥ 0,85** em 18 meses.
- **Taxa de abandono feminino no funil:** de 35% para **≤ 20%** em 12 meses.

### Impacto sistêmico (setor de IA)
- **Participação feminina em IA:** de 10,58% para **≥ 35%** em 24 meses (meta aspiracional).
- **Mobilidade social:** +1.200 profissionais de baixa renda em posições de elite.
- **Segurança jurídica:** redução ≥ 40% em processos por discriminação algorítmica.

---

## Pipeline Técnico

O projeto inclui um script Python que simula dados sujos, aplica limpeza e calcula métricas de equidade.

### Pré-requisitos
- Python 3.7+
- pandas, numpy

### Execução
```bash
python pipeline_kraira.py
```

O script gera:
- `output/dados_limpos.csv` – dados prontos para Power BI.
- `output/kraira.db` – banco SQLite com tabela original e view limpa.
- `output/relatorio_executivo.md` – relatório automático com métricas.

### Resultados da simulação (seed=42)
- Taxas de aprovação: Feminino 41,7% | Masculino 58,3% | Não informado 35,0% | Outro 45,0%
- **DI = 0,715** → impacto adverso (abaixo de 0,80)
- Correlações: portfolio 0,62 | técnico 0,78
- Inconsistências de funil: ~25 registros

---

## Dashboard Power BI

Após importar `dados_limpos.csv`, o dashboard oferece:

- **Cartão de Disparate Impact (DI)** com alerta visual se < 0,80.
- **Gráfico de barras** com taxa de aprovação por gênero.
- **Funil de recrutamento** com contagem por etapa.
- **Gráfico de dispersão** correlacionando scores e aprovação.
- **Semáforo de meta** para DI ≥ 0,80.

---

## Acessibilidade e Sustentabilidade

- **WCAG 2.1 (POUR):** navegação por teclado, contraste 4.5:1, leitores de tela, suporte a Libras.
- **PWA offline-first:** funciona com conexão intermitente e hardware antigo.
- **TI Verde:** algoritmos otimizados e nuvem com energia renovável.

---

## Interseccionalidade e Riscos Residuais

A auditoria de gênero é essencial, mas insuficiente. A análise unidimensional pode mascarar vieses interseccionais (ex.: mulheres negras, com deficiência). Riscos residuais identificados:

- **Viés de proxy** – variáveis como CEP substituem identidade.
- **Poder estatístico baixo** – subgrupos pequenos geram falsos negativos.
- **Supervisão superficial** – HITL burocrático.
- **Dados desatualizados** – perda de eficácia.

**Mitigações:** auditoria interseccional periódica, revisão de proxies, HITL com checklist, monitoramento por subgrupo.

---

## Documentação Adicional

- [Anexo A – Documentação Técnica do Pipeline](docs/anexo-a-pipeline.md)
- [Anexo B – Interseccionalidade e Riscos Residuais](docs/anexo-b-interseccionalidade.md)
- [Relatório Final em PDF](https://github.com/talitamoreno/kraira-ia-auditoria-etica/blob/main/docs/kraira_ia_documento_final.pdf)

---

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/talitamoreno/kraira-ia-auditoria-etica.git
   ```
2. Instale as dependências:
   ```bash
   pip install pandas numpy
   ```
3. Execute o pipeline:
   ```bash
   python pipeline_kraira.py
   ```
4. Importe `output/dados_limpos.csv` no Power BI para visualizar o dashboard.

---

## Estrutura do Repositório

```text
kraira-ia-auditoria-etica/
│   pipeline_kraira.py          # Script principal de simulação e auditoria
│   README.md
│
├── output/
│   ├── dados_limpos.csv        # Dados limpos para Power BI
│   ├── kraira.db               # Banco SQLite com view limpa
│   └── relatorio_executivo.md  # Relatório automático
│
└── docs/
    ├── anexo-a-pipeline.md     # Documentação técnica do pipeline
    ├── anexo-b-interseccionalidade.md # Interseccionalidade e riscos
    └── relatorio_final.pdf     # Documento executivo completo
```

---

## Licença MIT/ Uso Educacional

Este projeto é parte de um portfólio acadêmico. Os dados e resultados são simulados para fins de demonstração técnica e não representam dados reais de empresas ou candidatos.

---

**Desenvolvido por Talita Moreno**  
