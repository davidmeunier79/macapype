import pytest
from macapype.nodes.extract_brain import T1xT2BET

from macapype.utils.utils_bids import create_datasink

def test_create_datasink():
    iterables = [('subjects', "mysub"), ('sessions', 'myses')]
    datasink = create_datasink(iterables)

    assert True
