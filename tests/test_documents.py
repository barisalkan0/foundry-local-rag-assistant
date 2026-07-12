from pathlib import Path
import unittest

from src.documents import (
    chunk_documents,
    extract_title,
    strip_front_matter,
    tokenize_words,
    Document,
)


class DocumentTests(unittest.TestCase):
    def test_strip_front_matter_removes_metadata(self) -> None:
        text = "---\ntitle: Örnek\n---\n# Gerçek Başlık\nGövde"
        self.assertEqual(strip_front_matter(text).strip(), "# Gerçek Başlık\nGövde")

    def test_extract_title_uses_first_markdown_h1(self) -> None:
        self.assertEqual(extract_title("# Başlığım\nGövde", Path("fallback.md")), "Başlığım")

    def test_chunk_documents_uses_overlap(self) -> None:
        document = Document(
            path=Path("sample.md"),
            title="Sample",
            text=" ".join(str(index) for index in range(10)),
        )
        chunks = chunk_documents([document], max_words=6, overlap_words=2)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(tokenize_words(chunks[0].text), ["0", "1", "2", "3", "4", "5"])
        self.assertEqual(tokenize_words(chunks[1].text), ["4", "5", "6", "7", "8", "9"])


if __name__ == "__main__":
    unittest.main()
