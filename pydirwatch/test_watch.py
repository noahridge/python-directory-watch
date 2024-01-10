from pydirwatch import listen, mangage_history
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
    
    with mangage_history(empty_history_file) as h:

        h.update(set(items))
    
    with open(empty_history_file) as f:
        updated_hist = set([x.strip() for x in  f.readlines()])


    assert items == updated_hist

def test_manage_history_filled(filled_history_file):

    items = set(["fasjhf", "sdfhslfh", "sjdfhsjkdhf", "skjdfhskdjf"])
    
    with mangage_history(filled_history_file) as h:

        h.update(set(items))
    
    with open(filled_history_file) as f:
        updated_hist = set([x.strip() for x in  f.readlines()])

    items.add("djkfhskjhf")

    assert updated_hist == items


@pytest.fixture(scope = "session")
def listen_dir(tmp_path_factory):
    p = tmp_path_factory.mktemp("test_listen_dir") 

    return p

def test_listen(listen_dir):

    new_file = Path(listen_dir) /Path("mytestfile.test")
    new_file.touch()

    listen_gen = listen(listen_dir)

    assert next(listen_gen) == new_file
    
    new_file_2 = Path(listen_dir) /Path("mytestfile2.test")
    new_file_2.touch()

    assert next(listen_gen) == new_file_2


def test_listen_errors(listen_dir):

    with pytest.raises(ValueError) as exec_info:
        next(listen(listen_dir, history_paths=["sjdfhsdjf"]))
        assert exec_info.value.contains("history_paths object must be a python set.")

    with pytest.raises(ValueError) as exec_info:
        next(listen(listen_dir, pattern=223))
        assert exec_info.value.contains("Input pattern must be a str object")

    with pytest.raises(ValueError):
        next(listen("test/test"))
        assert exec_info.value.contains("Input path must be a pathlib.Path object")

    with pytest.warns(UserWarning, match = "not a pathlib.Path object"):

        next(listen(listen_dir,history_paths=set(["test/sf/sdf","sdfs/sdfsdg"])))
    
