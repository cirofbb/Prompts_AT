# Solução de IA para Processamento de Dados da Câmara dos Deputados do Brasil

## Resumo do Projeto
Este projeto tem como objetivo desenvolver uma solução baseada em Inteligência Artificial para processar e analisar informações da Câmara dos Deputados do Brasil. A solução realiza coleta e processamento de dados textuais e imagens utilizando APIs públicas, permitindo a visualização de resultados e interação com o usuário por meio de Modelos de Linguagem de Última Geração (LLMs).

### Componentes do Projeto

#### 1. **Parte Offline (dataprep.py):**
- **Coleta de dados**: Extração de informações das APIs públicas da Câmara dos Deputados.
- **Processamento**:
  - Geração de sumarizações dos textos coletados.
  - Análises automáticas com base em prompts configurados.
  - Marcação de palavras-chave para identificação rápida de conteúdos relevantes.
- **Bases vetoriais**: Criação de bases vetoriais utilizando FAISS para referência posterior no ambiente online.

#### 2. **Parte Online (dashboard.py):**
- **Visualização**:
  - Dashboard interativo com Streamlit para apresentar as informações coletadas e analisadas.
  - Apresentação de insights, estatísticas e dados relevantes.
- **Interação**:
  - Interface de chat com assistente virtual utilizando Modelos de Linguagem.
  - Consulta de informações por meio de buscas vetoriais baseadas em embeddings.

### URL Base
Todas as requisições de coleta de dados são realizadas a partir da URL:
```
https://dadosabertos.camara.leg.br/api/v2/
```

### Período de Referência
- **Início:** 01/08/2024
- **Fim:** 30/08/2024 (datas inclusivas)

---

## Requisitos do Projeto

### Dependências
Certifique-se de instalar os pacotes listados abaixo antes de executar o projeto:

- **Python 3.10+**
- **Bibliotecas**:
  - `streamlit`
  - `langchain`
  - `langchain-community`
  - `faiss-cpu`
  - `openai`
  - `requests`
  - `json`

### Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/repositorio.git
   cd repositorio
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração
- **Chaves de API:**
  - Gere uma chave de API para acesso à OpenAI ou outro provedor de LLM e configure-a em um arquivo `.env`:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

### Execução

#### Parte Offline (dataprep.py):
Para realizar a coleta e preparação dos dados:
```bash
python dataprep.py
```

#### Parte Online (dashboard.py):
Para iniciar o dashboard interativo:
```bash
streamlit run dashboard.py
```

---

## Funcionalidades Planejadas

- **Sumarizações automáticas** de textos legislativos.
- **Busca vetorial** eficiente com FAISS para consulta de documentos.
- **Assistente virtual interativo** com capacidades de resposta em linguagem natural.
- **Visualização dinâmica** de insights e análises extraídas dos dados.

---

## Estrutura do Repositório

```
├── dataprep.py       # Script para coleta e preparação de dados
├── dashboard.py     # Script para o dashboard interativo
├── requirements.txt # Lista de dependências do projeto
├── .env.example     # Modelo de arquivo de configuração
└── README.md       # Documentação do projeto
```

---

## Observações
- Certifique-se de que a API da Câmara dos Deputados está acessível.
- Atualize suas dependências regularmente para evitar problemas de compatibilidade.

---
