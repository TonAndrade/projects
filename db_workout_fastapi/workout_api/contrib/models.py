# modelos genéricos. É literalmente um modelo base.
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4

# Use o mapped para mapeamento em sqlalchemy
# Use o mapped_column para mapear colunas
# Use o postgresql UUID para importar um modelo do postgres

class ModeloBase(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, nullable=False)