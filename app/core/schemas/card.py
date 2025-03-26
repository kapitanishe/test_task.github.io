from pydantic import BaseModel, Field


class CardGetSchema(BaseModel):
    page: int = Field(..., gt=0, le=100, strict=True)
    page_size: int = Field(..., ge=0, strict=True)


class CardCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    board: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    description: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    estimation: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)


class CardDeleteSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)


class CardUpdateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    board: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)


class CardColumnGetSchema(BaseModel):
    board: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    column: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    assignee: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
