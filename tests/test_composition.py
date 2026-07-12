from poseguide.guide.composition import composition_report, coach_bundle


def test_composition_power_stance() -> None:
    r = composition_report("power_stance")
    assert r["pose_id"] == "power_stance"
    assert r["rule"] == "thirds"
    assert r["tips"]


def test_coach_bundle_svg() -> None:
    r = coach_bundle("power_stance")
    assert r["coach_mode"] is True
    assert r["svg"]
