from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

Perfil = Literal["Administrador", "Operador", "Cliente"]


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)
    perfil: Perfil


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(default=None, min_length=8, max_length=128)
    perfil: Optional[Perfil] = None


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: Perfil

    model_config = {"from_attributes": True}


class LoginInput(BaseModel):
    email: EmailStr
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    usuario: UsuarioOut
