from dataclasses import dataclass, field


@dataclass
class DBBoardGetRequest:
    page_size: int
    offset: int


@dataclass
class DBBoardRow:
    board_id: int
    board_name: str
    created_at: str
    last_updated_at: str
    status_id: int
    user_id: int


@dataclass
class DBBoardGetResponse:
    boards: list[DBBoardRow] = field(default_factory=list)


@dataclass
class DBBoardCreateRequest:
    board_name: str
    user_id: int


@dataclass
class DBBoardCreateResponse:
    board_name: str
    created_at: str
    last_updated_at: str
    status_id: int
    user_id: int


@dataclass
class DBBoardDeleteRequest:
    board_name: str


@dataclass
class DBBoardDeleteResponse:
    board_name: str
