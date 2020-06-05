import pytest
from pathlib import Path

import codesleuth as cs

R = Path(__file__).resolve().parents[3]


def test_detect():

    langs = cs.detect_lang(R)

    assert len(langs) == 1
    assert "python" in langs


if __name__ == "__main__":
    pytest.main([__file__])
