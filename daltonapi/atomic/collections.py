"""collections.py

Class for Atomic NFT Collections"""

from __future__ import annotations

from datetime import datetime
import json
from typing import Any, List, Union, Optional

from pydantic import BaseModel, Field, validator, Json 

from .. wax import Account 

class CollectionData(BaseModel):
    """Handler for collection data supplied in the "data" field of the collection call"""
    img: str = Field(default=None, description = "Collection image")
    url: str = Field(default=None, description = "Collection website")
    name: str = Field(default=None, description = "Collection name")
    images: Json = Field(default="{}", description = "Other collection images")
    socials: Json = Field(default="{}", description = "Collection social media handles")
    description: str = Field(default=None, description = "Collection description")
    creator_info: Json = Field(default="{}", description = "Collection creator information")

    def __init__(self,**data: Any):
        super().__init__(**data)
        if type(self.images) is str:
            self.images = json.loads(self.images)
        if type(self.socials) is str:
            self.socials = json.loads(self.socials)
        if type(self.creator_info) is str:
            self.creator_info = json.loads(self.creator_info)


class Collection(BaseModel):
    """A Pydantic model for Atomic Collections"""
    collection_name: str = Field(..., description="The official name of the collection")
    contract: str = Field(default="atomicassets", description="The smart contract of the NFT standard. Should always be `atomicassets`")
    name: str = Field(default=None, description = "The display name of the collection")
    img: str = Field(default=None, description = "The collection image")
    author: Union[Account,str] = Field(default=None, description = "The account that created the author") #XXX Replace with Account class when created
    allow_notify: bool = Field(..., description = "Whether contract notifications are allowed")
    authorized_accounts: List[Union[Account,str]] = Field(..., description = "Accounts authorized on the colllection")
    notify_accounts: List[Union[Account,str]] = Field(..., description = "Accounts authorized on the colllection")
    market_fee: float = Field(..., description = "The collection market fee as a decimal (10% = 0.1)")
    data: CollectionData = Field(default=CollectionData(), description = "Whether contract notifications are allowed")
    created_at_time: datetime = Field(..., description = "When the collection was created")
    created_at_block: int = Field(..., description = "The block number the collection was created in")
