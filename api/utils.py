"""JSON serialization helpers for API responses."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any


def to_camel_case(snake: str) -> str:
    parts = snake.split("_")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def serialize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return serialize_row(value)
    if isinstance(value, list):
        return [serialize_value(v) for v in value]
    return value


def serialize_row(row: dict, camel_case: bool = True) -> dict:
    result = {}
    for key, value in row.items():
        out_key = to_camel_case(key) if camel_case else key
        result[out_key] = serialize_value(value)
    return result


def serialize_rows(rows: list, camel_case: bool = True) -> list:
    return [serialize_row(r, camel_case) for r in rows]
