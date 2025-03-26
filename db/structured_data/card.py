from dataclasses import dataclass, field


@dataclass
class DBCardGetRequest:
    page_size: int
    offset: int


@dataclass
class DBCardRow:
    card_id: int
    assignee: int
    board: int
    title: str
    estimation: str
    status: int
    description: str
    created_at: str
    last_updated_at: str


@dataclass
class DBCardGetResponse:
    cards: list[DBCardRow] = field(default_factory=list)


@dataclass
class DBCardCreateRequest:
    assignee: int
    title: str
    board: str
    description: str
    estimation: str


@dataclass
class DBCardCreateResponse:
    id_: int
    assignee: int
    board: int
    title: str
    estimation: str
    status: int
    description: str
    created_at: str
    last_updated_at: str


@dataclass
class DBCardDeleteRequest:
    title: str


@dataclass
class DBCardDeleteResponse:
    title: str


@dataclass
class DBCardUpdateRequest:
    title: str
    board: str


@dataclass
class DBCardUpdateResponse:
    id_: int
    assignee: int
    board: int
    title: str
    estimation: str
    status: int
    description: str
    created_at: str
    last_updated_at: str


@dataclass
class DBCardEstimationRequest:
    assignee: str
    status: str


@dataclass
class DBCardEstimationResponse:
    estimation: str


@dataclass
class DBCardColumnRequest:
    status: str
    board: str
    assignee: str


@dataclass
class DBCardColumnResponse:
    title: str
    board: str
    status: str
    description: str
    assignee: str
    estimation: str
    created_by: str
    created_at: str
    last_updated_at: str
    last_updated_by: str
