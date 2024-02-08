from pydantic import BaseModel


class LanguageBase(BaseModel):
    code: str


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageCreate):
    pass


class Language(LanguageCreate):
    id: int

    class Config:
        orm_mode = True
