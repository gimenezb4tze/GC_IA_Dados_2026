from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

#url das frutas e suas informações
 
URL_BASE = "https://www.fruityvice.com/api/fruit"

# criando nossa api del Chavo

app = FastAPI(title="Casa de sucos")


# criando lista de sucos
sucos_cadastrados = []

# Modelo dos dados recebidos para cadastrar um suco
class SucoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    frutas: list[str] = Field(min_length=1)
    tem_gosto_de: str = Field(min_length=1)

# Função para consultar uma fruta na API Fruityvice.
def consultar_fruta(nome: str):
    """Consulta a fruta na Fruityvice e devolve nome, calorias e açúcar (por 100 g)."""

    fruta = nome.strip().lower()

    # nome vazio cairia no endpoint que lista todas as frutas
    if fruta == "":
        raise HTTPException(
            status_code=400,
            detail="Informe o nome da fruta."
        )

    # consulta por endpoint 
    try:
        resposta = requests.get(f"{URL_BASE}/{fruta}", timeout=10)

    # se não deu para falar com a API (sem internet, timeout...)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível consultar a API de frutas agora. Tente novamente em instantes."
        )

    # se o status estiver OK
    if resposta.status_code == 200:
        dados = resposta.json()
        nutri = dados["nutritions"]

        return {
            "nome": dados["name"],
            "calorias": nutri["calories"],
            "acucar": nutri["sugar"]
        }

    # Se o status for Not Found
    elif resposta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Não encontrei a fruta '{fruta}'. "
                "Tente outra (ex: apple, mango, strawberry)."
            )
        )

    # qualquer outro status que a API de frutas devolver
    else:
        raise HTTPException(
            status_code=502,
            detail=f"A API de frutas respondeu com status {resposta.status_code}."
        )
    
# GET - consultando frutas 
@app.get("/frutas/{nome}")
def obter_fruta(nome: str):
    return consultar_fruta(nome)

# POST - Criar Sucos
@app.post("/sucos", status_code=201)
def criar_suco(suco : SucoEntrada):
    nomes_frutas = []

    total_calorias = 0
    total_acucar = 0    

    # consulta todas as frutas antes de salvar, se alguma falhar nada é cadastrado
    for nome_fruta in suco.frutas:
        fruta = consultar_fruta(nome_fruta)

        nomes_frutas.append(fruta["nome"].lower())
        total_calorias += fruta["calorias"]
        total_acucar += fruta["acucar"]

    novo_suco = {
        "id": len(sucos_cadastrados) + 1,
        "nome": suco.nome,
        "frutas": nomes_frutas,
        "tem_gosto_de": suco.tem_gosto_de,
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }

    sucos_cadastrados.append(novo_suco)

    return novo_suco

# GET - listagem dos sucos cadastrados
@app.get("/sucos")
def listar_sucos():
    return sucos_cadastrados