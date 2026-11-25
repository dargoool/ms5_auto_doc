import pytest

from app.extractors.regex_extractor import RegexExtractor


class TestRegexExtractor:

    @pytest.fixture
    def extractor(self):
        return RegexExtractor()

    def test_extract_passport_series_number(self, extractor):
        text = "Серия и номер паспорта: 4500 123456"

        result = extractor.extract(text, "PASSPORT")

        assert "series_number" in result
        assert result["series_number"]["value"] == "4500 123456"
        assert result["series_number"]["method"] == "regex"

    def test_extract_birth_date(self, extractor):
        text = "Дата рождения: 12.05.1990"

        result = extractor.extract(text, "PASSPORT")

        assert "birth_date" in result
        assert result["birth_date"]["value"] == "12.05.1990"

    def test_extract_department_code(self, extractor):
        text = "Код подразделения 770-001"

        result = extractor.extract(text, "PASSPORT")

        assert "department_code" in result
        assert result["department_code"]["value"] == "770-001"

    def test_extract_snils(self, extractor):
        text = "СНИЛС: 112-233-445 95"

        result = extractor.extract(text, "SNILS")

        assert "snils_number" in result
        assert result["snils_number"]["value"] == "112-233-445 95"

    def test_unknown_document_type(self, extractor):
        result = extractor.extract("Любой текст", "UNKNOWN")

        assert result == {}

    def test_empty_text(self, extractor):
        result = extractor.extract("", "PASSPORT")

        assert result["series_number"]["value"] is None
        assert result["birth_date"]["value"] is None
        assert result["issue_date"]["value"] is None
        assert result["department_code"]["value"] is None
        assert result["birth_place"]["value"] is None
        assert result["issued_by"]["value"] is None

    def test_no_matches(self, extractor):
        result = extractor.extract("Просто какой-то текст", "PASSPORT")

        assert result["series_number"]["value"] is None
        assert result["birth_date"]["value"] is None
        assert result["issue_date"]["value"] is None
        assert result["department_code"]["value"] is None
        assert result["birth_place"]["value"] is None
        assert result["issued_by"]["value"] is None