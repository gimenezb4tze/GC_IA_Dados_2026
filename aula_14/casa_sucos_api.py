from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests
 
URL_BASE = "https://www.fruityvice.com/api/fruit"

app = FastAPI(title="Casa de sucos")

sucos_cadastrados = []

# Modelo dos dados recebidos para cadastrar um suco
class SucoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    frutas: list[str] = Field(min_length=1)
    descricao_gosto: str = Field(min_length=1)

# Função de consultar fruta
def consultar_fruta(nome: str):
    """Consulta uma fruta na API Fruityvice."""

    fruta = nome.strip().lower()

    if fruta == "sair":
        print("Até mais!")
        return

    try:
        resposta = requests.get(f"{URL_BASE}/{fruta}", timeout=10)

        if resposta.status_code == 200:
            dados = resposta.json()
            nutri = dados["nutritions"]

            print(f"\n{dados['name']} (família {dados['family']})")
            print(f"   Calorias: {nutri['calories']} kcal")
            print(f"   Açúcar:   {nutri['sugar']} g")

            return {
                "nome": dados["name"],
                "calorias": nutri["calories"],
                "acucar": nutri["sugar"]
            }

        elif resposta.status_code == 404:
            print(
                f"Não encontrei a fruta '{fruta}'. "
                "Tente outra (ex: apple, mango, strawberry)."
            )
            return None

        else:
            print(f"A API respondeu com status {resposta.status_code}.")
            return None

    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão: {erro}")
        return None
    
# GET - consultando frutas 
@app.get("/frutas/{nome}")
def obter_fruta(nome: str):
    fruta = consultar_fruta(nome)

    if fruta is None:
        raise HTTPException(
            status_code=404,
            detail="Fruta não encontrada ou não foi possível consultar."
        )

    return fruta

