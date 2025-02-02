import json
from typing import Any, Dict

from docs_src.tutorial.path_params.tutorial_003 import app
from xpresso.testclient import TestClient

client = TestClient(app)

openapi_schema: Dict[str, Any] = {
    "openapi": "3.0.3",
    "info": {"title": "API", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response",
                                    "type": "object",
                                    "additionalProperties": {"type": "integer"},
                                }
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "parameters": [
                    {
                        "required": True,
                        "style": "simple",
                        "explode": False,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMinimum": 0.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            }
        }
    },
    "components": {
        "schemas": {
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"oneOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.content
    assert response.json() == openapi_schema


def test_get_items_valid():
    response = client.get("/items/1")
    assert response.status_code == 200, response.content
    assert response.json() == json.load(
        open("docs_src/tutorial/path_params/tutorial_003_response_1.json")
    )


def test_get_items_invalid():
    response = client.get("/items/-1")
    assert response.status_code == 422, response.content
    assert response.json() == json.load(
        open("docs_src/tutorial/path_params/tutorial_003_response_2.json")
    )
