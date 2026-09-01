"""
================================================================================
SCRIPT: Geração de Dados Sintéticos - Cooperativa de Crédito (Padrão BACEN / Sicredi)
AUTOR: Iago Walter
DATA: Setembro/2026
OBJETIVO:
    Gerar dados relacionais e consistentes para simular a operação de uma
    instituição financeira cooperativa, cobrindo:
    - Dimensão de Associados (PF, PJ e Produtor Rural com Score de Crédito)
    - Dimensão de Agências e Polos
    - Dimensão de Produtos (Linhas de Crédito e Captação)
    - Fato de Carteira de Crédito e Risco (com Ratings BACEN de AA a H, Aging e PCLD)
    - Fato de Captação (Depósitos a Prazo RDC e Poupança)
    - Fato de Metas das Agências (Originação, Captação e Inadimplência NPL)
================================================================================
"""

import os
import sys
import logging
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE LOGGING
# -----------------------------------------------------------------------------
DIRETORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_LOGS = os.path.join(DIRETORIO_BASE, "logs")
DIRETORIO_DADOS = os.path.join(DIRETORIO_BASE, "dados")

os.makedirs(DIRETORIO_LOGS, exist_ok=True)
os.makedirs(DIRETORIO_DADOS, exist_ok=True)

ARQUIVO_LOG = os.path.join(DIRETORIO_LOGS, "geracao_dados.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Fixando semente para reprodutibilidade
random.seed(42)
np.random.seed(42)

# -----------------------------------------------------------------------------
# 2. DEFINIÇÃO DAS ESTRUTURAS DE TABELA (PADRÃO DIMENSIONAL KIMBALL)
# -----------------------------------------------------------------------------

def gerar_dim_agencias():
    """Gera o cadastro de Agências e Regionais da Cooperativa."""
    logging.info("Iniciando geração da tabela Dim_Agencias...")
    
    dados = [
        {"ID_Agencia": "AG001", "Nome_Agencia": "Ag. Santa Cruz Centro", "Regional": "Polo Santa Cruz", "Cidade": "Santa Cruz do Sul", "UF": "RS", "Porte": "Grande"},
        {"ID_Agencia": "AG002", "Nome_Agencia": "Ag. Arroio Grande", "Regional": "Polo Santa Cruz", "Cidade": "Santa Cruz do Sul", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG003", "Nome_Agencia": "Ag. Universitária", "Regional": "Polo Santa Cruz", "Cidade": "Santa Cruz do Sul", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG004", "Nome_Agencia": "Ag. Linha Santa Cruz", "Regional": "Polo Santa Cruz", "Cidade": "Santa Cruz do Sul", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG005", "Nome_Agencia": "Ag. Vera Cruz Centro", "Regional": "Polo Rio Pardo & Vales", "Cidade": "Vera Cruz", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG006", "Nome_Agencia": "Ag. Venâncio Aires Centro", "Regional": "Polo Venâncio Aires", "Cidade": "Venâncio Aires", "UF": "RS", "Porte": "Grande"},
        {"ID_Agencia": "AG007", "Nome_Agencia": "Ag. Venâncio Av. Ruperti", "Regional": "Polo Venâncio Aires", "Cidade": "Venâncio Aires", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG008", "Nome_Agencia": "Ag. Rio Pardo Centro", "Regional": "Polo Rio Pardo & Vales", "Cidade": "Rio Pardo", "UF": "RS", "Porte": "Média"},
        {"ID_Agencia": "AG009", "Nome_Agencia": "Ag. Sinimbu", "Regional": "Polo Encosta da Serra", "Cidade": "Sinimbu", "UF": "RS", "Porte": "Pequena"},
        {"ID_Agencia": "AG010", "Nome_Agencia": "Ag. Passo do Sobrado", "Regional": "Polo Rio Pardo & Vales", "Cidade": "Passo do Sobrado", "UF": "RS", "Porte": "Pequena"},
        {"ID_Agencia": "AG011", "Nome_Agencia": "Ag. Pantano Grande", "Regional": "Polo Rio Pardo & Vales", "Cidade": "Pantano Grande", "UF": "RS", "Porte": "Pequena"},
        {"ID_Agencia": "AG012", "Nome_Agencia": "Ag. Vale Verde", "Regional": "Polo Rio Pardo & Vales", "Cidade": "Vale Verde", "UF": "RS", "Porte": "Pequena"}
    ]
    
    df = pd.DataFrame(dados)
    caminho = os.path.join(DIRETORIO_DADOS, "Dim_Agencias.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Dim_Agencias salva com sucesso: {len(df)} agências.")
    return df


def gerar_dim_produtos():
    """Gera o catálogo de produtos financeiros da Cooperativa (Crédito e Captação)."""
    logging.info("Iniciando geração da tabela Dim_Produtos...")
    
    produtos = [
        # Linhas de Crédito (Ativo da Cooperativa)
        {"ID_Produto": "PRD_CR_RURAL_CUST", "Nome_Produto": "Crédito Rural - Custeio", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Produtor Rural", "Taxa_Juros_aa_Base": 0.105},
        {"ID_Produto": "PRD_CR_RURAL_INV", "Nome_Produto": "Crédito Rural - Investimento", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Produtor Rural", "Taxa_Juros_aa_Base": 0.125},
        {"ID_Produto": "PRD_GIRO_PJ", "Nome_Produto": "Capital de Giro PJ", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Pessoa Jurídica", "Taxa_Juros_aa_Base": 0.198},
        {"ID_Produto": "PRD_CONSIGNADO_PF", "Nome_Produto": "Crédito Consignado", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Pessoa Física", "Taxa_Juros_aa_Base": 0.185},
        {"ID_Produto": "PRD_VEICULOS", "Nome_Produto": "Financiamento de Veículos / Máquinas", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Geral", "Taxa_Juros_aa_Base": 0.165},
        {"ID_Produto": "PRD_CHEQUE_ESP", "Nome_Produto": "Limite Cheque Especial / Rotativo", "Tipo_Operacao": "Crédito", "Segmento_Alvo": "Geral", "Taxa_Juros_aa_Base": 0.450},
        
        # Linhas de Captação (Passivo da Cooperativa - Depósitos dos Associados)
        {"ID_Produto": "PRD_RDC_POS", "Nome_Produto": "RDC Pós-Fixado (Depósito a Prazo)", "Tipo_Operacao": "Captação", "Segmento_Alvo": "Geral", "Taxa_Juros_aa_Base": 0.108},
        {"ID_Produto": "PRD_POUPANCA", "Nome_Produto": "Poupança Cooperativa", "Tipo_Operacao": "Captação", "Segmento_Alvo": "Pessoa Física", "Taxa_Juros_aa_Base": 0.065},
        {"ID_Produto": "PRD_LCA", "Nome_Produto": "LCA - Letra de Crédito do Agronegócio", "Tipo_Operacao": "Captação", "Segmento_Alvo": "Geral", "Taxa_Juros_aa_Base": 0.095}
    ]
    
    df = pd.DataFrame(produtos)
    caminho = os.path.join(DIRETORIO_DADOS, "Dim_Produtos.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Dim_Produtos salva com sucesso: {len(df)} produtos cadastrados.")
    return df


def gerar_dim_associados(qtd=1500, df_agencias=None):
    """Gera a base de associados (cooperados) com perfis e scores de risco."""
    logging.info(f"Gerando base de {qtd} associados...")
    
    segmentos = ["Pessoa Física", "Pessoa Jurídica", "Produtor Rural"]
    pesos_segmento = [0.50, 0.25, 0.25]
    
    agencias = df_agencias["ID_Agencia"].tolist()
    
    lista = []
    data_inicio = datetime(2015, 1, 1)
    
    for i in range(1, qtd + 1):
        id_assoc = f"ASC{i:05d}"
        segmento = random.choices(segmentos, weights=pesos_segmento)[0]
        agencia = random.choice(agencias)
        
        # Data de associação entre 2015 e 2025
        dias_assoc = random.randint(0, 3650)
        dt_associacao = data_inicio + timedelta(days=dias_assoc)
        
        # Score de Crédito (300 a 1000 - distribuição realista)
        # Produtor Rural e PJ tendem a ter média ligeiramente mais alta por patrimônio
        if segmento == "Produtor Rural":
            score = int(np.clip(np.random.normal(740, 110), 320, 990))
            renda_faturamento = round(float(np.random.exponential(450000) + 120000), 2)
        elif segmento == "Pessoa Jurídica":
            score = int(np.clip(np.random.normal(710, 120), 300, 980))
            renda_faturamento = round(float(np.random.exponential(600000) + 180000), 2)
        else:
            score = int(np.clip(np.random.normal(670, 140), 300, 970))
            renda_faturamento = round(float(np.random.exponential(48000) + 25000), 2)
            
        lista.append({
            "ID_Associado": id_assoc,
            "Nome_Associado": f"Associado {id_assoc}",
            "Segmento": segmento,
            "ID_Agencia": agencia,
            "Score_Credito": score,
            "Faixa_Score": "Excelente (800+)" if score >= 800 else ("Bom (700-799)" if score >= 700 else ("Regular (550-699)" if score >= 550 else "Crítico (<550)")),
            "Renda_Faturamento_Anual": renda_faturamento,
            "Data_Associacao": dt_associacao.strftime("%Y-%m-%d")
        })
        
    df = pd.DataFrame(lista)
    caminho = os.path.join(DIRETORIO_DADOS, "Dim_Associados.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Dim_Associados salva com sucesso: {len(df)} registros.")
    return df


def gerar_fatos_carteira_credito(qtd_contratos=3500, df_associados=None, df_produtos=None):
    """
    Gera a carteira ativa de crédito com regras reais do Banco Central (Res. 2.682):
    - Dias de atraso (0 a 360+ dias)
    - Aging: Em Dia, 01-14d, 15-30d, 31-60d, 61-90d, 90d+ (NPL)
    - Ratings BACEN de AA a H e cálculo da Provisão PCLD
    """
    logging.info(f"Gerando {qtd_contratos} contratos da Carteira de Crédito...")
    
    produtos_credito = df_produtos[df_produtos["Tipo_Operacao"] == "Crédito"].to_dict("records")
    assoc_dict = df_associados.set_index("ID_Associado").to_dict("index")
    ids_associados = list(assoc_dict.keys())
    
    contratos = []
    data_base_analise = datetime(2026, 8, 31)
    
    for i in range(1, qtd_contratos + 1):
        id_contrato = f"CTR{i:06d}"
        id_assoc = random.choice(ids_associados)
        assoc_info = assoc_dict[id_assoc]
        
        # Filtra produtos adequados ao segmento do associado
        seg = assoc_info["Segmento"]
        prod_compativeis = [p for p in produtos_credito if p["Segmento_Alvo"] in [seg, "Geral"]]
        if not prod_compativeis:
            prod_compativeis = produtos_credito
            
        prod = random.choice(prod_compativeis)
        
        # Data de contratação entre 2023 e 2026
        dias_atras = random.randint(30, 1100)
        dt_contratacao = data_base_analise - timedelta(days=dias_atras)
        prazo_meses = random.choice([12, 24, 36, 48, 60, 72])
        dt_vencimento = dt_contratacao + timedelta(days=prazo_meses * 30)
        
        # Valor Contratado conforme segmento e produto
        if prod["ID_Produto"].startswith("PRD_CR_RURAL"):
            vl_contratado = round(float(np.random.uniform(150000, 1800000)), 2)
        elif prod["ID_Produto"] == "PRD_GIRO_PJ":
            vl_contratado = round(float(np.random.uniform(50000, 600000)), 2)
        elif prod["ID_Produto"] == "PRD_VEICULOS":
            vl_contratado = round(float(np.random.uniform(60000, 350000)), 2)
        else:
            vl_contratado = round(float(np.random.uniform(5000, 95000)), 2)
            
        # Saldo Devedor Atual (entre 20% e 95% do valor original)
        pct_saldo = random.uniform(0.20, 0.95)
        saldo_devedor = round(vl_contratado * pct_saldo, 2)
        
        # ---------------------------------------------------------------------
        # MODELAGEM DE ATRASO, RATING BACEN E PCLD (Resolução BACEN 2.682)
        # ---------------------------------------------------------------------
        score = assoc_info["Score_Credito"]
        
        # Probabilidade de atraso condicionada ao score do associado
        prob_inadimplencia = 0.02 if score >= 800 else (0.05 if score >= 700 else (0.12 if score >= 550 else 0.35))
        
        if random.random() < prob_inadimplencia:
            # Associado em atraso
            faixa_sorteada = random.choices(
                ["01-14 dias", "15-30 dias", "31-60 dias", "61-90 dias", "90+ dias (NPL)"],
                weights=[0.35, 0.25, 0.18, 0.12, 0.10]
            )[0]
            
            if faixa_sorteada == "01-14 dias":
                dias_atraso = random.randint(1, 14)
                rating = random.choice(["B", "C"])
            elif faixa_sorteada == "15-30 dias":
                dias_atraso = random.randint(15, 30)
                rating = random.choice(["C", "D"])
            elif faixa_sorteada == "31-60 dias":
                dias_atraso = random.randint(31, 60)
                rating = "E"
            elif faixa_sorteada == "61-90 dias":
                dias_atraso = random.randint(61, 90)
                rating = "F"
            else:
                dias_atraso = random.randint(91, 380)
                rating = random.choice(["G", "H"])
        else:
            # Em dia
            dias_atraso = 0
            faixa_sorteada = "Em Dia"
            if score >= 800:
                rating = random.choice(["AA", "A"])
            elif score >= 700:
                rating = random.choice(["A", "B"])
            else:
                rating = random.choice(["B", "C"])
                
        # Percentuais de Provisão Mandatórios pelo BACEN
        tabela_provisao_bacen = {
            "AA": 0.000,
            "A":  0.005,
            "B":  0.010,
            "C":  0.030,
            "D":  0.100,
            "E":  0.300,
            "F":  0.500,
            "G":  0.700,
            "H":  1.000
        }
        
        pct_provisao = tabela_provisao_bacen[rating]
        valor_provisao = round(saldo_devedor * pct_provisao, 2)
        
        # Taxa contratada anual (ajustada pelo risco)
        spread_risco = 0.04 if rating in ["E", "F", "G", "H"] else (0.015 if rating in ["C", "D"] else 0.0)
        taxa_juros_aa = round(prod["Taxa_Juros_aa_Base"] + spread_risco, 4)
        
        contratos.append({
            "ID_Contrato": id_contrato,
            "ID_Associado": id_assoc,
            "ID_Agencia": assoc_info["ID_Agencia"],
            "ID_Produto": prod["ID_Produto"],
            "Data_Contratacao": dt_contratacao.strftime("%Y-%m-%d"),
            "Data_Vencimento_Final": dt_vencimento.strftime("%Y-%m-%d"),
            "Valor_Contratado": vl_contratado,
            "Saldo_Devedor": saldo_devedor,
            "Dias_Atraso": dias_atraso,
            "Faixa_Atraso": faixa_sorteada,
            "Status_Inadimplencia": "NPL 90+ (Inadimplente)" if dias_atraso > 90 else ("Alerta (1-90 dias)" if dias_atraso > 0 else "Normal (Em Dia)"),
            "Rating_Bacen": rating,
            "Perc_Provisao_Bacen": pct_provisao,
            "Valor_Provisao_PCLD": valor_provisao,
            "Taxa_Juros_aa": taxa_juros_aa,
            "Receita_Juros_Anual_Estimada": round(saldo_devedor * taxa_juros_aa, 2)
        })
        
    df = pd.DataFrame(contratos)
    caminho = os.path.join(DIRETORIO_DADOS, "Fatos_Carteira_Credito.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Fatos_Carteira_Credito salva com sucesso: {len(df)} contratos ativos.")
    return df


def gerar_fatos_captacao(qtd_operacoes=2200, df_associados=None, df_produtos=None):
    """Gera o histórico e saldo de captação (Depósitos RDC, Poupança e LCA)."""
    logging.info(f"Gerando {qtd_operacoes} operações de captação...")
    
    produtos_captacao = df_produtos[df_produtos["Tipo_Operacao"] == "Captação"].to_dict("records")
    assoc_dict = df_associados.set_index("ID_Associado").to_dict("index")
    ids_associados = list(assoc_dict.keys())
    
    captacoes = []
    data_base = datetime(2026, 8, 31)
    
    for i in range(1, qtd_operacoes + 1):
        id_op = f"CAP{i:06d}"
        id_assoc = random.choice(ids_associados)
        assoc_info = assoc_dict[id_assoc]
        prod = random.choice(produtos_captacao)
        
        # Data de aplicação entre 2023 e 2026
        dt_aplicacao = data_base - timedelta(days=random.randint(15, 900))
        
        # Saldo aplicado conforme segmento
        if assoc_info["Segmento"] == "Pessoa Jurídica":
            saldo_aplicado = round(float(np.random.uniform(50000, 1500000)), 2)
        elif assoc_info["Segmento"] == "Produtor Rural":
            saldo_aplicado = round(float(np.random.uniform(30000, 900000)), 2)
        else:
            saldo_aplicado = round(float(np.random.uniform(1000, 120000)), 2)
            
        captacoes.append({
            "ID_Operacao_Captacao": id_op,
            "ID_Associado": id_assoc,
            "ID_Agencia": assoc_info["ID_Agencia"],
            "ID_Produto": prod["ID_Produto"],
            "Data_Aplicacao": dt_aplicacao.strftime("%Y-%m-%d"),
            "Saldo_Aplicado": saldo_aplicado,
            "Taxa_Remuneracao_aa": prod["Taxa_Juros_aa_Base"],
            "Custo_Captacao_Anual_Estimado": round(saldo_aplicado * prod["Taxa_Juros_aa_Base"], 2)
        })
        
    df = pd.DataFrame(captacoes)
    caminho = os.path.join(DIRETORIO_DADOS, "Fatos_Captacao.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Fatos_Captacao salva com sucesso: {len(df)} registros.")
    return df


def gerar_fatos_metas_agencias(df_agencias=None):
    """Gera as metas mensais de cada Agência para 2025 e 2026."""
    logging.info("Gerando metas mensais por agência...")
    
    agencias = df_agencias.to_dict("records")
    metas = []
    
    meses = pd.date_range(start="2025-01-01", end="2026-12-01", freq="MS")
    
    for mes in meses:
        mes_str = mes.strftime("%Y-%m-%d")
        for ag in agencias:
            multiplicador = 1.6 if ag["Porte"] == "Grande" else 1.0
            
            # Metas proporcionais ao porte
            meta_originacao = round(float(random.uniform(3500000, 6000000) * multiplicador), 2)
            meta_captacao = round(float(random.uniform(3000000, 5500000) * multiplicador), 2)
            meta_npl_maximo = 0.028 # Meta teto de 2,8% de inadimplência Bacen
            
            metas.append({
                "ID_Agencia": ag["ID_Agencia"],
                "Data_Mes": mes_str,
                "Meta_Originacao_Credito": meta_originacao,
                "Meta_Captacao_Depositos": meta_captacao,
                "Meta_Teto_NPL90_Pct": meta_npl_maximo
            })
            
    df = pd.DataFrame(metas)
    caminho = os.path.join(DIRETORIO_DADOS, "Fatos_Metas_Agencias.xlsx")
    df.to_excel(caminho, index=False)
    logging.info(f"Fatos_Metas_Agencias salva com sucesso: {len(df)} registros de metas.")
    return df


# -----------------------------------------------------------------------------
# 3. EXECUÇÃO PRINCIPAL
# -----------------------------------------------------------------------------
def main():
    try:
        logging.info("=== INICIANDO PIPELINE DE GERAÇÃO DE DADOS BANCÁRIOS / SICREDI ===")
        
        # 1. Dimensões
        df_agencias = gerar_dim_agencias()
        df_produtos = gerar_dim_produtos()
        df_associados = gerar_dim_associados(qtd=1500, df_agencias=df_agencias)
        
        # 2. Fatos
        df_credito = gerar_fatos_carteira_credito(qtd_contratos=3500, df_associados=df_associados, df_produtos=df_produtos)
        df_captacao = gerar_fatos_captacao(qtd_operacoes=2200, df_associados=df_associados, df_produtos=df_produtos)
        df_metas = gerar_fatos_metas_agencias(df_agencias=df_agencias)
        
        # Totais para conferência
        total_credito = df_credito["Saldo_Devedor"].sum()
        total_captacao = df_captacao["Saldo_Aplicado"].sum()
        total_pdd = df_credito["Valor_Provisao_PCLD"].sum()
        npl_90_volume = df_credito[df_credito["Dias_Atraso"] > 90]["Saldo_Devedor"].sum()
        npl_90_pct = (npl_90_volume / total_credito) * 100
        
        logging.info("=== RESUMO DOS DADOS GERADOS ===")
        logging.info(f"Carteira Total Ativa: R$ {total_credito:,.2f}")
        logging.info(f"Captação Total (Depósitos): R$ {total_captacao:,.2f}")
        logging.info(f"Provisão PCLD/BACEN: R$ {total_pdd:,.2f}")
        logging.info(f"Volume NPL 90+ (Inadimplência): R$ {npl_90_volume:,.2f} ({npl_90_pct:.2f}%)")
        logging.info("=== PROCESSO CONCLUÍDO COM SUCESSO! ===")
        
    except Exception as e:
        logging.error(f"Erro crítico durante a execução: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
