from pydantic import BaseModel


class Brand(BaseModel):
    """Brand Schema"""

    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
