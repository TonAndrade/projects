from pydantic import BaseModel


class EsquemaBase(BaseModel):
    class Config:
        extra = 'forbid'
        from_att = True