from backend.text_chunker import TextChunker

chunker = TextChunker()

# Simulated documents
short_text = "This is a short document. " * 100
medium_text = "This is a medium document sentence. " * 2000
long_text = "This is a long document sentence with more content. " * 10000

documents = [
    ("short.pdf", short_text, 1),
    ("medium.pdf", medium_text, 5),
    ("long.pdf", long_text, 42)
]

for name, text, page in documents:
    print("=" * 60)
    print(f"Processing {name}")

    chunks = chunker.create_chunks(
        cleaned_text=text,
        source_file=name,
        page_number=page,
        strategy="sentences"
    )

    print(f"Total chunks: {len(chunks)}")

    for c in chunks[:3]:
        print("\nChunk Index:", c["chunk_index"])
        print("Tokens:", c["token_count"])
        print("Words:", c["word_count"])
        print("Characters:", c["char_count"])
        print("Text Preview:", c["text"][:120])