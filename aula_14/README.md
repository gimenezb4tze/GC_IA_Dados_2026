# Casa de Sucos do Chaves
API REST em Python que cadastra sucos e calcula seus valores nutricionais usando dados da API pública Fruityvice.

## Sobre o projeto
Projeto desenvolvido como atividade da aula 14 da Trilha de IA e Dados (GC 26), com o objetivo de praticar o consumo e a criação de APIs, endpoints, métodos HTTP, JSON e tratamento de erros.

A aplicação atua como servidor, expondo rotas para consultar frutas e cadastrar sucos, e como cliente da [Fruityvice](https://www.fruityvice.com/api/fruit/), de onde obtém as informações nutricionais de cada fruta.

## Funcionalidades

- Consultar uma fruta na Fruityvice, retornando apenas nome, calorias e açúcar
- Cadastrar sucos com nome, lista de frutas e descrição do gosto
- Calcular o total de calorias e de açúcar de cada suco
- Listar os sucos cadastrados com seus valores nutricionais
- Tratar erros com mensagens claras
- Documentação interativa gerada automaticamente pelo Swagger

## Tecnologias

| Tecnologia | Uso no projeto |
|---|---|
| Python 3.14 | Linguagem principal |
| FastAPI | Criação da API e das rotas |
| Pydantic | Modelo e validação dos dados recebidos |
| Uvicorn | Servidor que executa a aplicação |
| Requests | Consumo da API Fruityvice |
| venv | Ambiente virtual do projeto |
| Swagger (OpenAPI) | Documentação e testes dos endpoints |

## Estrutura do projeto

```text
aula_14/
├── evidencias/
│   ├── get_frutas_banana_200.png
│   ├── get_frutas_invalida_404.png
│   ├── post_sucos_201.png
│   ├── post_sucos_fruta_invalida_404.png
│   └── get_sucos_200.png
├── .gitignore
├── casa_sucos_api.py
├── README.md
└── requirements.txt
```

## Como executar

### Pré-requisitos

- Python instalado (testado com a versão 3.14)
- Git
- Conexão com a internet, para consultar a Fruityvice

### Passo a passo

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO/aula_14
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicie o servidor:

```bash
py -m uvicorn casa_sucos_api:app --reload
```

**Em macOS ou Linux, use** `python3 -m uvicorn casa_sucos_api:app --reload`.

5. Acesse a documentação interativa em http://127.0.0.1:8000/docs

## Endpoints

| Método | Rota | Descrição | Sucesso |
|---|---|---|---|
| GET | `/frutas/{nome}` | Consulta uma fruta na Fruityvice | 200 |
| POST | `/sucos` | Cadastra um suco e calcula os totais | 201 |
| GET | `/sucos` | Lista todos os sucos cadastrados | 200 |

Os nomes das frutas devem ser digitados em inglês (por exemplo: `banana`, `strawberry`, `apple`), pois é o idioma da Fruityvice.

### GET /frutas/{nome}

Consulta uma fruta e devolve somente nome, calorias e açúcar.

Exemplo: `GET /frutas/banana`

```json
{
  "nome": "Banana",
  "calorias": 96,
  "acucar": 17.2
}
```

### POST /sucos

Cadastra um suco. A API consulta cada fruta na Fruityvice e soma as calorias e o açúcar.

Corpo da requisição:

```json
{
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo"
}
```

Resposta (201 Created):

```json
{
  "id": 1,
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo",
  "total_calorias": 125,
  "total_acucar": 22.6
}
```

### GET /sucos

Devolve a lista de todos os sucos cadastrados.

```json
[
  {
    "id": 1,
    "nome": "Vitamina Tropical",
    "frutas": ["banana", "strawberry"],
    "tem_gosto_de": "Tamarindo",
    "total_calorias": 125,
    "total_acucar": 22.6
  }
]
```
## Regras de negócio

- Os cálculos consideram 100 g de cada fruta informada.
- O total do suco é a soma dos valores de cada fruta.
- Se qualquer fruta falhar na consulta, nenhum suco é cadastrado.
- Os sucos são guardados em memória: ao reiniciar o servidor, a lista é zerada.

## Tratamento de erros

Os erros retornam uma mensagem no campo `detail`:

```json
{
  "detail": "Não encontrei a fruta 'tamarindo'. Tente outra (ex: apple, mango, strawberry)."
}
```

| Código | Quando acontece |
|---|---|
| 400 Bad Request | O nome da fruta veio vazio |
| 404 Not Found | A fruta não existe na Fruityvice |
| 422 Unprocessable Entity | O corpo do `POST /sucos` está inválido (campo faltando, vazio ou com tipo errado) |
| 502 Bad Gateway | A Fruityvice respondeu com um status inesperado |
| 503 Service Unavailable | Não foi possível acessar a Fruityvice (sem internet ou tempo esgotado) |

## Evidências de testes

Testes realizados pelo Swagger (`/docs`).

GET /frutas/banana (200):

![GET fruta existente](evidencias/get_frutas_banana_200.png)

GET /frutas/xyz (404):

![GET fruta inexistente](evidencias/get_frutas_invalida_404.png)

POST /sucos (201):

![POST suco](evidencias/post_sucos_201.png)

POST /sucos com fruta inválida (404, nada é salvo):

![POST com fruta inválida](evidencias/post_sucos_fruta_invalida_404.png)

GET /sucos (200):

![GET sucos](evidencias/get_sucos_200.png)

### Trilha de IA e Dados, GC 26 (aula 14).