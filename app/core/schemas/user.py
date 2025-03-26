from pydantic import BaseModel, Field


class UserGetSchema(BaseModel):
    page: int = Field(..., gt=0, le=100, strict=True)
    page_size: int = Field(..., ge=0, strict=True)


class UserSignUpSchema(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    password: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    role: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)


class UserSignInSchema(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
    password: str = Field(..., min_length=1, max_length=255, strip_whitespace=True)
