import streamlit as st
import pandas as pd
import yaml
from PIL import Image
import json
import plotly.express as px
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import os
import faiss

# Configurações do Streamlit
st.set_page_config(page_title="Dashboard - Câmara dos Deputados (ago/2024)", layout="wide")

# Carregar o arquivo de configuração YAML
with open('./data/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Carregando os dados para o assistente virtual
deputados = pd.read_parquet("./data/deputados.parquet")
despesas = pd.read_parquet("./data/serie_despesas_diárias_deputados.parquet")
proposicoes = pd.read_parquet("./data/proposicoes_deputados.parquet")
with open("./data/insights_despesas_deputados.json", 'r') as f:
    insights_despesas = json.load(f)

# Carregando os modelos
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
model_embedding = SentenceTransformer('neuralmind/bert-base-portuguese-cased', cache_folder='./data/embeddings_cache')

# Organizando os embeddings
dados_camara = []
for registro_deputado in deputados.values.tolist():
    dados_camara.append(registro_deputado)

for registro_despesa in despesas.values.tolist():
    dados_camara.append(registro_despesa)

for registro_proposicao in proposicoes.values.tolist():
    dados_camara.append(registro_proposicao)

with open('./data/insights_despesas_deputados.json') as arquivo_despesas:
    dados_despesas = json.load(arquivo_despesas)
    for insight in dados_despesas['insights']:
        for chave, texto in insight.items():
            dados_camara.append([chave, texto])
    dados_camara.extend(dados_despesas.get('conclusoes', []))
    dados_camara.extend(dados_despesas.get('limitacoes', []))

with open('./data/insights_distribuicao_deputados.json') as arquivo_distribuicao:
    dados_distribuicao = json.load(arquivo_distribuicao)
    dados_camara.append(dados_distribuicao)

with open('./data/sumarizacao_proposicoes.json', encoding='utf-8') as arquivo_proposicoes:
    dados_resumidos = arquivo_proposicoes.read()
    dados_camara.append(dados_resumidos)

dados_camara_processados = []
for item in dados_camara:
    if isinstance(item, list):  # Se for uma lista, converte para uma string concatenada
        dados_camara_processados.append(' '.join(map(str, item)))
    elif isinstance(item, (str, int, float)):  # Se for string, número inteiro ou float
        dados_camara_processados.append(str(item))
    else:  # Ignorar tipos incompatíveis
        continue

# Menu
page = st.sidebar.radio("Navegação", ["Overview", "Despesas", "Proposições", 'Assistente virtual'])

if page == "Overview":
    st.title("Overview: Câmara dos Deputados")
    st.write(config['data']['config']['overview_summary'])

    try:
        st.markdown('---')
        st.subheader("Distribuição dos Deputados")
        image = Image.open('./docs/distribuicao_deputados.png')
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.error("Imagem não encontrada. Certifique-se de que o arquivo 'distribuicao_deputados.png' esteja na pasta './docs/'")
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")


    try:
        st.markdown('---')
        st.subheader("Insights sobre a Distribuição")
        with open('./data/insights_distribuicao_deputados.json', 'r') as f:
            insights_data = json.load(f)
            insights = insights_data['insights']
            for insight in insights:
                st.write(f"- {insight}") #Assumindo que insight é uma string, ajuste conforme a estrutura real

    except FileNotFoundError:
        st.error("Arquivo JSON não encontrado. Certifique-se de que o arquivo 'insights_distribuicao_deputados.json' esteja na pasta './data/'")
    except KeyError:
        st.error("Chave 'insights' não encontrada no arquivo JSON.")
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o arquivo JSON. Verifique se o arquivo está bem formatado.")



elif page == "Despesas":
    st.title("Despesas dos Deputados")

    try:
        with open('./data/insights_despesas_deputados.json', 'r') as f:
            insights_data = json.load(f)
            for insight in insights_data['insights']:
                for key, value in insight.items():
                    st.write(f"**{key}:** {value}")

    except FileNotFoundError:
        st.error("Arquivo JSON não encontrado. Certifique-se de que o arquivo 'insights_despesas_deputados.json' esteja na pasta './data/'")
    except KeyError:
        st.error("Chave 'insights' não encontrada no arquivo JSON.")
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o arquivo JSON. Verifique se o arquivo está bem formatado.")


    try:
        df_despesas = pd.read_parquet('./data/serie_despesas_diárias_deputados.parquet')
        deputados = df_despesas['nome'].unique()
        deputado_selecionado = st.selectbox('Selecione um Deputado:', deputados)

        df_deputado = df_despesas[df_despesas['nome'] == deputado_selecionado]
        df_deputado['data_documento'] = pd.to_datetime(df_deputado['data_documento'])
        df_deputado = df_deputado.sort_values(by='data_documento')
        df_deputado = df_deputado.groupby('data_documento')['valor_documento'].sum().reset_index()


        fig = px.bar(df_deputado, x='data_documento', y='valor_documento', title=f'Despesas de {deputado_selecionado}')
        st.plotly_chart(fig)

    except FileNotFoundError:
        st.error("Arquivo Parquet não encontrado. Certifique-se de que o arquivo 'serie_despesas_diárias_deputados.parquet' esteja na pasta './data/'")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

elif page == "Proposições":
    st.title("Proposições")

    try:
        df_proposicoes = pd.read_parquet('./data/proposicoes_deputados.parquet')
        st.dataframe(df_proposicoes)

    except FileNotFoundError:
        st.error("Arquivo Parquet não encontrado. Certifique-se de que o arquivo 'proposicoes_deputados.parquet' esteja na pasta './data/'")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")


    try:
        with open('./data/sumarizacao_proposicoes.json', 'r', encoding='utf-8') as f:
            sumarizacao_data = json.load(f)
            for sumario in sumarizacao_data['sumarizacao_proposicoes']:
                st.write(sumario)

    except FileNotFoundError:
        st.error("Arquivo JSON não encontrado. Certifique-se de que o arquivo 'sumarizacao_proposicoes.json' esteja na pasta './data/'")
    except KeyError:
        st.error("Chave 'sumarizacao_proposicoes' não encontrada no arquivo JSON.")
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o arquivo JSON. Verifique se o arquivo está bem formatado.")

elif page == 'Assistente virtual': # foi necessário separar o assistente da página de proposições pelo tempo de carregamento
    if 'embeddings' not in st.session_state:
        with st.spinner('Preparando a base de dados... Isso pode levar alguns minutos.'):
            st.session_state['embeddings'] = model_embedding.encode(dados_camara_processados, convert_to_numpy=True)

    st.title('Assistente virtual')
    st.write('Interaja com nosso assistente sobre temas relacionados à Câmara dos Deputados.')

    # Configuração dos avatares
    icones = {
        'usuario': 'user',
        'assistente': 'assistant'
    }

    # Configuração do índice FAISS
    dimensao_embeddings = st.session_state['embeddings'].shape[1]
    indice_faiss = faiss.IndexFlatL2(dimensao_embeddings)
    indice_faiss.add(st.session_state['embeddings'])

    # Entrada do usuário
    if entrada_usuario := st.chat_input('Digite sua mensagem aqui:'):
        st.chat_message('user').write(entrada_usuario)
        with st.spinner('Processando sua solicitação...'):
            try:
                entrada_embedding = model_embedding.encode([entrada_usuario], convert_to_numpy=True)

                top_k = 20
                contexto_respostas = []
                distancias, indices = indice_faiss.search(entrada_embedding, top_k)

                for i in range(top_k):
                    item_base = dados_camara[indices[0][i]]
                    if isinstance(item_base, list):
                        contexto_respostas.append(' '.join(map(str, item_base)))
                    elif isinstance(item_base, str):
                        contexto_respostas.append(item_base)

                
                instrucoes_modelo = f"""
                Você é um especialista em política brasileira e na Câmara dos Deputados em Brasília.

                Baseando-se nas informações abaixo, responda a pergunta do usuário.

                • Pergunta:
                {entrada_usuario}

                • Base de Dados:
                {' '.join(contexto_respostas)}
                """

                resposta_gerada = model.generate_content(instrucoes_modelo).text
                st.chat_message('assistant').write(resposta_gerada)
            except:
                st.error('Ocorreu um erro ao processar a resposta.')