from pathlib import Path
from contextlib import contextmanager
import warnings
from typing import Generator


@contextmanager
def mangage_history(history_file: Path):
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
    path: Path, *, history_paths=set(), pattern: str = "*", resolve_paths=True
) -> Generator[Path, None, None]:
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
