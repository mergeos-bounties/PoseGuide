import pytest
from poseguide.schemas import Joint, Pose, PoseCatalog, REQUIRED_JOINTS


def make_joints():
    return {j: {"x": 0.5, "y": 0.5, "visibility": 1.0} for j in REQUIRED_JOINTS}


def test_joint_validation():
    p = Pose(id="1", name="n", tags=[" t "], standing=True, joints=make_joints())
    # ensure joint fields are floats and visibility present
    joint = p.joints["nose"]
    assert isinstance(joint.x, float)
    assert isinstance(joint.y, float)
    assert joint.visibility == 1.0


def test_tags_strip_and_lower():
    p = Pose(id="1", name="n", tags=[" Demo "], standing=True, joints=make_joints())
    assert p.tags == ["demo"]


def test_missing_joint_raises():
    j = make_joints()
    j.pop("nose")
    with pytest.raises(ValueError):
        Pose(id="1", name="n", tags=["d"], standing=True, joints=j)


def test_nonstanding_raises():
    with pytest.raises(ValueError):
        Pose(id="1", name="n", tags=["d"], standing=False, joints=make_joints())


def test_posecatalog_min_items():
    p = Pose(id="1", name="n", tags=["d"], standing=True, joints=make_joints())
    with pytest.raises(ValueError):
        PoseCatalog(poses=[])
