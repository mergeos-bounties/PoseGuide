from __future__ import annotations

import json
from pathlib import Path


def write_guidance_overlay(result: dict, out_path: Path) -> Path:
    """
    Write a JSON guidance payload a camera UI could consume.
    Real overlay drawing (OpenCV/Pillow) is a bounty.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "poseguide.overlay.v1",
        "result": result,
        "draw_hints": [
            {"type": "skeleton", "source": "target_pose"},
            {"type": "text_banner", "text": "Align your stance with the guide"},
        ],
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path
