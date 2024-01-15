from pydirwatch import listen_with_history
import pytest
from pathlib import Path
from threading import Thread, Lock
import time


@pytest.fixture(scope="session")
def listen_dir(tmp_path_factory):
    p = tmp_path_factory.mktemp("test_listen_dir")

    return p


@pytest.fixture(scope="session")
def history_path(tmp_path_factory):
    p = tmp_path_factory.mktemp("history_file")
    file = p / Path("~history_file.tmp")

    return file


def test_listen_with_history(listen_dir, history_path):
    lock = Lock()

    def make_new_files(lock: Lock, start, stop, paths):
        for i in range(start, stop):
            time.sleep(0.1)
            with lock:
                p = listen_dir / f"test_item_{i}"
                p.touch()

                paths.append(p)

    paths1 = []

    make_file_thread = Thread(target=make_new_files, args=(lock, 0, 100, paths1))
    make_file_thread.start()

    for idx, new_path in enumerate(
        listen_with_history(listen_dir, history_filepath=history_path)
    ):
        with lock:
            assert new_path == paths1[idx]

        if idx == 90:
            break

    make_file_thread.join()
    time.sleep(3)

    # time.sleep(2)
    # paths2 = []
    # make_file_thread = Thread(target= make_new_files, args = (lock,100, 200, paths2 ))
    # make_file_thread.start()

    # for idx, new_path in enumerate(listen_with_history(listen_dir, history_filepath=history_path)):
    #     with lock:
    #         print(f"{new_path =}")
    #         # print(f"{paths[idx] = }")
    #         print(idx)
    #         print(paths2)
    #         assert new_path == paths2[idx]

    #     if idx == 90:
    #         break
