"""accounts.py

Class for Accounts"""
from typing import Any

from pydantic import BaseModel, Field

class Account(BaseModel):
    """A Pydantic model for Atomic Asset Accounts"""
    __root__: str = Field(..., description="The WAX address of the account")

    def __init__(self,data:Any):
        super().__init__(**data)
        self.address = self.__root__

    def __str__(self):
        return self.address

    def __eq__(self,other: Any):
        if type(other) == Account:
            return self.address == other.address
        else:
            return self.address == other
