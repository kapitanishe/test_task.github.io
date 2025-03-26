from dataclasses import dataclass


@dataclass
class CoreUserSignUpResponse:
    name: str
    role: str


@dataclass
class CoreUserSignInResponse:
    id_: int
    name: str
    token: str
    role: str


@dataclass
class TokenCheckResponse:
    id: int
    name: str
    role: str
