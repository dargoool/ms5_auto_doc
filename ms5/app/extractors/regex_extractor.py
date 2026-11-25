import re

from .patterns import PATTERNS


class RegexExtractor:

    def extract(self, text: str, doc_type: str) -> dict:

        result = {}

        document = PATTERNS.get(doc_type)

        if not document:
            return result

        regex_patterns = document.get("regex", {})

        for field, regex_list in regex_patterns.items():

            # Значение по умолчанию
            result[field] = {
                "value": None,
                "method": "regex"
            }

            for pattern in regex_list:

                match = re.search(pattern, text, re.IGNORECASE)

                if match:

                    value = match.group(1) if match.lastindex else match.group()

                    result[field] = {
                        "value": value.strip(),
                        "method": "regex"
                    }

                    break

        return result