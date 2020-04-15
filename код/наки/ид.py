def assert_ид(ид):
    assert isinstance(ид, str)
    assert len(ид) == 32, f"лоша дужина {ид}"


def извор_ид(ид):
    return ид[:-1] + '0'

