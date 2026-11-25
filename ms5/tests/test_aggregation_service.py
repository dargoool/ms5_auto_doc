from app.services.aggregation_service import AggregationService


def test_process_ocr():

    service = AggregationService()

    service.process_ocr({"doc_id": "1"})


def test_process_bert():

    service = AggregationService()

    service.process_bert({"doc_id": "1"})


def test_process_yolo():

    service = AggregationService()

    service.process_yolo({"doc_id": "1"})