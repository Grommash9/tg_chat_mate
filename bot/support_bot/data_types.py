from dataclasses import dataclass
from typing import Optional

from dataclasses_jsonschema import JsonSchemaMixin


class BaseType(JsonSchemaMixin):
    pass


@dataclass(kw_only=True)
class Manager(BaseType):
    hashed_password: str
    full_name: str
    root: Optional[bool]
    activated: Optional[bool]
    username: str
