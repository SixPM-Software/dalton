"""assets.py

Class for Atomic NFT Assets"""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Union
from pydantic import BaseModel, Field
from .collections import Collection
from .templates import Template
from .. wax import Account

class Asset(BaseModel):
    """A Pydantic model for Atomic Asset NFTs"""
    contract: str = Field(default="atomicassets", description="The smart contract of the NFT standard. Should always be `atomicassets`")
    asset_id: int = Field(..., description="The asset ID of the NFT", gt=0)
    is_transferable: bool = Field(..., description="Whether the asset is transferable")
    is_burnable: bool = Field(..., description="Whether the asset is burnable")
    collection: Collection = Field(..., description="The collection the NFT belongs to")
    nft_schema: dict[str,Any] = Field(..., description="The schema the NFT belongs to", alias="schema")
    template: Union[Template,None] = Field(None, description="The template the NFT belongs to")
    mutable_data: dict[str,Any] = Field({}, description="The NFT's mutable data")
    immutable_data: dict[str,Any] = Field({}, description="The NFT's immutable data")
    template_mint: int = Field(..., description="The NFT's mint number. 0 indicates no template or mint number still pending.")
    backed_tokens: List[Any] = Field([], description="The NFT's mutable data")
    burned_by_account: Union[Account, None] = Field(default=None, description = "Which account burned this NFT"),
    burned_at_block: Union[int, None] = Field(default=None, description = "The block number this NFT was burned in"),
    burned_at_time: Union[datetime, None] = Field(default=None, description = "When the NFT was burned"),
    updated_at_block: Union[int, None] = Field(default=None, description = "The block number this NFT was lasted updated in"),
    updated_at_time: Union[datetime, None] = Field(default=None, description = "When the NFT was last updated"),
    transferred_at_block: Union[int, None] = Field(default=None, description = "The block number this NFT was lasted transferred in"),
    transferred_at_time: Union[datetime, None] = Field(default=None, description = "When the NFT was last transferred"),
    minted_at_block: int = Field(default=None, description = "The block number this NFT was minted in"),
    minted_at_time: datetime = Field(default=None, description = "When the NFT was minted"),
    data: dict[str,Any] = Field({}, description="The NFT's presented data. Use this in most cases")
    owner: Union[Account,str] = Field(default=None, description = "The owner of the NFT") #XXX Replace with Account class when created
    name: str = Field(default=None, description = "The name of the NFT")

    burned: bool = Field(default=False, description="Whether or not the asset has been burned")

    class Config:
        allow_population_by_field_name = True
    
    def __init__(self,**data):
        super().__init__(**data)
        if self.burned_at_block:
            self.burned = True

        if self.template:
            self.template.collection = self.collection
            self.template.nft_schema = self.nft_schema
