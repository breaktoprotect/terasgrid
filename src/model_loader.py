from sentence_transformers import SentenceTransformer
from config import MODEL_ID

_model_instance: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load and cache the SBERT model so it's only initialized once."""
    global _model_instance
    if _model_instance is None:
        _model_instance = SentenceTransformer(MODEL_ID)
    return _model_instance
