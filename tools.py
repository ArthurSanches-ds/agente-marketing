import pandas as pd


def menor_custo_por_lead():
    df = pd.read_csv("dados_campanhas.csv")
    df["custo_por_lead"] = df["investimento"] / df["leads"]
    resultado = df.groupby("campanha")["custo_por_lead"].mean()
    melhor = resultado.idxmin()
    valor = resultado.min()
    return f"A campanha com menor custo por lead é '{melhor}' com média de R$ {valor:.2f} por lead."


def melhor_engajamento():
    df = pd.read_csv("dados_campanhas.csv")
    resultado = df.groupby("campanha")[["cliques", "visualizacoes"]].sum()
    melhor_cliques = resultado["cliques"].idxmax()
    melhor_views = resultado["visualizacoes"].idxmax()
    return (
        f"Maior número de cliques: '{melhor_cliques}' com {resultado['cliques'].max()} cliques.\n"
        f"Maior número de visualizações: '{melhor_views}' com {resultado['visualizacoes'].max()} visualizações."
    )


def analisar_fechamentos():
    df = pd.read_csv("dados_campanhas.csv")
    resultado = df.groupby("campanha")["fechamentos"].sum()
    melhor = resultado.idxmax()
    valor = resultado.max()
    return f"A campanha com mais fechamentos é '{melhor}' com {valor} fechamentos no total."


def calcular_roi():
    df = pd.read_csv("dados_campanhas.csv")
    resultado = df.groupby("campanha")[
        ["investimento", "receita_gerada"]].sum()
    resultado["roi"] = ((resultado["receita_gerada"] -
                        resultado["investimento"]) / resultado["investimento"]) * 100
    melhor = resultado["roi"].idxmax()
    resposta = ""
    for campanha, row in resultado.iterrows():
        resposta += f"{campanha}: investiu R$ {row['investimento']:.2f}, gerou R$ {row['receita_gerada']:.2f}, ROI de {row['roi']:.1f}%\n"
    resposta += f"\nMelhor ROI: '{melhor}'"
    return resposta


def resumo_semanal():
    df = pd.read_csv("dados_campanhas.csv")
    resultado = df.groupby("semana")[
        ["investimento", "leads", "fechamentos", "receita_gerada"]].sum()
    resposta = ""
    for semana, row in resultado.iterrows():
        resposta += f"Semana {semana}: investiu R$ {row['investimento']:.2f}, {row['leads']} leads, {row['fechamentos']} fechamentos, receita R$ {row['receita_gerada']:.2f}\n"
    return resposta
