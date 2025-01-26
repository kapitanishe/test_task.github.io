from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

post_board_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "user_id": {"type": "integer", "minimum": 1},
    },
    "required": ["title", "user_id"],
    "additionalProperties": False,
}

del_board_schema = {
    "type": "object",
    "properties": {"title": {"type": "string", "minLength": 1}},
    "required": ["title"],
    "additionalProperties": False,
}


class BoardPost(Inputs):
    json = [JsonSchema(schema=post_board_schema)]


class BoardDel(Inputs):
    json = [JsonSchema(schema=del_board_schema)]
