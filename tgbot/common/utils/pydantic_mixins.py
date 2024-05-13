from abc import ABC

from pydantic import BaseModel


class TypesAllowedConfig(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True
