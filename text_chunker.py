import uuid
import re
from typing import List, Dict
import tiktoken


class TextChunker:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.encoder = tiktoken.encoding_for_model(model)

    # -------------------------------------------------
    # Utility Functions
    # -------------------------------------------------
    def calculate_optimal_chunk_size(self, text: str) -> int:
        """Determine chunk size based on document length"""
        token_count = len(self.encoder.encode(text))

        if token_count < 5_000:
            return 500
        elif token_count < 50_000:
            return 1_000
        else:
            return 1_500

    def merge_small_chunks(self, chunks: List[Dict], min_tokens: int = 200) -> List[Dict]:
        """Merge chunks that are too small to preserve context"""
        merged = []
        buffer = None

        for chunk in chunks:
            if chunk["token_count"] < min_tokens:
                if buffer:
                    buffer["text"] += " " + chunk["text"]
                    buffer["token_count"] += chunk["token_count"]
                    buffer["word_count"] += chunk["word_count"]
                    buffer["char_count"] += chunk["char_count"]
                else:
                    buffer = chunk
            else:
                if buffer:
                    merged.append(buffer)
                    buffer = None
                merged.append(chunk)

        if buffer:
            merged.append(buffer)

        return merged

    # -------------------------------------------------
    # Chunking Strategies
    # -------------------------------------------------
    def chunk_by_tokens(
        self,
        text: str,
        source_file: str,
        page_number: int,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[Dict]:
        """Fixed-size token chunking with overlap"""

        tokens = self.encoder.encode(text)
        chunks = []
        start = 0
        index = 0

        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoder.decode(chunk_tokens)

            chunks.append(self._build_chunk(
                chunk_text,
                index,
                source_file,
                page_number
            ))

            start += chunk_size - overlap
            index += 1

        return chunks

    def chunk_by_sentences(
        self,
        text: str,
        source_file: str,
        page_number: int,
        max_tokens: int = 1000
    ) -> List[Dict]:
        """Sentence-aware chunking that avoids mid-sentence splits"""

        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_text = ""
        index = 0

        for sentence in sentences:
            temp_text = f"{current_text} {sentence}".strip()
            token_count = len(self.encoder.encode(temp_text))

            if token_count > max_tokens and current_text:
                chunks.append(self._build_chunk(
                    current_text,
                    index,
                    source_file,
                    page_number
                ))
                index += 1
                current_text = sentence
            else:
                current_text = temp_text

        if current_text:
            chunks.append(self._build_chunk(
                current_text,
                index,
                source_file,
                page_number
            ))

        return chunks

    # -------------------------------------------------
    # Master Chunking Function
    # -------------------------------------------------
    def create_chunks(
        self,
        cleaned_text: str,
        source_file: str,
        page_number: int,
        strategy: str = "tokens"
    ) -> List[Dict]:
        """Create chunks using the selected strategy"""

        if not cleaned_text.strip():
            return []

        chunk_size = self.calculate_optimal_chunk_size(cleaned_text)

        if strategy == "sentences":
            chunks = self.chunk_by_sentences(
                cleaned_text,
                source_file,
                page_number,
                max_tokens=chunk_size
            )
        else:
            chunks = self.chunk_by_tokens(
                cleaned_text,
                source_file,
                page_number,
                chunk_size=chunk_size
            )

        return self.merge_small_chunks(chunks)

    # -------------------------------------------------
    # Internal Helper
    # -------------------------------------------------
    def _build_chunk(self, text: str, index: int, source_file: str, page_number: int) -> Dict:
        tokens = self.encoder.encode(text)

        return {
            "chunk_id": str(uuid.uuid4()),
            "chunk_index": index,
            "text": text,
            "source_file": source_file,
            "page_number": page_number,
            "token_count": len(tokens),
            "word_count": len(text.split()),
            "char_count": len(text)
        }