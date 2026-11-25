from app.models.classification import ClassificationResult


class ClassificationService:

    SUPPORTED_TYPES = {
        "PASSPORT",
        "SNILS"
    }

    def resolve_document_type(
        self,
        bert_result,
        yolo_result
    ):

        # Если одна модель вернула неизвестный тип,
        # используем вторую.

        if bert_result.doc_type not in self.SUPPORTED_TYPES:
            return yolo_result

        if yolo_result.doc_type not in self.SUPPORTED_TYPES:
            return bert_result

        # Если обе согласны

        if bert_result.doc_type == yolo_result.doc_type:
            return bert_result

        # Если мнения расходятся,
        # выбираем модель с большей уверенностью.

        if bert_result.confidence >= yolo_result.confidence:
            return bert_result

        return yolo_result