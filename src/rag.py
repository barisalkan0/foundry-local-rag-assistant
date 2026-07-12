from __future__ import annotations

from src.config import (
    CHAT_MAX_TOKENS,
    CHAT_MODEL_ALIAS,
    CHAT_TEMPERATURE,
    MAX_ANSWER_CHARS,
    RETRIEVAL_MIN_SCORE,
)
from src.foundry_runtime import ensure_model_loaded
from src.retrieval import keyword_overlap, retrieve


FALLBACK_ANSWER = "Yerel dokümanlarda bu bilgi yok."


SYSTEM_PROMPT = """Sen yerel çalışan bir RAG asistanısın.
Yalnızca verilen bağlamdan cevap ver.
Bağlam cevabı içermiyorsa tam olarak şunu söyle: Yerel dokümanlarda bu bilgi yok.
Bağlamdaki ifadeleri ve gerçekleri kullan. Dışarıdan bilgi ekleme.
Türkçe cevap ver. Cevabın 2-4 kısa cümle olsun ve kullandığın doküman başlığını belirt."""


def answer_question(question: str) -> dict:
    sources = retrieve(question)
    if not sources or sources[0]["score"] < RETRIEVAL_MIN_SCORE:
        return {
            "answer": FALLBACK_ANSWER,
            "sources": summarize_sources(sources),
        }

    context = build_context(sources)

    model = ensure_model_loaded(CHAT_MODEL_ALIAS)
    client = model.get_chat_client()
    client.settings.temperature = CHAT_TEMPERATURE
    client.settings.max_tokens = CHAT_MAX_TOKENS
    client.settings.random_seed = 7
    response = client.complete_chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Bağlam:\n"
                    f"{context}\n\n"
                    "Soru:\n"
                    f"{question}\n\n"
                    "Cevap:"
                ),
            },
        ]
    )
    answer = response.choices[0].message.content.strip()
    if is_low_quality_answer(answer, sources):
        answer = build_extractive_answer(sources, question)

    return {
        "answer": answer,
        "sources": summarize_sources(sources),
    }


def build_context(sources: list[dict]) -> str:
    blocks = []
    for source in sources:
        blocks.append(
            "\n".join(
                [
                    f"Doküman: {source['document_title']}",
                    f"Skor: {source['score']:.4f}",
                    f"Vektör skoru: {source.get('vector_score', 0.0):.4f}",
                    f"Anahtar kelime skoru: {source.get('keyword_score', 0.0):.4f}",
                    f"Metin: {source['text']}",
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def summarize_sources(sources: list[dict]) -> list[dict]:
    return [
        {
            "document_title": source["document_title"],
            "source_path": source["source_path"],
            "chunk_index": source["chunk_index"],
            "score": source["score"],
            "vector_score": source.get("vector_score", 0.0),
            "keyword_score": source.get("keyword_score", 0.0),
            "text": source["text"][:500],
        }
        for source in sources
    ]


def is_low_quality_answer(answer: str, sources: list[dict]) -> bool:
    if not answer:
        return True
    if len(answer) > MAX_ANSWER_CHARS:
        return True
    source_titles = [source["document_title"].lower() for source in sources]
    if source_titles and not any(title in answer.lower() for title in source_titles):
        return True
    lower_answer = answer.lower()
    repeated_markers = ["aynı zamanda", "genel bir", "kullanıcıya uygun"]
    return any(lower_answer.count(marker) >= 2 for marker in repeated_markers)


def build_extractive_answer(sources: list[dict], question: str) -> str:
    if not sources:
        return FALLBACK_ANSWER
    source = sources[0]
    text = clean_markdown_text(source["text"])
    title = source["document_title"]
    if text.lower().startswith(title.lower()):
        text = text[len(title) :].strip()
    sentences = split_sentences(text)
    ranked_sentences = sorted(
        sentences,
        key=lambda sentence: keyword_overlap(question, sentence),
        reverse=True,
    )
    selected_sentences = [sentence for sentence in ranked_sentences[:1] if sentence]
    selected = " ".join(selected_sentences).strip() or text[:MAX_ANSWER_CHARS]
    if len(selected) > MAX_ANSWER_CHARS:
        selected = selected[:MAX_ANSWER_CHARS].rsplit(" ", 1)[0] + "..."
    return f"{selected} Kaynak: {title}."


def split_sentences(text: str) -> list[str]:
    normalized = " ".join(text.split())
    parts = []
    current = []
    for char in normalized:
        current.append(char)
        if char in ".!?":
            sentence = "".join(current).strip()
            if sentence:
                parts.append(sentence)
            current = []
    remainder = "".join(current).strip()
    if remainder:
        parts.append(remainder)
    return parts


def clean_markdown_text(text: str) -> str:
    cleaned = text.replace("\n", " ").strip()
    cleaned = cleaned.replace("# ", "")
    cleaned = cleaned.replace("## ", "")
    return " ".join(cleaned.split())
