from typing import Any, _TypedDictMeta


type JsonLike = dict[str, Any | JsonLike]
type Schema = dict[str, type | Schema]
type TypedDict = _TypedDictMeta


def get_schema(d: TypedDict) -> Schema:
    schema: Schema = {}
    for k, v in d.__annotations__.items():
        schema[k] = get_schema(v) if isinstance(v, _TypedDictMeta) else v
    return schema


class BadSchemaError(ValueError): ...


def validate_schema(
        candidate: JsonLike,
        schema: Schema,
        path: list[str] | None = None,
        *,
        allow_missing_keys: bool | None = None,
):
    if not allow_missing_keys and (missing := set(schema).difference(candidate)):
        raise BadSchemaError(f"Missing keys: [{", ".join(missing)}].")
    if unknown := set(candidate).difference(schema):
        raise BadSchemaError(f"Unknown keys: [{", ".join(unknown)}]")

    for k, v in candidate.items():
        path_ext = (path or []) + [k]
        k_ext = ".".join(path_ext)
        expected = dict if isinstance(schema[k], dict) else schema[k]

        if not isinstance(v, expected):
            raise BadSchemaError(
                f"Expected key {k_ext!r} to be of type {expected.__name__!r},"
                f" not {type(v).__name__!r}."
            )
        if isinstance(v, dict):
            validate_schema(v, schema[k], path_ext)