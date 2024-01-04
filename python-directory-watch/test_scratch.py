from scratch import listen, _mangage_history
import pytest
from pathlib import Path


@pytest.fixture()
def empty_history_file(tmpdir):
    p = (Path(tmpdir) / "temphistory.tmp")
    p.touch()

    return p

@pytest.fixture()
def filled_history_file(tmpdir):
    p = (Path(tmpdir) / "temphistory2.tmp")
    p.touch()
    with p.open(mode = "w") as f:
        f.write("djkfhskjhf\n")

    return p


def test_manage_history(empty_history_file):

    items = set(["fasjhf", "sdfhslfh", "sjdfhsjkdhf", "skjdfhskdjf"])
    
    with _mangage_history(empty_history_file) as h:

        h.update(set(items))
    
    with open(empty_history_file) as f:
        updated_hist = set([x.strip() for x in  f.readlines()])


    assert items == updated_hist

def test_manage_history_filled(filled_history_file):
    """Test _manage_history adds new items and preserves existing"""

    items = set(["fasjhf", "sdfhslfh", "sjdfhsjkdhf", "skjdfhskdjf"])
    
    with _mangage_history(filled_history_file) as h:

        h.update(set(items))
    
    with open(filled_history_file) as f:
        updated_hist = set([x.strip() for x in  f.readlines()])

    items.add("djkfhskjhf")

    assert updated_hist == items


