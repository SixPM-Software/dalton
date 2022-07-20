"""templates.py

Class for Atomic NFT Templates"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from .collections import Collection
from .. wax import Account

class Template(BaseModel):
    """A Pydantic model for Atomic Templates"""
    contract: str = Field(default="atomicassets", description="The smart contract of the NFT standard. Should always be `atomicassets`")
    template_id: int = Field(..., description="The template ID of the template", gt=0)
    is_transferable: bool = Field(..., description="Whether the asset is transferable")
    is_burnable: bool = Field(..., description="Whether the asset is burnable")
    collection: Optional[Collection] = Field(None, description="The collection the template belongs to")
    nft_schema: Optional[dict[str,Any]] = Field(None, description="The schema the template belongs to", alias="schema")
    issued_supply: int = Field(0, description="Number minted")
    max_supply: int = Field(0, description="Maximum supply, 0 = no limit")
    immutable_data: dict[str,Any] = Field({}, description="The template's immutable data")
    created_at_block: int = Field(default=None, description = "The block number this template was created in"),
    created_at_time: datetime = Field(default=None, description = "When the template was created"),
    name: str = Field(default=None, description = "The name of the NFT")

    class Config:
        allow_population_by_field_name = True

    def __init__(self,**data):
        super().__init__(**data)
        if (name := self.immutable_data.get("name")) and not self.name:
            self.name = name