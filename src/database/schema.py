from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ImageRecord(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    image_type = Column(String(50), nullable=False) # 'original', 'generated'
    defect_type = Column(String(50), nullable=True) # 'normal', 'nut_error', 'crack', etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata for generated images
    parent_image_id = Column(Integer, nullable=True) # ID of source image if applicable
    generation_model_version = Column(String(50), nullable=True)

class LabelRecord(Base):
    __tablename__ = 'labels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, nullable=False)
    class_id = Column(Integer, nullable=False)
    x_center = Column(Float, nullable=False)
    y_center = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
