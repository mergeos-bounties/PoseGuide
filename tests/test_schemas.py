from poseguide.schemas import Pose, PoseCatalog, REQUIRED_JOINTS


def make_joints():
    return {j: {"x": 0.5, "y": 0.5, "visibility": 1.0} for j in REQUIRED_JOINTS}


def test_pose_construction():
    joints = make_joints()
    p = Pose(id="p1", name="test", tags=["demo"], standing=True, joints=joints)
    assert p.id == "p1"
    assert p.standing is True


def test_posecatalog_construction():
    joints = make_joints()
    p = Pose(id="p1", name="n", tags=["demo"], standing=True, joints=joints)
    catalog = PoseCatalog(poses=[p])
    assert len(catalog.poses) == 1
