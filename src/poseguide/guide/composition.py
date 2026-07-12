"""Rule-of-thirds and framing composition hints for poses."""

from __future__ import annotations

from poseguide.models.catalog import get_pose_by_id


def composition_report(pose_id: str) -> dict:
    """
    Analyze pose joint placement against a 3×3 rule-of-thirds grid (normalized 0–1).

    Returns per-landmark nearest third-line and overall framing tips.
    """
    pose = get_pose_by_id(pose_id)
    if pose is None:
        raise KeyError(f"unknown pose {pose_id!r}")
    joints = pose.get("joints") or {}
    thirds = (1 / 3, 2 / 3)
    lines: list[dict] = []
    tips: list[str] = []

    def nearest_third(v: float) -> tuple[float, float]:
        best = min(thirds, key=lambda t: abs(t - v))
        return best, abs(best - v)

    nose = joints.get("nose")
    if nose and len(nose) >= 2:
        x, y = float(nose[0]), float(nose[1])
        tx, dx = nearest_third(x)
        ty, dy = nearest_third(y)
        lines.append({"joint": "nose", "xy": [round(x, 3), round(y, 3)], "nearest_third": [tx, ty], "delta": [round(dx, 3), round(dy, 3)]})
        if dx < 0.08:
            tips.append("Eyes/head near a vertical third — strong portrait placement.")
        if y < 0.25:
            tips.append("Head in upper third — leave breathing room above crown.")

    # shoulder span vs frame
    ls, rs = joints.get("l_shoulder"), joints.get("r_shoulder")
    if ls and rs and len(ls) >= 2 and len(rs) >= 2:
        span = abs(float(rs[0]) - float(ls[0]))
        mid_x = (float(ls[0]) + float(rs[0])) / 2
        lines.append({"joint": "shoulders", "span": round(span, 3), "mid_x": round(mid_x, 3)})
        if 0.28 <= span <= 0.45:
            tips.append("Shoulder width fills the frame without cropping elbows.")
        elif span > 0.5:
            tips.append("Subject is very wide in frame — step back or use a wider lens.")
        tx, dx = nearest_third(mid_x)
        if dx < 0.1:
            tips.append(f"Torso center aligns near vertical third ({tx:.2f}).")

    # feet / grounding
    la, ra = joints.get("l_ankle"), joints.get("r_ankle")
    if la and ra and len(la) >= 2 and len(ra) >= 2:
        ground_y = max(float(la[1]), float(ra[1]))
        lines.append({"joint": "ankles", "ground_y": round(ground_y, 3)})
        if ground_y > 0.85:
            tips.append("Feet near bottom edge — good grounded standing shot.")
        elif ground_y < 0.7 and pose.get("standing", True):
            tips.append("Crop higher for standing pose or include more floor for stability.")

    if not tips:
        tips.append("Balanced placement — refine with subject-specific coach score.")

    return {
        "pose_id": pose.get("id"),
        "name": pose.get("name"),
        "rule": "thirds",
        "analysis": lines,
        "tips": tips,
        "score_hint": round(max(0.0, 1.0 - sum(a.get("delta", [0, 0])[0] for a in lines if "delta" in a) / max(1, len(lines))), 3),
    }


def coach_bundle(pose_id: str, subject_path=None) -> dict:
    """Composition report + optional subject score for side-by-side coaching."""
    from pathlib import Path

    from poseguide.guide.score import score_subject_against_pose
    from poseguide.render.svg import render_pose_svg
    from poseguide.config import OUT_DIR

    comp = composition_report(pose_id)
    svg_path = render_pose_svg(pose_id, OUT_DIR / f"coach_{pose_id}.svg")
    out: dict = {
        "composition": comp,
        "svg": str(svg_path),
        "coach_mode": True,
    }
    if subject_path is not None:
        path = Path(subject_path)
        out["subject_score"] = score_subject_against_pose(pose_id, path)
    return out
