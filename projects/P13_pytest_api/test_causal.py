from causal import causal_mean


def test_mean():
    assert abs(causal_mean([1, 2, 3]) - 2) < 1e-12


def test_empty():
    try:
        causal_mean([])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
