from pydantic import BaseModel, ConfigDict, Field

from app.models import Classification

class ObjectCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    scp_id:int = Field(strict=True, gt=0)
    name:str = Field(min_length=1, max_length=30)
    description:str | None = Field(max_length=255, default=None) 
    classification: Classification

class ObjectUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    scp_id:int|None = Field(strict=True, gt=0, default=None)
    name:str|None = Field(min_length=1, max_length=255, default=None)
    description:str | None = Field(max_length=255, default=None) 
    classification: Classification
