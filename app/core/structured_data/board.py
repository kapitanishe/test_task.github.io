from dataclasses import dataclass


@dataclass
class CoreBoardCreateResponse:
    board_name: str
    created_at: str
    last_updated_at: str
    status_id: int
    user_id: int


@dataclass
class CoreBoardDeleteResponse:
    title: str
