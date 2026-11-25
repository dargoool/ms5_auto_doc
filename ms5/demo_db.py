import json
import logging
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from app.db.database import SessionLocal
from app.db.models import DocumentState, ExtractedFields
from app.kafka.dispatcher import KafkaDispatcher
from app.schemas.kafka_messages import KafkaMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

BASE_DIR = Path(__file__).parent


def load_text(path: Path):

    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path: Path):

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):

    path.parent.mkdir(exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )
    


def main():

    dispatcher = KafkaDispatcher()

    doc_id = str(uuid4())


    logging.info(f"Document ID: {doc_id}")

    #
    # OCR
    #

    text = load_text(
        BASE_DIR / "input" / "snils.txt"
    )

    logging.info("✓ OCR text loaded")

    dispatcher.dispatch(
        "doc.ocr.done",
        KafkaMessage(
            doc_id=doc_id,
            trace_id="demo",
            service="ocr",
            payload={
                "text": text
            }
        )
    )

    logging.info("✓ OCR message processed")

    #
    # BERT
    #

    bert = load_json(
        BASE_DIR / "input" / "bert.json"
    )

    logging.info(
        f"✓ {bert['doc_type']} "
        f"({bert['confidence']:.2f})"
    )

    dispatcher.dispatch(
        "doc.bert.done",
        KafkaMessage(
            doc_id=doc_id,
            trace_id="demo",
            service="bert",
            payload=bert
        )
    )

    #
    # YOLO

    yolo = load_json(
        BASE_DIR / "input" / "yolo.json"
    )

    logging.info(
        f"✓ {yolo['doc_type']} "
        f"({yolo['confidence']:.2f})"
    )

    result = dispatcher.dispatch(
        "doc.yolo.done",
        KafkaMessage(
            doc_id=doc_id,
            trace_id="demo",
            service="yolo",
            payload=yolo
        )
    )

    #
    # JSON
    #

    if result:

        save_json(
            BASE_DIR / "output" / "classification.json",
            asdict(result["classification"])
        )

        save_json(
            BASE_DIR / "output" / "extracted.json",
            result["fields"]
        )

        logging.info("✓ JSON saved")

        logging.info("\nExtracted fields:\n")

        for key, value in result["fields"].items():

            logging.info(
                f"{key:20} -> {value['value']}"
            )

    #
    # PostgreSQL
    #


    db = SessionLocal()

    try:

        state = (
            db.query(DocumentState)
            .filter(
                DocumentState.doc_id == doc_id
            )
            .first()
        )

        extracted = (
            db.query(ExtractedFields)
            .filter(
                ExtractedFields.doc_id == doc_id
            )
            .first()
        )

        logging.info("\ndocument_state\n")

        logging.info(f"doc_id      : {state.doc_id}")
        logging.info(f"ocr_done    : {state.ocr_done}")
        logging.info(f"bert_done   : {state.bert_done}")
        logging.info(f"yolo_done   : {state.yolo_done}")
        logging.info(f"doc_type    : {state.doc_type}")

        logging.info("\nextracted_fields\n")

        logging.info(f"doc_id      : {extracted.doc_id}")
        logging.info(f"doc_type    : {extracted.doc_type}")
        logging.info(
            f"confidence  : "
            f"{extracted.classification_confidence}"
        )

        logging.info("\nJSON:\n")

        logging.info(
            json.dumps(
                extracted.fields,
                ensure_ascii=False,
                indent=4
            )
        )

    finally:

        db.close()


    logging.info("✓ Pipeline completed successfully")


if __name__ == "__main__":

    main()