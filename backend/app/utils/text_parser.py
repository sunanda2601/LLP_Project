import re


class TextParser:

    @staticmethod
    def extract_word(message: str):

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            message
        )

        if not words:

            return ""

        return words[-1]