from pathlib import Path
from contextlib import contextmanager
from typing import Generator
from os import PathLike


@contextmanager
def mangage_history(history_file: Path) -> Generator[set[str], None, None]:
    """Context manager which reads and writes to file with newline delimited strings. 
    Yeilds a set of the strings contained in the file or an empty set, 
    any items added to the set will be written to the file when the context manager exits. 
    Creates a file if the history_file argument is not an existing filepath.

    Parameters
    ----------
    history_file : Path
        Path to history file location

    Yields
    ------
    Generator[set[str], None, None]
        A set containing items from newline delimited file. 
    """    
    history_file.touch()

    try:
        with open(history_file, mode="r") as f:
            initial = set([x.strip() for x in f.readlines()])
            yield initial

    finally:
        with open(history_file, mode="w") as f:
            for file in initial:
                f.write(f"{file}\n")


def listen(
    path: Path, *, history_paths: set[PathLike]=set(), pattern: str = "*", resolve_paths: bool=True
) -> Generator[Path, None, None]:
    """Generator which polls for new files in a directory and yeilds when new files are found. Will block unless new file is found. 

    Parameters
    ----------
    path : Path
        The directory which should be watched for new files. 
    history_paths : set[PathLike], optional
        set of path objects which should be ignored (usually because they were already processed), by default empty set()
    pattern : str, optional
        Unix glob patterns to filter new paths found. Conforms to patterns allowed in pathlib.Path.glob. , by default "*"
    resolve_paths : bool, optional
        All paths found will be resolved to absolute using pathlib.Path.resolve, by default True

    Yields
    ------
    Generator[Path, None, None]
        Will yield paths to new files found in the directory. Blocks until new file is found.

    Raises
    ------
    ValueError
        Check that path parameter is valid directory & pathlib.Path object
    ValueError
        Check that history_paths is valid python set
    ValueError
        Check that pattern is a string.

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

    history_paths_converted = set()
    for hist_path in history_paths:
       
        history_paths_converted.add(Path(hist_path))

    
    yield from _listen(
        path, history_paths=history_paths_converted, pattern=pattern, resolve_paths=resolve_paths
    )


def _listen(
    path: Path, *, history_paths=set(), pattern: str = "*", resolve_paths=True
) -> Generator[Path, None, None]:
    
    while True:
        if resolve_paths:
            items = set([p.resolve() for p in path.glob(pattern)])
        else:
            items = set([p for p in path.glob(pattern)])

        new_items = items.difference(history_paths)

        if new_items:
            for item in new_items:
                yield item

                history_paths.add(item)
