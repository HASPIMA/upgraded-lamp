from pydantic import BaseModel


class SignupUser(BaseModel):
    nombre: str
    identificacion: str
    correo_electronico: str
    contrasena: str
