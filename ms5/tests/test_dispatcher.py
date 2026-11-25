import pytest
from unittest.mock import MagicMock

from app.kafka.dispatcher import KafkaDispatcher


@pytest.fixture
def dispatcher():

    dispatcher = KafkaDispatcher()

    dispatcher.aggregator = MagicMock()

    return dispatcher

def test_dispatch_ocr(dispatcher):

    dispatcher.dispatch(
        "doc.ocr.done",
        {"doc_id": "1"}
    )

    dispatcher.aggregator.process_ocr.assert_called_once()

def test_dispatch_bert(dispatcher):

    dispatcher.dispatch(
        "doc.bert.done",
        {"doc_id": "1"}
    )

    dispatcher.aggregator.process_bert.assert_called_once()

def test_dispatch_yolo(dispatcher):

    dispatcher.dispatch(
        "doc.yolo.done",
        {"doc_id": "1"}
    )

    dispatcher.aggregator.process_yolo.assert_called_once()

def test_unknown_topic(dispatcher):

    with pytest.raises(ValueError):

        dispatcher.dispatch(
            "unknown.topic",
            {}
        )