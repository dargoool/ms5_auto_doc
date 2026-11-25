import pytest

from app.models.classification import ClassificationResult
from app.services.classification_service import ClassificationService


class TestClassificationService:

    @pytest.fixture
    def service(self):
        return ClassificationService()

    def test_choose_bert(self, service):

        bert = ClassificationResult(
            model="bert",
            doc_type="PASSPORT",
            confidence=0.95
        )

        yolo = ClassificationResult(
            model="yolo",
            doc_type="SNILS",
            confidence=0.80
        )

        result = service.resolve_document_type(
            bert,
            yolo
        )

        assert result.doc_type == "PASSPORT"
        assert result.model == "bert"

    def test_choose_yolo(self, service):

        bert = ClassificationResult(
            model="bert",
            doc_type="PASSPORT",
            confidence=0.70
        )

        yolo = ClassificationResult(
            model="yolo",
            doc_type="SNILS",
            confidence=0.98
        )

        result = service.resolve_document_type(
            bert,
            yolo
        )

        assert result.doc_type == "SNILS"
        assert result.model == "yolo"