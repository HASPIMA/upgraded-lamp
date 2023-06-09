from pydantic import (
    BaseModel,
    EmailStr,
    constr,
)


class SignupUser(BaseModel):
    nombre: constr(strip_whitespace=True, min_length=1)  # type: ignore
    identificacion: constr(strip_whitespace=True, min_length=1)  # type: ignore
    correo_electronico: EmailStr
    contrasena: constr(min_length=8)  # type: ignore
