from pydantic import BaseModel, Field


class BoardGetSchema(BaseModel):
    page: int = Field(..., gt=0, le=100, strict=True)
    page_size: int = Field(..., ge=0, strict=True)


class BoardCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    user_id: int = Field(..., gt=0)


class BoardDeleteSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
