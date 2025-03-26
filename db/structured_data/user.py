from dataclasses import dataclass, field


@dataclass
class DBUserGetRequest:
    page_size: int
    offset: int


@dataclass
class DBUserRow:
    user_id: int
    user_name: str
    admin: bool


@dataclass
class DBUserGetResponse:
    users: list[DBUserRow] = field(default_factory=list)


@dataclass
class DBUserSignUpRequest:
    name: str
    password: str
    role: bool


@dataclass
class DBUserSignUpResponse:
    name: str
    role: bool


@dataclass
class DBUserSignInRequest:
    user_name: str | None = field(default=None)


@dataclass
class DBUserSignInResponse:
    id_: int
    name: str
    password: str
    role: bool
