from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String
from workout_api.contrib.schemas import EsquemaBase

class CTModelo(EsquemaBase):
    # Nome da tabela que será usado pelo banco de dados
    __tablename__ = 'ct'

    pk_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    nome: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    atleta: Mapped['AtletaModelo'] = relationship(back_populates='ct')
    proprietario: Mapped[str] = mapped_column(String(50),nullable=False)
    endereco: Mapped[str] = mapped_column(String(50),nullable=False)