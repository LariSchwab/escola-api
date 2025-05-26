from dataclasses import dataclass, field
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.openapi.models import Response
from fastapi.openapi.utils import status_code_ranges
app = FastAPI()

@app.get("/")
def index():
    return {"dados": "Hello World"}

@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"soma": soma}

# http://127.0.0.1:8000/processar-cliente?nome=Pedro&sobrenome=Pascal&idade=27
@app.get("/processar-cliente")
def processar_cliente(nome: str, idade: int, sobrenome: str):
    nome_completo = nome + " " + sobrenome
    ano_nascimento = datetime.now().year - idade

    if ano_nascimento >= 1990 and ano_nascimento <= 2000:
        decada = "decada de 90"
    elif ano_nascimento >= 1980 and ano_nascimento <= 1990:
        decada = "decada de 80"
    elif ano_nascimento >= 1970 and ano_nascimento <= 1980:
        decada = "decada de 70"
    else:
        decada = "decada abaixo de 70 ou acima de 90"

    return {
        "nome": nome_completo,
        "ano_nascimento": ano_nascimento,
        "decada": decada,
    }
@dataclass
class Curso:
    id: int = field()
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoCadastro:
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoEditar:
    nome: str = field()
    sigla: str = field()

cursos = [
    # instanciando um objeto da Class Curso
    Curso(id = 1, nome = "Python Web", sigla="PY1"),
    Curso(id = 2, nome = "Git e GitHub", sigla="GT")
]
@app.get("/api/cursos")
def listar_todos_cursos():
    return cursos

@app.get("/api/cursos/{id}")
def obter_por_id_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            return curso

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

@app.post("/api/cursos")
def cadastrar_curso(form: CursoCadastro):
    ultimo_id = max([curso.id for curso in cursos], default=0)

    # instanciar um objeto da classe Curso
    curso = Curso(id = ultimo_id + 1, nome=form.nome, sigla=form.sigla)

    cursos.append(curso)

    return curso

@app.delete("/api/cursos/{id}", status_code=204)
def apagar_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            cursos.remove(curso)
            return
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

@app.put("/api/cursos/{id}")
def editar_curso(id: int, form: CursoEditar):
    for curso in cursos:
        if curso.id == id:
            curso.nome = form.nome
            curso.sigla = form.sigla
            return curso
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


@dataclass
class Aluno:
    id: int = field()
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: datetime = field()

@dataclass
class AlunoCadastro:
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: str = field()

@dataclass
class AlunoEditar:
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: str = field()

alunos = [
    # instanciando um objeto da Class Aluno
    Aluno(id = 1, nome = "João", sobrenome="Diniz", cpf="062.950.959-55", data_nascimento=datetime(1990, 5, 25))
]
@app.get("/api/alunos")
def listar_todos_alunos():
    return alunos

@app.get("/api/alunos/{id}")
def obter_por_id_alunos(id: int):
    for aluno in alunos:
        if aluno.id == id:
            return aluno

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")

@app.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro):
    ultimo_id = max([aluno.id for aluno in alunos], default=0)

    # instanciar um objeto da classe Aluno
    aluno = Aluno(
        id = ultimo_id + 1,
        nome=form.nome,
        sobrenome=form.sobrenome,
        cpf=form.cpf,
        data_nascimento=datetime.fromisoformat(form.data_nascimento))

    alunos.append(aluno)

    return aluno

@app.delete("/api/alunos/{id}", status_code=204)
def apagar_aluno(id: int):
    for aluno in alunos:
        if aluno.id == id:
            alunos.remove(aluno)
            return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")

@app.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar):
    for aluno in alunos:
        if aluno.id == id:
            aluno.nome = form.nome
            aluno.sobrenome = form.sobrenome
            aluno.cpf = form.cpf
            aluno.data_nascimento = datetime.fromisoformat(form.data_nascimento)
            return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


if __name__ == "__main__":
    uvicorn.run("main:app")