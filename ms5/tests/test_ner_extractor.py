import pytest

from app.extractors.ner_extractor import NERExtractor


class TestNERExtractor:

    @pytest.fixture
    def extractor(self):
        return NERExtractor()

    def test_extract_person_from_passport(self, extractor):
        text = "Иванов Иван Иванович"

        result = extractor.extract(text, "PASSPORT")

        assert "fio" in result
        assert result["fio"]["value"] == "Иванов Иван Иванович"
        assert result["fio"]["method"] == "ner"

    def test_extract_person_from_snils(self, extractor):
        text = "Петров Петр Петрович"

        result = extractor.extract(text, "SNILS")

        assert "fio" in result
        assert result["fio"]["value"] == "Петров Петр Петрович"

    def test_without_person(self, extractor):

        text = "Сегодня хорошая погода."

        result = extractor.extract(text, "PASSPORT")

        assert "fio" in result
        assert result["fio"]["value"] is None

    def test_unknown_document_type(self, extractor):
        text = "Иванов Иван Иванович"

        result = extractor.extract(text, "UNKNOWN")

        assert result == {}

    def test_empty_text(self, extractor):
        result = extractor.extract("", "PASSPORT")

        assert "fio" in result
        assert result["fio"]["value"] is None
        assert result["fio"]["method"] == "ner"

    def test_text_with_spaces(self, extractor):
        result = extractor.extract("      ", "PASSPORT")

        assert "fio" in result
        assert result["fio"]["value"] is None
        assert result["fio"]["method"] == "ner"