from pathlib import Path
from contextlib import contextmanager
import warnings


@contextmanager
def mangage_history(history_file: Path):
    try:
        with open(history_file, mode="r") as f:
            initial = set([x.strip() for x in f.readlines()])
            yield initial

    finally:
        with open(history_file, mode="w") as f:
            for file in initial:
                f.write(f"{file}\n")


def listen(path: Path, *, history_paths=set(), pattern: str = "*") -> Path:
    """_summary_
    path: pathlib.Path object which is the directory to be searched
    pattern: str unix style glob pattern to filter for paths matching criteria. Corresponds to allowed glob patterns in pathlib.Path.glob() method.
    Yields:
    pathlib.Path objects. New files which are found in directory. Infinite blocking generator. 
    """
    if not isinstance(pattern, str):
        raise ValueError("Input pattern must be a str object. ")

    if not isinstance(path, Path):
        raise ValueError("Input path must be a pathlib.Path object")

    if not isinstance(history_paths, set):
        raise ValueError(
            f"history_paths object must be a python set. Object provided is of type {type(history_paths)}"
        )

    if not path.is_dir():
        raise ValueError(f"Input path must be a directory '{path}' is not a directory.")

    for hist_path in history_paths:
        if not isinstance(hist_path, Path):
            warnings.warn(
                f"The path `{hist_path}` in the provided history_paths set is not a pathlib.Path object. All paths will be considered new due to type mismatch."
            , UserWarning)
    
    yield from _listen(path, history_paths = history_paths, pattern = pattern)



def _listen(path: Path, *, history_paths=set(), pattern: str = "*"):

    while True:
        items = set([p.resolve() for p in path.glob(pattern)])
        new_items = items.difference(history_paths)

        if new_items:
            for item in new_items:
                yield item

                history_paths.add(item)



