from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base


class ImageStatus(str, Enum):
    INIT = 'init'
    UPLOADED = 'uploaded'
    PROCESSING = 'processing'
    DONE = 'done'
    ERROR = 'error'


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    images = relationship("Image", back_populates="project")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(Enum(ImageStatus), default=ImageStatus.INIT)
    project = relationship("Project", back_populates="images")
    original_url = Column(String, nullable=True)
    thumb_url = Column(String, nullable=True)
    big_thumb_url = Column(String, nullable=True)
    big_1920_url = Column(String, nullable=True)
    d2500_url = Column(String, nullable=True)
