import json
import logging
from dataclasses import asdict
from pathlib import Path

from app.kafka.dispatcher import KafkaDispatcher
from app.schemas.kafka_messages import KafkaMessage


BASE_DIR = Path(__file__).parent


def load_text(path):

    with open(path, encoding="utf-8") as f:

        return f.read()


def load_json(path):

    with open(path, encoding="utf-8") as f:

        return json.load(f)


def save_json(path, data):

    path.parent.mkdir(exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=4)


def main():

    logging.info("=" * 60)

    logging.info("MS5 Pipeline Demo")

    logging.info("=" * 60)

    dispatcher = KafkaDispatcher()

    text = load_text(BASE_DIR / "input" / "passport.txt")

    ocr_message = KafkaMessage(

        doc_id="1",

        trace_id="demo",

        service="ocr",

        payload={

            "text": text

        }

    )

    dispatcher.dispatch(

        "doc.ocr.done",

        ocr_message

    )

    bert = load_json(BASE_DIR / "input" / "bert.json")

    bert_message = KafkaMessage(

        doc_id="1",

        trace_id="demo",

        service="bert",

        payload=bert

    )

    dispatcher.dispatch(

        "doc.bert.done",

        bert_message

    )

    yolo = load_json(BASE_DIR / "input" / "yolo.json")

    yolo_message = KafkaMessage(

        doc_id="1",

        trace_id="demo",

        service="yolo",

        payload=yolo

    )

    result = dispatcher.dispatch(

        "doc.yolo.done",

        yolo_message

    )

    if result:

        save_json(

            BASE_DIR / "output" / "classification.json",

            asdict(result["classification"])

        )

        save_json(

            BASE_DIR / "output" / "extracted.json",

            result["fields"]

        )

        logging.info("\nРезультат сохранен.")


if __name__ == "__main__":

    main()