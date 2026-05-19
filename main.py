from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="API Biblioteca de Jogos", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str

class JogoCreate(BaseModel):
    nome: str
    tipo: str
    nota: int
    review: str

class JogoUpdate(BaseModel):
    nome: str
    tipo: str
    nota: int
    review: str

class JogoResponse(BaseModel):
    id: int
    nome: str
    tipo: str
    nota: int
    review: str

jogos_db = {}
next_id = 1

jogos_db[1] = {
    "id": 1,
    "nome": "The Legend of Zelda",
    "tipo": "Aventura",
    "nota": 10,
    "review": "Um clássico absoluto."
}
jogos_db[2] = {
    "id": 2,
    "nome": "FIFA 23",
    "tipo": "Esporte",
    "nota": 7,
    "review": "Bom para jogar com amigos."
}
next_id = 3


@app.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(credentials: LoginRequest):
    if credentials.email == "usuario@esoft.com" and credentials.password == "Abc123":
        token = str(uuid.uuid4())
        return LoginResponse(token=token)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas"
    )


@app.get("/jogos", response_model=List[JogoResponse], status_code=status.HTTP_200_OK)
async def listar_jogos():
    return list(jogos_db.values())


@app.get("/jogos/{id}", response_model=JogoResponse, status_code=status.HTTP_200_OK)
async def buscar_jogo(id: int):
    if id not in jogos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado"
        )

    return jogos_db[id]


@app.post("/jogos", response_model=JogoResponse, status_code=status.HTTP_201_CREATED)
async def criar_jogo(jogo: JogoCreate):
    global next_id

    novo_jogo = {
        "id": next_id,
        "nome": jogo.nome,
        "tipo": jogo.tipo,
        "nota": jogo.nota,
        "review": jogo.review
    }

    jogos_db[next_id] = novo_jogo
    next_id += 1

    return novo_jogo


@app.put("/jogos/{id}", response_model=JogoResponse, status_code=status.HTTP_200_OK)
async def atualizar_jogo(id: int, jogo: JogoUpdate):
    if id not in jogos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado"
        )

    jogo_atualizado = {
        "id": id,
        "nome": jogo.nome,
        "tipo": jogo.tipo,
        "nota": jogo.nota,
        "review": jogo.review
    }

    jogos_db[id] = jogo_atualizado

    return jogo_atualizado


@app.delete("/jogos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_jogo(id: int):
    if id not in jogos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogo não encontrado"
        )

    del jogos_db[id]

    return None
