#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kraira IA – Pipeline de Auditoria de Equidade em Recrutamento
Autor: Talita Moreno
Data: 2026-08-30

Este script:
1. Gera um dataset fictício com inconsistências (dados sujos)
2. Aplica limpeza e padronização
3. Calcula métricas de equidade (taxa de aprovação, Disparate Impact, correlações)
4. Exporta dados limpos para CSV e SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta

# ==============================
# CONFIGURAÇÕES
# ==============================
RANDOM_SEED = 42
NUM_CANDIDATOS = 250
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# 1. GERAÇÃO DO DATASET SUJO
# ==============================
def gerar_dados_sujos(n_candidatos=250, seed=42):
    np.random.seed(seed)

    # Variações de gênero (incluindo nulos)
    generos_sujos = [
        'F', 'f', 'feminino', 'Feminino', 'FEM',
        'M', 'm', 'masculino', 'Masculino', 'MASC',
        'NB', 'nb', 'Não binário', 'outro', 'Outro',
        'prefiro não informar', 'Prefiro não informar',
        None
    ]
    prob_genero = [0.1, 0.05, 0.05, 0.05, 0.02,
                   0.15, 0.1, 0.1, 0.1, 0.03,
                   0.05, 0.02, 0.03, 0.02, 0.02,
                   0.05, 0.02, 0.06]
    prob_genero = np.array(prob_genero)
    prob_genero = prob_genero / prob_genero.sum()
    generos = np.random.choice(generos_sujos, size=n_candidatos, p=prob_genero)

    # Scores sujos (strings, fora do intervalo, nulos)
    score_options = [
        '8.5', '7', '9', '6.5', '8', '7.5', '6', '5.5', '9.5', '10',
        'N/A', 'dez', '12', '-3', '7,5', '8,0', '9,3', '4,5', '3', '11',
        None, 'NaN', 'inf', '8.7', '5', '6.8', '7.2'
    ]
    score_tecnico_sujo = np.random.choice(score_options, size=n_candidatos)
    score_portfolio_sujo = np.random.choice(score_options, size=n_candidatos)

    # Tempo gasto (strings sujas)
    tempo_options = [
        '45min', '1h', '1h30', '2h', '30', '-', '-h', '1h15', '50min',
        '3h', '2h45', '1h45', '1h20', '40min', '55min', '1h10',
        None, '0', '4h', '2h30', '3h30', '1h50', '35min', '25min'
    ]
    tempo_gasto_sujo = np.random.choice(tempo_options, size=n_candidatos)

    # Etapa do funil
    etapas = ['submissao', 'teste', 'entrevista', 'aprovado']
    prob_etapas = [0.2, 0.4, 0.3, 0.1]
    etapa_funil = np.random.choice(etapas, size=n_candidatos, p=prob_etapas)

    # Aprovação (com inconsistências)
    aprovado = np.where(etapa_funil == 'aprovado', 1, 0)
    indices_bagunca = np.random.choice(n_candidatos, size=int(n_candidatos*0.1), replace=False)
    for i in indices_bagunca:
        aprovado[i] = 1 - aprovado[i]

    # Datas de submissão
    data_inicial = datetime(2026, 1, 1)
    data_submissao = [data_inicial + timedelta(days=int(x)) for x in np.random.randint(0, 90, size=n_candidatos)]

    df = pd.DataFrame({
        'id_candidato': range(1, n_candidatos+1),
        'genero': generos,
        'score_tecnico': score_tecnico_sujo,
        'score_portfolio': score_portfolio_sujo,
        'tempo_gasto': tempo_gasto_sujo,
        'etapa_funil': etapa_funil,
        'aprovado': aprovado,
        'data_submissao': data_submissao
    })
    return df

# ==============================
# 2. LIMPEZA E TRANSFORMAÇÃO
# ==============================
def padronizar_genero(serie):
    mapping = {
        'f': 'Feminino', 'feminino': 'Feminino', 'fem': 'Feminino',
        'm': 'Masculino', 'masculino': 'Masculino', 'masc': 'Masculino',
        'nb': 'Outro', 'não binário': 'Outro', 'nao binario': 'Outro',
        'outro': 'Outro',
        'prefiro não informar': 'Não informado', 'prefiro nao informar': 'Não informado'
    }
    def _map(val):
        if pd.isna(val):
            return 'Não informado'
        val_lower = str(val).strip().lower()
        return mapping.get(val_lower, 'Outro')
    return serie.apply(_map)

