import pytest


@pytest.mark.skip(reason="prueba temporal del guardrail")
def test_temporal_skip() -> None:
    assert False