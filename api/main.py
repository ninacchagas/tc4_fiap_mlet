from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# Instância do app FastAPI
app = FastAPI(title="Previsão de Preço de Ações do Banco BTG")

# Caminho absoluto para o modelo, compatível com Docker
caminho_modelo = os.path.join(os.path.dirname(__file__), "..", "modelo", "models_saved", "modelo_lstm.h5")
caminho_modelo = os.path.abspath(caminho_modelo)

model = load_model(caminho_modelo)

# Número de dias usados na janela de entrada (igual ao treinamento)
previsao_em_dias = 60

# Define o formato esperado para o input
class Historico(BaseModel):
    historico: list  # lista de valores numéricos (floats ou ints)

# Rota de status da API
@app.get("/")
def status():
    return {"mensagem": "A API de Previsão de Preço de Ações do Banco BTG está funcionando"}

# Rota de predição
@app.post("/prever")
async def prever(data: Historico):
    """
    Recebe um histórico de preços e retorna a previsão do próximo valor.
    
    Exemplo de input:
    {
      "historico": [12.5, 12.6, ..., 18.6]  # mínimo 60 valores
    }
    """
    try:
        # Converte entrada em array e reshape para (n, 1)
        valores = np.array(data.historico).reshape(-1, 1)

        # Verifica se há dados suficientes
        if len(valores) < previsao_em_dias:
            raise HTTPException(
                status_code=400,
                detail=f"É necessário fornecer pelo menos {previsao_em_dias} valores históricos."
            )

        # Normaliza os dados com MinMaxScaler (atenção: ideal usar scaler do treino!)
        scaler = MinMaxScaler()
        valores_normalizados = scaler.fit_transform(valores)

        # Seleciona os últimos 60 dias e adapta forma de entrada para o modelo
        entrada = valores_normalizados[-previsao_em_dias:].reshape(1, previsao_em_dias, 1)

        # Realiza a predição
        predicao_normalizada = model.predict(entrada)
        predicao_real = scaler.inverse_transform(predicao_normalizada)

        # Retorna o valor previsto como float simples
        return {"preco_previsto": float(predicao_real[0][0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {str(e)}")
