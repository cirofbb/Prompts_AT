import requests
import pandas as pd

url_base = "https://dadosabertos.camara.leg.br/api/v2"

def deputados():
    url = f"{url_base}/deputados"
    response = requests.get(url, params={'dataInicio': '2024-08-01', 'dataFim': '2024-08-30'})
    
    if response.status_code == 200:
        deputados_data = response.json()["dados"]
        df_deputados = pd.DataFrame(deputados_data)
        df_deputados.to_parquet("data/deputados.parquet", index=False)
        print("Dados dos deputados salvos em data/deputados.parquet")
    else:
        print(f"Erro ao acessar API: {response.status_code}")
    
    return deputados


def despesas():
    df_deputados = pd.read_parquet("data/deputados.parquet")
    lista_despesas = []

    for _, deputado in df_deputados.iterrows():
        deputado_id = deputado["id"]
        url = f"{url_base}/deputados/{deputado_id}/despesas"
        response = requests.get(url, params={'dataInicio': '2024-08-01', 'dataFim': '2024-08-30'})
        
        if response.status_code == 200:
            despesas_data = response.json()["dados"]
            for despesa in despesas_data:
                despesa["deputado_id"] = deputado_id
                despesa["nome"] = deputado["nome"]
                lista_despesas.append(despesa)
        else:
            print(f"Erro ao acessar despesas do deputado {deputado_id}: {response.status_code}")

    df_despesas = pd.DataFrame(lista_despesas)
    df_despesas_grouped = df_despesas.groupby(["dataDocumento", "nome", "tipoDespesa"]).sum().reset_index()
    df_despesas_grouped.to_parquet("data/serie_despesas_diárias_deputados.parquet", index=False)
    print("Dados de despesas salvos em data/serie_despesas_diárias_deputados.parquet")

    return despesas


