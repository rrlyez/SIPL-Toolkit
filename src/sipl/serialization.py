from dataclasses import fields, is_dataclass

from sipl.ast import Node


def to_data(value):
    if is_dataclass(value):
        result = {}

        if isinstance(value, Node):
            result["type"] = type(value).__name__

        for field in fields(value):
            result[field.name] = to_data(
                getattr(value, field.name)
            )

        return result

    if isinstance(value, (list, tuple)):
        return [to_data(item) for item in value]

    if isinstance(value, dict):
        return {
            key: to_data(item)
            for key, item in value.items()
        }

    return value