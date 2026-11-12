from pydantic import BaseModel, ConfigDict, Field

class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = ""
    price: float = Field(gt=0)
    category: str = "General"
    available: bool = True

class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    available: bool | None = None

class MenuItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price: float
    category: str
    available: bool
