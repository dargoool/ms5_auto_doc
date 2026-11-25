from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.sql import func

from app.db.database import Base


class DocumentState(Base):

    __tablename__ = "document_state"

    id = Column(Integer, primary_key=True)

    doc_id = Column(
        String,
        unique=True,
        nullable=False
    )

    ocr_done = Column(
        Boolean,
        default=False
    )

    bert_done = Column(
        Boolean,
        default=False
    )

    yolo_done = Column(
        Boolean,
        default=False
    )

    ocr_text = Column(
        String
    )

    bert_type = Column(
        String
    )

    bert_confidence = Column(
        Float
    )

    yolo_type = Column(
        String
    )

    yolo_confidence = Column(
        Float
    )

    doc_type = Column(
        String
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

class ExtractedFields(Base):

    __tablename__ = "extracted_fields"

    id = Column(Integer, primary_key=True)

    doc_id = Column(String)

    doc_type = Column(String)

    classification_confidence = Column(Float)

    fields = Column(JSON)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )