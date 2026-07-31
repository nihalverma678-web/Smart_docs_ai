import re
import unicodedata


class TextCleaner:
    def __init__(self):
        pass

    def remove_extra_whitespace(self, text: str) -> str:
        """Normalize spaces and line breaks"""
        if not text or not text.strip():
            return ""

        # Replace multiple spaces with single space
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize line breaks
        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()

    def remove_special_characters(self, text: str) -> str:
        """Remove unwanted symbols but keep punctuation"""
        if not text or not text.strip():
            return ""

        # Keep letters, numbers, punctuation
        text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'\"()\-]", "", text)
        return text

    def remove_headers_footers(self, text: str) -> str:
        """Remove page numbers and repetitive headers/footers"""
        if not text or not text.strip():
            return ""

        lines = text.split("\n")

        cleaned_lines = []
        for line in lines:
            # Remove page numbers (e.g., Page 1, 2, 3)
            if re.match(r"^\s*(page\s*)?\d+\s*$", line.lower()):
                continue

            # Remove short repetitive headers
            if len(line.strip()) < 3:
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def normalize_text(self, text: str, lowercase: bool = True) -> str:
        """Handle case conversion and unicode normalization"""
        if not text or not text.strip():
            return ""

        # Unicode normalization
        text = unicodedata.normalize("NFKC", text)

        if lowercase:
            text = text.lower()

        return text

    def clean_text(self, text: str) -> str:
        """Apply all cleaning steps in sequence"""
        if not text or not text.strip():
            return ""

        text = self.normalize_text(text)
        text = self.remove_headers_footers(text)
        text = self.remove_special_characters(text)
        text = self.remove_extra_whitespace(text)

        return text
    from backend.text_cleaner import TextCleaner

raw_text = """
    PAGE 1

    This   is     a    SAMPLE   text!!! ###@@@

    It contains    excessive     spaces,
    weird symbols ###$$$%%% and
    inconsistent   formatting.

    Page 2
    café  naïve   résumé

"""

cleaner = TextCleaner()
cleaned_text = cleaner.clean_text(raw_text)

print("=" * 60)
print("BEFORE CLEANING:")
print("=" * 60)
print(raw_text)

print("\n" + "=" * 60)
print("AFTER CLEANING:")
print("=" * 60)
print(cleaned_text)
python tests/test_text_cleaner.py

    