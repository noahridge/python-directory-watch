from pydirwatch import listen, mangage_history
from threading import Thread, Event
import time
import pytest
from shutil import rmtree
from pathlib import Path



def test_stress():


    found_paths = set()
    exit_event = Event()

    
    def run_listener(listen_path, hist, exit_event ):
        for path in (listen(listen_path, history_paths=hist)):
            # print(path)
            found_paths.add(path)
            if exit_event.is_set(): 
                print("exited")
                break


    made_paths = set()
    def make_files(listen_path,exit_event):
        for idx in range(100):
            time.sleep(0.001)
            p = (Path(listen_path)/ f"testfile_{idx}")
            p.touch()
            made_paths.add(p.resolve())
       

    try:
        p = Path("test/test_dir")
        p.mkdir(exist_ok=False)

        
        existing = set()
        for idx in range(1_000):
            exp= (Path(p)/ f"testfile_{idx}_existing")
            exp.touch()
            existing.add(exp.resolve())
        time.sleep(1)

        make_files_thread = Thread(target=make_files, args = (p,exit_event))

        listen_thread = Thread(target= run_listener, args = (p,existing, exit_event), daemon=True)

        listen_thread.start()
        make_files_thread.start()

        make_files_thread.join()
    
        time.sleep(1)
        exit_event.set()
        print(found_paths)
        print(made_paths)

        assert found_paths == made_paths

    finally:
        
        
        rmtree((p.resolve()))
        