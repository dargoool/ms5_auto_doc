import pytest
from pydantic import ValidationError

from app.schemas.kafka_messages import KafkaMessage

from app.schemas.kafka_messages import KafkaMessage


def test_valid_message():

    msg = KafkaMessage(

        doc_id="1",

        trace_id="abc",

        service="ms2",

        payload={}
    )

    assert msg.doc_id == "1"
    
def test_invalid_message():

    with pytest.raises(ValidationError):

        KafkaMessage()