from pathlib import Path
from наки import tsv, карте


def test_карте_рандомизуј():
    к = tsv.учитај_фајл(Path('тест-фајлови/tsv/карте.tsv'), карте.Карта)
    assert к
    assert len(к) == 24
    к = карте.рандомизуј(к)
    assert к
    assert len(к) == 24
