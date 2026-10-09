import os
from django.conf import settings

# Global variables initialized to None to prevent heavy startup memory usage
_model = None
_model_attempted = False
_tfidf_dim = 100

# Cache matching job.id to (updated_at_timestamp, embedding_vector)
_job_embeddings_cache = {}

SKILL_MAP = {
    "js": "javascript",
    "node": "nodejs",
    "reactjs": "react",
    "ts": "typescript",
}


def get_sentence_model():
    """
    Lazy-load the SentenceTransformer model only when needed.
    """
    global _model, _model_attempted

    if not _model_attempted:
        _model_attempted = True

        try:
            from sentence_transformers import SentenceTransformer

            hf_token = getattr(
                settings,
                "HF_TOKEN",
                os.environ.get("HF_TOKEN")
            )

            model_kwargs = {
                "local_files_only": True
            }

            if hf_token:
                model_kwargs["token"] = hf_token

            _model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                **model_kwargs
            )

            print(
                "Loaded sentence-transformers model "
                "all-MiniLM-L6-v2 from local cache"
            )

        except Exception as e:
            print(
                "Could not load sentence-transformers model "
                "(using TF-IDF fallback):",
                e
            )
            _model = None

    return _model


def get_tfidf_embeddings(texts):
    """
    Generate TF-IDF embeddings as a fallback.
    """

    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer

    if not texts:
        return np.array([], dtype=np.float32)

    vectorizer = TfidfVectorizer(
        max_features=_tfidf_dim,
        stop_words="english"
    )

    return vectorizer.fit_transform(texts).toarray().astype(
        np.float32
    )


def preprocess_text(text):
    if not text:
        return ""

    text = text.lower().replace(",", " ")

    words = text.split()

    normalized_words = [
        SKILL_MAP.get(word, word)
        for word in words
    ]

    return " ".join(normalized_words).strip()


def enhance_text_with_skills(text, skills):
    """
    Enhance text by repeating skills twice
    for increased weight in embeddings.
    """

    if not text:
        text = ""

    if not skills:
        return text

    skills_str = " ".join(
        [
            preprocess_text(str(skill))
            for skill in skills
            if skill
        ]
    )

    if not skills_str:
        return text

    weighted_skills = f"{skills_str} {skills_str}"

    return f"{text} {weighted_skills}".strip()


def encode_jobs(jobs):
    import numpy as np

    if not jobs:
        return np.array([], dtype=np.float32)

    model = get_sentence_model()

    if model is not None:

        embeddings = []
        jobs_to_encode = []
        indices_to_update = []

        for idx, job in enumerate(jobs):

            cached = _job_embeddings_cache.get(job.id)

            job_updated_str = (
                str(job.updated_at)
                if getattr(job, "updated_at", None)
                else ""
            )

            if cached and cached[0] == job_updated_str:
                embeddings.append(cached[1])

            else:
                embeddings.append(None)
                jobs_to_encode.append(job)
                indices_to_update.append(idx)

        if jobs_to_encode:

            new_embeddings = model.encode(
                [
                    job.get_text_representation()
                    for job in jobs_to_encode
                ],
                convert_to_numpy=True
            )

            for job, idx, emb in zip(
                jobs_to_encode,
                indices_to_update,
                new_embeddings
            ):

                job_updated_str = (
                    str(job.updated_at)
                    if getattr(job, "updated_at", None)
                    else ""
                )

                _job_embeddings_cache[job.id] = (
                    job_updated_str,
                    emb
                )

                embeddings[idx] = emb

        return np.array(
            embeddings,
            dtype=np.float32
        )

    else:
        # TF-IDF fallback

        job_texts = [
            job.get_text_representation()
            for job in jobs
        ]

        return get_tfidf_embeddings(job_texts)


def encode_user(profile):
    import numpy as np

    model = get_sentence_model()

    if not profile:
        dim = 384 if model else _tfidf_dim
        return np.zeros(dim, dtype=np.float32)

    try:
        text = profile.get_text_representation()

        skills = getattr(
            profile,
            "skills",
            []
        )

        if not text or not text.strip():
            dim = 384 if model else _tfidf_dim
            return np.zeros(dim, dtype=np.float32)

    except AttributeError:

        dim = 384 if model else _tfidf_dim

        return np.zeros(
            dim,
            dtype=np.float32
        )

    if model is not None:

        enhanced_text = enhance_text_with_skills(
            text,
            skills
        )

        return model.encode(
            enhanced_text,
            convert_to_numpy=True
        )

    else:

        return get_tfidf_embeddings([text])[0]


# Keep the module import-safe: model loading is intentionally lazy.
# Importing this service must not trigger a remote model download.
model = None
