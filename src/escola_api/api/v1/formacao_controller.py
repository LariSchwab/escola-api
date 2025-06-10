from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.escola_api.app import router
from src.escola_api.database.modelos import FormacaoEntidade
from src.escola_api.dependencias import get_db
from src.escola_api.schemas.formacao_schemas import FormacaoEditar, FormacaoCadastro


@router.get("/api/formacoes", tags=["formacoes"])
def listar_todas_formacoes(db: Session = Depends(get_db)):
    formacoes = db.query(FormacaoEntidade).all()
    return formacoes


@router.get("/api/formacoes/{id}")
def obter_por_id_formacao(id: int, db: Session = Depends(get_db)):
    formacao = db.query(FormacaoEntidade).filter(FormacaoEntidade.id == id).first()
    if formacao:
        return formacao

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Formação não encontrada com id: {id}")


@router.post("/api/formacoes", tags=["formacoes"])
def cadastrar_formacao(form: FormacaoCadastro, db: Session = Depends(get_db)):
    formacao = FormacaoCadastro(nome=form.nome, descricao=form.descricao, duracao=form.duracao)
    db.add(formacao)
    db.commit()
    db.refresh(formacao)

    return formacao


@router.delete("/api/formacoes/{id}", status_code=204, tags=["formacoes"])
def apagar_curso(id: int, db: Session = Depends(get_db)):
    formacao = db.query(FormacaoEntidade).filter(FormacaoEntidade.id == id).first()
    if formacao:
        db.delete(formacao)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Formação não encontrado com id: {id}")


@router.put("/api/formacoes/{id}", status_code=204, tags=["formacoes"])
def editar_formacao(id: int, form: FormacaoEditar, db: Session = Depends(get_db)):
    formacao = db.query(FormacaoEntidade).filter(FormacaoEntidade.id == id).first()
    if formacao:
        formacao.nome = form.nome
        formacao.descricao = form.descricao
        formacao.duracao = form.duracao
        db.commit()
        db.refresh(formacao)
        return formacao
    raise HTTPException(status_code=404, detail=f"Formação não encontrado com id: {id}")
