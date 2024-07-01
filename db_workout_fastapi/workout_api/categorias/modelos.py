from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String
from workout_api.contrib.schemas import EsquemaBase

class CategoriaModelo(EsquemaBase):
    # Nome da tabela que será usado pelo banco de dados
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    nome: Mapped[str] = mapped_column(String(100),unique=True, nullable=False)
    atleta: Mapped['AtletaModelo'] = relationship(back_populates='categoria')