from dataclasses import dataclass


@dataclass
class CoreCardCreateResponse:
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
class CoreCardDeleteResponse:
    title: str


@dataclass
class CoreCardUpdateResponse:
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
class CoreCardColumnResponse:
    board: str
    column: str
    assignee: str
    count: int
    estimation: str
    cards: list
