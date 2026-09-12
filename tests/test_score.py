"""Official score formula regression."""

from copper_scar.harness.score import compute_score


def test_compute_score_fixture():
    # volume_mm3 + 50*vias + 5000*copper_layers
    # 1000 + 50*10 + 5000*4 = 1000 + 500 + 20000 = 21500
    assert compute_score(1000, 10, 4) == 21500
