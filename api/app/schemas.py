from pydantic import BaseModel
from typing import List, Optional
from .models import ImageStatus

class ImageBase(BaseModel):
    filename: str
    project_id: int

class ImageCreate(ImageBase):
    pass

class ImageInDBBase(ImageBase):
    id: int
    status: ImageStatus
    original_url: Optional[str] = None
    thumb_url: Optional[str] = None
    big_thumb_url: Optional[str] = None
    big_1920_url: Optional[str] = None
    d2500_url: Optional[str] = None

    class Config:
        orm_mode = True

class Image(ImageInDBBase):
    pass

class ProjectBase(BaseModel):
    id: int

class Project(ProjectBase):
    images: List[Image] = []

    class Config:
        orm_mode = True
