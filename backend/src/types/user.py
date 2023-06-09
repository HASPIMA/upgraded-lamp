from pydantic import BaseModel, EmailStr


class SignupUser(BaseModel):
    nombre: str
    identificacion: str
    correo_electronico: EmailStr
    contrasena: str
