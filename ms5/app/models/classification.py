from dataclasses import dataclass


@dataclass
class ClassificationResult:
    """
    Результат классификации документа одной моделью.
    """

    model: str          # bert или yolo
    doc_type: str       # PASSPORT, SNILS ...
    confidence: float   # вероятность