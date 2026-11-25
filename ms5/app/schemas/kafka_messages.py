from pydantic import BaseModel
from typing import Optional


class KafkaMessage(BaseModel):

    doc_id: str

    trace_id: str

    service: str

    payload: dict