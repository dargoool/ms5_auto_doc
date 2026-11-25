import json
import logging
from pathlib import Path

from app.services.extraction_service import ExtractionService


# Папка, в которой находится demo.py
BASE_DIR = Path(__file__).resolve().parent


def process_document(input_file: str, output_file: str, doc_type: str):
    """
    Загружает текст документа из файла,
    извлекает поля и сохраняет результат в JSON.
    """

    input_path = BASE_DIR / input_file
    output_path = BASE_DIR / output_file

    # Проверяем существование входного файла
    if not input_path.exists():
        logging.info(f"Ошибка: файл {input_path} не найден.")
        return

    # Читаем текст документа
    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Создаем сервис извлечения
    service = ExtractionService()

    # Извлекаем данные
    result = service.extract(text, doc_type)

    # Создаем папку output при необходимости
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем JSON
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    logging.info(f"окумент '{input_path.name}' успешно обработан.")
    logging.info(f"Результат сохранен в '{output_path}'.")


def main():
    logging.info("=" * 50)
    logging.info("MS5 Field Extraction Demo")
    logging.info("=" * 50)

    process_document(
        input_file="input/passport.txt",
        output_file="output/passport.json",
        doc_type="PASSPORT"
    )


    process_document(
        input_file="input/snils.txt",
        output_file="output/snils.json",
        doc_type="SNILS"
    )


if __name__ == "__main__":
    main()