# Importamos o nosso modelo base da pasta contrib, onde já está tudo predefinido.
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Float, Integer, String, DateTime,ForeignKey
from workout_api.contrib.schemas import EsquemaBase

class AtletaModelo(EsquemaBase):
    # Nome da tabela que será usado pelo banco de dados
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    nome: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    cpf: Mapped[str] = mapped_column(String(11),nullable=False)
    idade: Mapped[int] = mapped_column(Integer,nullable=False)
    peso: Mapped[float] = mapped_column(Float,nullable=False)
    altura: Mapped[float] = mapped_column(Float,nullable=False)
    sexo: Mapped[str] = mapped_column(String(1),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped['CategoriaModelo'] = relationship(back_populates='atleta')
    centro_treinamento: Mapped['CTModelo'] = relationship(back_populates='atleta')
    categoria_id = Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    centro_treinamento: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))