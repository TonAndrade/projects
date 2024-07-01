# Arquivo para validação de dados. Use o BAseModel para ajudar nesse processo.
from pydantic import BaseModel, Field, PositiveFloat
from typing import Annotated
from numeros import gerarCPF

class Atleta(BaseModel):
    # sendo str o tipo de dado e Field() o retorno desse dado.
    # examples é usado como placeholder para o campo em questão, como um exemplo mesmo.
    # O max_length é usado para limitar o número de caracteres do campo.
    # Use o PositiveFloat para que o campo aceite apenas valores positivos.
    nome: Annotated[str, Field(description='Nome do atleta', example='Fulano', max_length=100)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=18, max_length=99)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=80.1, max_length=200)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75, max_length=3)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]