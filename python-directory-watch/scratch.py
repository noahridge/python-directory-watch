from pathlib import Path
from contextlib import contextmanager


@contextmanager
def mangage_history(history_file: Path):

    try:
        with open(history_file, mode = "r") as f:
            initial =  set([x.strip() for x in f.readlines()])
            yield initial
    

    finally:
        with open(history_file, mode = "w") as f: 
            for file in initial:
                f.write(f"{file}\n")


def listen(path : Path, history_paths = set(), pattern:str = "*") -> Path:

    """_summary_
    path: pathlib Path object which is the directory to be searched
    pattern: unix style glob pattern to filter for paths matching criteria. Corresponds to allowed glob patterns in pathlib.Path.glob() method.  
    Yields:
    pathlib.Path object
    """
    if not isinstance(pattern, str):
        raise ValueError("Input pattern must be a str object. ")
    
    if not isinstance(path, Path):
        raise ValueError("Input path must be a pathlib.Path object")

    if not path.is_dir():
        raise ValueError(f"Input path must be a directory '{path}' is not a directory.")

    # history_file  = (Path.cwd().resolve() / Path("~listen_history.temp"))
    # history_file.touch()

    # with _mangage_history(history_file) as history:

    # history_paths = set([Path(p).resolve() for p in history])

    while True:
        items = set([p.resolve() for p in path.glob(pattern)])
        new_items = items.difference(history_paths)
        
        if new_items:

            for item in new_items:
    
                yield item
                # history.add(item)
                history_paths.add(item)
                    
                  


        

if __name__ == "__main__":
    import traceback

    history_file  = (Path.cwd().resolve() / Path("~listen_history.temp"))
    history_file.touch()

    with mangage_history(history_file) as history:

        history_paths = set([Path(p).resolve() for p in history])

        for new_file in listen(Path("test_dir"), history_paths=history_paths):

            try:
                #DO STUFF
                print(f"{new_file}")

                if new_file.name.startswith("s"):
                    raise ValueError("kjshdfkjshdkf")
                
                #ADD to history if sucessful
                history.add(new_file)
            
            except Exception :
                traceback.print_exc()

            


