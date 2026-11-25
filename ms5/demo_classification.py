import json
import logging
from dataclasses import asdict
from pathlib import Path

from app.models.classification import ClassificationResult
from app.services.classification_service import ClassificationService
from app.services.extraction_service import ExtractionService


BASE_DIR = Path(__file__).parent


def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def main():

    # ---------- Загружаем OCR текст ----------

    text = load_text(BASE_DIR / "input" / "passport.txt")
    logging.info("✓ OCR текст загружен")

    # ---------- Загружаем результат BERT ----------

    bert_json = load_json(BASE_DIR / "input" / "bert.json")

    bert_result = ClassificationResult(
        model="bert",
        doc_type=bert_json["doc_type"],
        confidence=bert_json["confidence"]
    )

    logging.info(
        f"✓ BERT: {bert_result.doc_type} "
        f"(confidence={bert_result.confidence})"
    )

    # ---------- Загружаем результат YOLO ----------

    yolo_json = load_json(BASE_DIR / "input" / "yolo.json")

    yolo_result = ClassificationResult(
        model="yolo",
        doc_type=yolo_json["doc_type"],
        confidence=yolo_json["confidence"]
    )

    logging.info(
        f"✓ YOLO: {yolo_result.doc_type} "
        f"(confidence={yolo_result.confidence})"
    )

    # ---------- Определяем итоговый тип документа ----------

    classifier = ClassificationService()

    final_result = classifier.resolve_document_type(
        bert_result,
        yolo_result
    )

    logging.info("\n✓ Итоговый тип документа:", final_result.doc_type)

    # ---------- Сохраняем результат классификации ----------

    classification_json = {
        "bert": asdict(bert_result),
        "yolo": asdict(yolo_result),
        "final": asdict(final_result)
    }

    save_json(
        BASE_DIR / "output" / "classification.json",
        classification_json
    )

    # ---------- Извлекаем поля ----------

    extractor = ExtractionService()

    extracted = extractor.extract(
        text,
        final_result.doc_type
    )

    save_json(
        BASE_DIR / "output" / "extracted.json",
        extracted
    )

    logging.info("✓ Поля успешно извлечены")

    logging.info("\nРезультаты сохранены:")

    logging.info(BASE_DIR / "output" / "classification.json")
    logging.info(BASE_DIR / "output" / "extracted.json")


if __name__ == "__main__":
    main()