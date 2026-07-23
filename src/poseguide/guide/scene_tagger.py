from __future__ import annotations

import re
from pathlib import Path


_TAG_RULES = (
    (("beach", "coast", "ocean", "seaside"), ("beach", "outdoor")),
    (("urban", "city", "downtown"), ("urban", "outdoor")),
    (("street", "alley"), ("street", "urban", "outdoor")),
    (("wall", "brick"), ("wall",)),
    (("studio", "backdrop"), ("studio", "indoor")),
    (("portrait", "headshot"), ("portrait",)),
    (("business", "corporate"), ("business", "indoor")),
    (("office", "workplace", "lobby"), ("office", "indoor", "business")),
    (("forest", "woods", "woodland"), ("forest", "outdoor")),
    (("park", "garden"), ("garden", "outdoor")),
    (("cafe", "coffee"), ("cafe", "indoor")),
    (("home", "room", "library", "loft"), ("indoor",)),
    (("mountain", "trail", "hiking"), ("mountain", "outdoor")),
    (("sunset", "sunrise", "golden hour"), ("golden_hour", "outdoor")),
    (("night", "neon"), ("night", "urban")),
    (("rooftop", "balcony"), ("rooftop", "urban", "outdoor")),
    (("sports", "field", "stadium"), ("sports", "outdoor")),
    (("subway", "metro", "station"), ("subway", "urban", "indoor")),
    (("festival", "crowd"), ("festival", "outdoor")),
    (("harbor", "pier", "lakeside"), ("waterfront", "outdoor")),
)


def infer_scene_tags(
    *, description: str | None = None, image_path: Path | None = None
) -> list[str]:
    """Infer ranker-compatible scene tags from text and an image filename."""
    sources = [description or ""]
    if image_path is not None:
        sources.append(image_path.stem)
    normalized = re.sub(r"[^a-z0-9]+", " ", " ".join(sources).lower()).strip()
    if not normalized:
        return []

    haystack = f" {normalized} "
    tags: list[str] = []
    for keywords, inferred_tags in _TAG_RULES:
        if not any(f" {keyword} " in haystack for keyword in keywords):
            continue
        for tag in inferred_tags:
            if tag not in tags:
                tags.append(tag)
    return tags
