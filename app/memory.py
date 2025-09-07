from datetime import datetime
from typing import Dict, List
from typing import Optional

from pydantic import BaseModel, Field
import math
import re
from collections import Counter, defaultdict


class MemoryItem(BaseModel):
    """A single piece of memory stored for an LLM / user."""

    user_id: str
    llm: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemoryStore:
    """Simple in-process memory store.

    This is suitable for prototyping; swap with a database or external cache in production.
    """

    def __init__(self) -> None:
        self._store: Dict[str, List[MemoryItem]] = {}

    def add(self, item: MemoryItem) -> None:
        """Add a memory item to the store."""
        self._store.setdefault(item.user_id, []).append(item)

    def get(self, user_id: str) -> List[MemoryItem]:
        """Return all memory for a user (ordered by timestamp ascending)."""
        return sorted(self._store.get(user_id, []), key=lambda m: m.timestamp)

    def search(self, user_id: str, query: str, *, llm: Optional[str] = None) -> List[MemoryItem]:
        """Search a user's memory for items whose content contains the given query (case-insensitive).

        Optionally filter by the originating LLM.
        """
        query_lc = query.lower()
        results = [m for m in self.get(user_id) if query_lc in m.content.lower()]
        if llm is not None:
            results = [m for m in results if m.llm == llm]
        return results

    def delete(self, user_id: str) -> int:
        """Delete **all** memories for a user.

        Returns the number of items removed so callers can confirm deletion.
        """
        items = self._store.pop(user_id, [])
        return len(items)

    # Relevant memory retrieval
    def relevant(
        self,
        user_id: str,
        prompt: str,
        *,
        llm: Optional[str] = None,
        k: int = 5,
        min_score: float = 0.0,
    ) -> List[MemoryItem]:
        """Return the top-k memory items most relevant to the given prompt.

        This uses a lightweight TF-IDF cosine similarity over tokenized text.
        """
        items = self.get(user_id)
        if llm is not None:
            items = [m for m in items if m.llm == llm]

        if not items:
            return []

        # Simple tokenizer: alnum lowercased tokens
        token_pattern = re.compile(r"[a-z0-9]+")

        def tokenize(text: str) -> List[str]:
            return token_pattern.findall(text.lower())

        # Build document term frequencies
        docs_tokens: List[List[str]] = [tokenize(m.content) for m in items]
        prompt_tokens = tokenize(prompt)

        if not prompt_tokens:
            # If the prompt is empty or only stop chars, return the most recent k
            return list(reversed(items))[:k]

        # Document frequencies
        df = defaultdict(int)
        for tokens in docs_tokens:
            for term in set(tokens):
                df[term] += 1

        num_docs = len(docs_tokens)

        def idf(term: str) -> float:
            # Smoothed IDF
            return math.log((num_docs + 1) / (df.get(term, 0) + 1)) + 1.0

        def tfidf_vector(tokens: List[str]) -> Dict[str, float]:
            tf = Counter(tokens)
            vec: Dict[str, float] = {}
            for term, count in tf.items():
                vec[term] = (count / len(tokens)) * idf(term)
            return vec

        def cosine_sim(a: Dict[str, float], b: Dict[str, float]) -> float:
            # Dot product
            dot = 0.0
            for term, aval in a.items():
                bval = b.get(term)
                if bval is not None:
                    dot += aval * bval
            # Norms
            anorm = math.sqrt(sum(v * v for v in a.values())) or 1.0
            bnorm = math.sqrt(sum(v * v for v in b.values())) or 1.0
            return dot / (anorm * bnorm)

        prompt_vec = tfidf_vector(prompt_tokens)

        scored: List[tuple[float, MemoryItem]] = []
        for tokens, item in zip(docs_tokens, items):
            doc_vec = tfidf_vector(tokens)
            score = cosine_sim(prompt_vec, doc_vec)
            scored.append((score, item))

        # Filter and sort by score desc, then by recency desc for tie-breaker
        filtered = [si for si in scored if si[0] >= min_score]
        filtered.sort(key=lambda si: (si[0], si[1].timestamp), reverse=True)
        return [item for _, item in filtered[: max(1, k)]]

    def relevant_diverse(
        self,
        user_id: str,
        prompt: str,
        *,
        llm: Optional[str] = None,
        k: int = 5,
        lambda_mult: float = 0.5,
        min_score: float = 0.0,
    ) -> List[MemoryItem]:
        """Return top-k memories using MMR (diversity-aware relevance).

        lambda_mult controls relevance vs diversity tradeoff: 1.0 is relevance-only; 0.0 is diversity-only.
        """
        items = self.get(user_id)
        if llm is not None:
            items = [m for m in items if m.llm == llm]

        if not items:
            return []

        lambda_mult = max(0.0, min(1.0, lambda_mult))

        token_pattern = re.compile(r"[a-z0-9]+")

        def tokenize(text: str) -> List[str]:
            return token_pattern.findall(text.lower())

        docs_tokens: List[List[str]] = [tokenize(m.content) for m in items]
        prompt_tokens = tokenize(prompt)

        if not prompt_tokens:
            return list(reversed(items))[:k]

        df = defaultdict(int)
        for tokens in docs_tokens:
            for term in set(tokens):
                df[term] += 1

        num_docs = len(docs_tokens)

        def idf(term: str) -> float:
            return math.log((num_docs + 1) / (df.get(term, 0) + 1)) + 1.0

        def tfidf_vector(tokens: List[str]) -> Dict[str, float]:
            tf = Counter(tokens)
            vec: Dict[str, float] = {}
            for term, count in tf.items():
                vec[term] = (count / len(tokens)) * idf(term)
            return vec

        def cosine_sim(a: Dict[str, float], b: Dict[str, float]) -> float:
            dot = 0.0
            for term, aval in a.items():
                bval = b.get(term)
                if bval is not None:
                    dot += aval * bval
            anorm = math.sqrt(sum(v * v for v in a.values())) or 1.0
            bnorm = math.sqrt(sum(v * v for v in b.values())) or 1.0
            return dot / (anorm * bnorm)

        prompt_vec = tfidf_vector(prompt_tokens)
        doc_vecs: List[Dict[str, float]] = [tfidf_vector(toks) for toks in docs_tokens]

        # Precompute similarity to prompt
        sim_to_prompt: List[float] = [cosine_sim(v, prompt_vec) for v in doc_vecs]

        # Filter out below min_score relative to prompt
        cand_indices = [i for i, s in enumerate(sim_to_prompt) if s >= min_score]
        if not cand_indices:
            return []

        selected: List[int] = []
        # Greedy MMR selection
        while len(selected) < min(k, len(cand_indices)):
            best_idx = None
            best_score = -1e9
            for i in cand_indices:
                if i in selected:
                    continue
                relevance = sim_to_prompt[i]
                if not selected:
                    diversity_penalty = 0.0
                else:
                    # Max similarity to any selected doc
                    diversity_penalty = max(
                        cosine_sim(doc_vecs[i], doc_vecs[j]) for j in selected
                    )
                score = lambda_mult * relevance - (1.0 - lambda_mult) * diversity_penalty
                # Tie-breaker: prefer more recent by timestamp when scores equal
                if score > best_score or (
                    abs(score - best_score) < 1e-9 and items[i].timestamp > items[best_idx].timestamp if best_idx is not None else True
                ):
                    best_score = score
                    best_idx = i
            if best_idx is None:
                break
            selected.append(best_idx)

        return [items[i] for i in selected]

    def relevant_pack(
        self,
        user_id: str,
        prompt: str,
        *,
        llm: Optional[str] = None,
        k: int = 10,
        budget_chars: int = 2000,
        strategy: str = "relevant",
        min_score: float = 0.0,
        lambda_mult: float = 0.5,
        candidate_multiplier: int = 3,
        separator: str = "\n\n",
    ) -> tuple[List[MemoryItem], str]:
        """Select up to k relevant memories and pack them into a single string within a character budget.

        strategy: "relevant" (TF-IDF) or "mmr" (diversity-aware).
        Returns (items, packed_text).
        """
        k = max(1, k)
        budget_chars = max(1, budget_chars)
        candidate_k = max(k, min(k * max(1, candidate_multiplier), 100))

        if strategy == "mmr":
            candidates = self.relevant_diverse(
                user_id,
                prompt,
                llm=llm,
                k=candidate_k,
                lambda_mult=lambda_mult,
                min_score=min_score,
            )
        else:
            candidates = self.relevant(
                user_id,
                prompt,
                llm=llm,
                k=candidate_k,
                min_score=min_score,
            )

        if not candidates:
            return [], ""

        packed: List[MemoryItem] = []
        pieces: List[str] = []
        current_len = 0

        for item in candidates:
            if len(packed) >= k:
                break
            piece = item.content
            add_len = (len(separator) if pieces else 0) + len(piece)
            if pieces and current_len + add_len > budget_chars:
                # Stop if adding this would exceed budget and we already packed something
                break
            if not pieces and add_len > budget_chars:
                # If the first item itself exceeds the budget, truncate it
                piece = piece[: max(0, budget_chars)]
                add_len = len(piece)
                if not piece:
                    continue
            pieces.append(piece)
            packed.append(item)
            current_len += add_len

        packed_text = separator.join(pieces)
        return packed, packed_text


# Global store instance the application can import
memory_store = MemoryStore() 