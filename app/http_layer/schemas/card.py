from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

post_card_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "board": {"type": "string", "minLength": 1},
        "description": {"type": "string", "minLength": 1},
        "estimation": {"type": "string", "minLength": 2},
    },
    "required": ["title", "board", "description", "estimation"],
    "additionalProperties": False,
}

del_card_schema = {
    "type": "object",
    "properties": {"title": {"type": "string", "minLength": 1}},
    "required": ["title"],
    "additionalProperties": False,
}

put_card_schema = {
    "type": "object",
    "properties": {"title": {"type": "string", "minLength": 1}, "board": {"type": "string", "minLength": 1}},
    "required": ["title", "board"],
    "additionalProperties": False,
}

get_card_estimation_schema = {
    "type": "object",
    "properties": {
        "board": {"type": "string", "minLength": 1},
        "column": {"type": "string", "minLength": 1},
        "assignee": {"type": "string", "minLength": 1},
    },
    "required": ["board", "column", "assignee"],
    "additionalProperties": False,
}


class CardPost(Inputs):
    json = [JsonSchema(schema=post_card_schema)]


class CardDel(Inputs):
    json = [JsonSchema(schema=del_card_schema)]


class CardPut(Inputs):
    json = [JsonSchema(schema=put_card_schema)]


class CardEstimation(Inputs):
    json = [JsonSchema(schema=get_card_estimation_schema)]
