from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import EsquemaBase


class CentroTreinamento(EsquemaBase):
    nome: Annotated[str, Field(description='Nome do centro de treinamentos', example='CT Well', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do CT', example='Rua e quadra', max_length=100)]
    proprietario: Annotated[str, Field(description='Proprietário do CT', example='Fulano', max_length=50)]