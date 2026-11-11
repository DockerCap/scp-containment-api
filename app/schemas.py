from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models import Classification

from datetime import datetime


class ObjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scp_id: int = Field(strict=True, gt=0)
    name: str = Field(min_length=1, max_length=30)
    description: str | None = Field(max_length=255, default=None)
    classification: Classification

    @field_validator("name")
    @classmethod
    def reject_blank_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be blank")
        return value


class ObjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def reject_null_name(self):
        for field in ("scp_id", "name", "classification"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self

    scp_id: int | None = Field(strict=True, gt=0, default=None)
    name: str | None = Field(min_length=1, max_length=30, default=None)
    description: str | None = Field(max_length=255, default=None)
    classification: Classification | None = None

    @field_validator("name")
    @classmethod
    def reject_blank_name(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be blank")
        return value


class ObjectGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scp_id: str
    name: str
    description: str | None
    classification: Classification
    created_at: datetime
    updated_at: datetime
