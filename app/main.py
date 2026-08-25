import os
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas
from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    criar_token,
    exigir_perfis,
    gerar_hash_senha,
    get_current_user,
    verificar_senha,
)
from .database import Base, SessionLocal, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST Segura para Gestão de Usuários",
    version="1.0.0",
    description=(
        "API acadêmica com CRUD de usuários, autenticação JWT "
        "e autorização por perfis RBAC."
    ),
)

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


def criar_admin_inicial():
    db = SessionLocal()
    try:
        existe_admin = (
            db.query(models.Usuario)
            .filter(models.Usuario.perfil == "Administrador")
            .first()
        )

        if existe_admin:
            return

        nome = os.getenv("ADMIN_NAME", "Administrador")
        email = os.getenv("ADMIN_EMAIL", "admin@demo.com").lower()
        senha = os.getenv("ADMIN_PASSWORD", "Admin@123")

        usuario = models.Usuario(
            nome=nome,
            email=email,
            senha_hash=gerar_hash_senha(senha),
            perfil="Administrador",
        )
        db.add(usuario)
        db.commit()
    finally:
        db.close()


criar_admin_inicial()


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


@app.post(
    "/login",
    response_model=schemas.TokenOut,
    tags=["Autenticação"],
)
def login(dados: schemas.LoginInput, db: Session = Depends(get_db)):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == dados.email.lower())
        .first()
    )

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    token = criar_token(usuario)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "usuario": usuario,
    }


@app.get(
    "/me",
    response_model=schemas.UsuarioOut,
    tags=["Usuários"],
)
def meus_dados(usuario: models.Usuario = Depends(get_current_user)):
    return usuario


@app.get(
    "/usuarios",
    response_model=List[schemas.UsuarioOut],
    tags=["Usuários"],
)
def listar_usuarios(
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(
        exigir_perfis("Administrador", "Operador")
    ),
):
    return db.query(models.Usuario).order_by(models.Usuario.id).all()


@app.get(
    "/usuarios/{usuario_id}",
    response_model=schemas.UsuarioOut,
    tags=["Usuários"],
)
def consultar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(get_current_user),
):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    if atual.perfil == "Cliente" and atual.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cliente pode visualizar apenas seus próprios dados.",
        )

    return usuario


@app.post(
    "/usuarios",
    response_model=schemas.UsuarioOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuários"],
)
def criar_usuario(
    dados: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(exigir_perfis("Administrador")),
):
    email = dados.email.lower()

    existente = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == email)
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este e-mail.",
        )

    usuario = models.Usuario(
        nome=dados.nome.strip(),
        email=email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@app.put(
    "/usuarios/{usuario_id}",
    response_model=schemas.UsuarioOut,
    tags=["Usuários"],
)
def atualizar_usuario(
    usuario_id: int,
    dados: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(
        exigir_perfis("Administrador", "Operador")
    ),
):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    if atual.perfil == "Operador" and "perfil" in alteracoes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operador não pode alterar perfis de acesso.",
        )

    if "email" in alteracoes:
        novo_email = str(alteracoes["email"]).lower()
        conflito = (
            db.query(models.Usuario)
            .filter(
                models.Usuario.email == novo_email,
                models.Usuario.id != usuario_id,
            )
            .first()
        )
        if conflito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um usuário com este e-mail.",
            )
        usuario.email = novo_email

    if "nome" in alteracoes:
        usuario.nome = alteracoes["nome"].strip()

    if "senha" in alteracoes:
        usuario.senha_hash = gerar_hash_senha(alteracoes["senha"])

    if "perfil" in alteracoes:
        usuario.perfil = alteracoes["perfil"]

    db.commit()
    db.refresh(usuario)

    return usuario


@app.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Usuários"],
)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    atual: models.Usuario = Depends(exigir_perfis("Administrador")),
):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    if atual.id == usuario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O administrador autenticado não pode excluir a própria conta.",
        )

    db.delete(usuario)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
