# Projeto: Predição dos Valores de Ações - Banco BTG Pactual

> **Aviso:** Este projeto é meramente acadêmico e não deve ser usado como recomendação financeira.

## Descrição do Projeto

Este projeto tem como objetivo construir um modelo preditivo para estimar o preço futuro das ações do Banco BTG Pactual (símbolo: `BPAC11.SA`).

Os dados foram obtidos via API YahooFinance, cobrindo um período de janeiro de 2015 a julho de 2025.

---

## Coleta e Pré-processamento dos Dados

- Dados extraídos da API do YahooFinance:
  ```symbol = 'BPAC11.SA'```
  ```start_date = '2015-01-01'```
  ```end_date = '2025-07-01'```
  ```df = yf.download(symbol, start=start_date, end=end_date)```

- Seleção da coluna Close para análise.

- Verificação de valores nulos (não foram encontrados).

- Visualização gráfica da série temporal dos preços.

- Normalização dos dados usando MinMaxScaler para faixa [0,1].

- Definição do tamanho da janela para previsão (exemplo: 60 dias).

- Criação de sequências para entrada no modelo LSTM.

- Separação em dados de treino e teste.


## Modelo
**Construído com Keras:**

- Camada LSTM com 50 neurônios.

- Camada densa para saída com 1 neurônio.

- Compilado com loss='mean_squared_error' e otimizador adam.

- Treinamento com callback EarlyStopping para evitar overfitting.

- Métrica de avaliação: RMSE (Root Mean Squared Error).

- Modelo salvo localmente no formato .h5.

- Gráfico comparativo entre valores reais e previstos gerado.


## Deploy da API
- API RESTful criada com FastAPI.

- Endpoint principal: /prever que recebe um JSON com uma lista de preços históricos.

- API processa dados, realiza a normalização, faz a previsão usando o modelo LSTM carregado, e retorna o preço previsto.

- Exemplo da estrutura do JSON recebido:

```{```
  ```"historico": [30.5, 30.6, 30.8, ..., 41.2, 41.4]```
```}```

- Resposta da API:

```{```
```  "preco_previsto": 41.57```
```}```


## Execução
**Executando Localmente**

- Instale as dependências:

```pip install -r requirements.txt```

- Rode a API:

```uvicorn api.main:app --reload --host 0.0.0.0 --port 80```

- Acesse a documentação interativa no navegador: http://localhost/docs


## Executando com Docker
**Crie o Dockerfile (exemplo):**

```FROM python:3.9```

```WORKDIR /code```

```COPY requirements.txt /code/requirements.txt```

```RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt```

```COPY ./app /code/app```

```CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]```

- Construa a imagem:

```docker build -t modelo_lstm .```
```docker run -p 8080:8080 modelo_lstm```

- Acesse a API em: http://localhost/docs


## Testando a API
**Exemplo usando curl:**

```curl -X POST "http://localhost/prever" -H "Content-Type: application/json" ```
```-d "{\"historico\": [30.5, 30.6, 30.8, 31.0, 31.2, 31.5, 31.7, 31.8, 32.0, 32.1, 32.3, 32.5, 32.7, 32.8, 33.0, 33.2, 33.4, 33.6, 33.8, 34.0, 34.1, 34.3, 34.5, 34.7, 34.9, 35.0, 35.2, 35.4, 35.6, 35.8, 36.0, 36.1, 36.3, 36.5, 36.7, 36.9, 37.0, 37.2, 37.4, 37.6, 37.8, 38.0, 38.1, 38.3, 38.5, 38.7, 38.9, 39.0, 39.2, 39.4, 39.6, 39.8, 40.0, 40.1, 40.3, 40.5, 40.7, 40.9, 41.0, 41.2, 41.4]}"```

- Resposta esperada:
```{```
  ```"preco_previsto": 41.57```
```}```


## MLflow
**Usado para monitorar experimentos e registrar métricas, parâmetros e artefatos.**

- Rodar o servidor MLflow local:

```mlflow ui```

- Acesse no navegador: http://localhost:5000
  
- Registra automaticamente métricas do Keras com mlflow.keras.autolog() no script de treinamento.
