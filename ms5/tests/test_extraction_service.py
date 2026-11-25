import pytest

from app.services.extraction_service import ExtractionService


class TestExtractionService:

    @pytest.fixture
    def service(self):
        return ExtractionService()

    def test_extract_passport(self, service):
        text = """
        Иванов Иван Иванович
        4500 123456
        12.05.1990
        Код подразделения 770-001
        """

        result = service.extract(text, "PASSPORT")

        assert "fio" in result
        assert "series_number" in result
        assert "birth_date" in result
        assert "department_code" in result

    def test_extract_snils(self, service):
        text = """
        Петров Петр Петрович
        СНИЛС: 112-233-445 95
        """

        result = service.extract(text, "SNILS")

        assert "fio" in result
        assert "snils_number" in result

    def test_unknown_document_type(self, service):
        result = service.extract(
            "Любой текст",
            "UNKNOWN"
        )

        assert result == {}

    def test_empty_text(self, service):

        result = service.extract("", "PASSPORT")

        assert result["series_number"]["value"] is None
        assert result["birth_date"]["value"] is None
        assert result["issue_date"]["value"] is None
        assert result["department_code"]["value"] is None
        assert result["birth_place"]["value"] is None
        assert result["issued_by"]["value"] is None
        assert result["fio"]["value"] is None