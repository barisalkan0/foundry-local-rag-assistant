import unittest

from src.retrieval import cosine_similarity, keyword_overlap


class RetrievalTests(unittest.TestCase):
    def test_cosine_similarity_identical_vectors(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1.0, 2.0], [1.0, 2.0]), 1.0)

    def test_cosine_similarity_orthogonal_vectors(self) -> None:
        self.assertEqual(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)

    def test_keyword_overlap_ignores_common_words(self) -> None:
        score = keyword_overlap(
            "Dokümanları değiştirdikten sonra ne yapmalıyım?",
            "Dokümanları değiştirdikten sonra ingestion scriptini tekrar çalıştır.",
        )
        self.assertGreater(score, 0.5)

    def test_keyword_overlap_handles_turkish_characters(self) -> None:
        score = keyword_overlap("Çevrimdışı yapay zeka", "Çevrimdışı yapay zeka yerelde çalışır.")
        self.assertGreater(score, 0.8)


if __name__ == "__main__":
    unittest.main()