def converter_score(serie):
    def _convert(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            if 0 <= val <= 10:
                return float(val)
            return np.nan
        s = str(val).strip().lower().replace(',', '.')
        if s in ['dez', 'n/a', 'nan', 'inf', '-', '']:
            return np.nan
        try:
            num = float(s)
            if 0 <= num <= 10:
                return num
            return np.nan
        except:
            return np.nan
    return serie.apply(_convert)

def converter_tempo(serie):
    def _convert(val):
        if pd.isna(val):
            return np.nan
        s = str(val).strip().lower()
        if 'h' in s and 'min' in s:
            parts = s.split('h')
            horas = int(parts[0]) if parts[0] else 0
            minutos = int(parts[1].replace('min','')) if parts[1] else 0
            return horas*60 + minutos
        elif 'h' in s:
            return int(s.replace('h',''))*60
        elif 'min' in s:
            return int(s.replace('min',''))
        else:
            try:
                return float(s)
            except:
                return np.nan
    return serie.apply(_convert)

def limpar_dados(df):
    df_limpo = df.copy()
    df_limpo['genero_padronizado'] = padronizar_genero(df_limpo['genero'])
    df_limpo['score_tecnico_num'] = converter_score(df_limpo['score_tecnico'])
    df_limpo['score_portfolio_num'] = converter_score(df_limpo['score_portfolio'])

    # Imputação por mediana (por gênero)
    for col in ['score_tecnico_num', 'score_portfolio_num']:
        df_limpo[col] = df_limpo.groupby('genero_padronizado')[col].transform(lambda x: x.fillna(x.median()))
        df_limpo[col] = df_limpo[col].fillna(df_limpo[col].median())

    # Tempo: converter e tratar outliers
    df_limpo['tempo_minutos'] = converter_tempo(df_limpo['tempo_gasto'])
    media_tempo = df_limpo['tempo_minutos'].mean()
    std_tempo = df_limpo['tempo_minutos'].std()
    limite_superior = media_tempo + 3*std_tempo
    df_limpo.loc[df_limpo['tempo_minutos'] > limite_superior, 'tempo_minutos'] = np.nan
    mediana_tempo = df_limpo['tempo_minutos'].median()
    df_limpo['tempo_minutos'] = df_limpo['tempo_minutos'].fillna(mediana_tempo)

    # Sinalizar inconsistências de funil
    df_limpo['inconsistencia_funil'] = ((df_limpo['aprovado'] == 1) & (df_limpo['etapa_funil'] != 'aprovado')) | \
                                       ((df_limpo['aprovado'] == 0) & (df_limpo['etapa_funil'] == 'aprovado'))
    return df_limpo

# ==============================
# 3. CÁLCULO DE MÉTRICAS
# ==============================
def calcular_metricas(df_limpo):
    taxas = df_limpo.groupby('genero_padronizado')['aprovado'].mean() * 100
    taxa_fem = taxas.get('Feminino', np.nan)
    taxa_masc = taxas.get('Masculino', np.nan)
    di = (taxa_fem / taxa_masc) if (pd.notna(taxa_fem) and pd.notna(taxa_masc) and taxa_masc > 0) else np.nan
    corr_portfolio = df_limpo['score_portfolio_num'].corr(df_limpo['aprovado'])
    corr_tecnico = df_limpo['score_tecnico_num'].corr(df_limpo['aprovado'])
    inconsistencias = df_limpo['inconsistencia_funil'].sum()
    return {
        'taxas': taxas,
        'di': di,
        'corr_portfolio': corr_portfolio,
        'corr_tecnico': corr_tecnico,
        'inconsistencias': inconsistencias
    }

# ==============================
# 4. EXPORTAÇÃO
# ==============================
def exportar_dados(df_limpo, df_sujo, output_dir):
    csv_path = os.path.join(output_dir, 'dados_limpos.csv')
    df_limpo.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Dados limpos exportados para: {csv_path}")

    db_path = os.path.join(output_dir, 'kraira.db')
    conn = sqlite3.connect(db_path)
    df_sujo.to_sql('candidatos_brutos', conn, if_exists='replace', index=False)
    df_limpo.to_sql('_temp_limpos', conn, if_exists='replace', index=False)
    conn.execute("CREATE VIEW IF NOT EXISTS candidatos_limpos AS SELECT * FROM _temp_limpos")
    conn.commit()
    conn.close()
    print(f"Banco SQLite salvo em: {db_path}")

# ==============================
# 5. FUNÇÃO PRINCIPAL
# ==============================
def main():
    print("="*60)
    print("KRAIRA IA – PIPELINE DE AUDITORIA DE EQUIDADE")
    print("="*60)

    print("\n[1] Gerando dataset sujo...")
    df_sujo = gerar_dados_sujos(NUM_CANDIDATOS, RANDOM_SEED)

    print("\n[2] Aplicando limpeza...")
    df_limpo = limpar_dados(df_sujo)

    print("\n[3] Calculando métricas...")
    metricas = calcular_metricas(df_limpo)

    print("\n--- Resultados ---")
    print("\nTaxas de aprovação por gênero:")
    for genero, taxa in metricas['taxas'].items():
        print(f"  {genero}: {taxa:.1f}%")
    print(f"\nDisparate Impact (DI): {metricas['di']:.3f}")
    if pd.notna(metricas['di']) and metricas['di'] < 0.8:
        print("  -> Possível impacto adverso identificado!")
    print(f"\nCorrelação portfolio × aprovação: {metricas['corr_portfolio']:.3f}")
    print(f"Correlação técnico × aprovação: {metricas['corr_tecnico']:.3f}")
    print(f"Inconsistências de funil: {metricas['inconsistencias']}")

    print("\n[4] Exportando dados...")
    exportar_dados(df_limpo, df_sujo, OUTPUT_DIR)

    print("\nPipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
