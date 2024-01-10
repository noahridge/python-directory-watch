# python-directory-watch

A minimal python package with the goal to watch a directory for new files. Allows for filtering by filetype and persistent history across restarts. 

Designed to allow for processing of files upon creation. Such as reading CSV data files into a database upon creation. 

# Usage

The ```listen``` generator prodvides a mechanism to yeild the path for each new file in the provided directory. New file discover is performed by polling the directory. The generator will block if no new file are found so it should be run in a seperate thread or python process. 

The ```manage_history``` context manager provides a mechanism to write history file to disk. This is simply a text file containing a newline delimited list of paths which have already been processed. The history manager returns a python set of string paths. Any items added to this set will automatically be written to the file when the python process ends. 

The ```listen``` generator can be used without persistent history. Each time the generator is started all files matching the pattern will be yielded.

```python

 for new_file_path in listen(Path("test_dir"),  pattern = "*.txt"):

        try:
            #DO STUFF with new_file_path
            print(f"{new_file_path}")
            
            #ADD to history if sucessful
            history.add(new_file)
        
        except Exception:
            # For use cases such as writing to database often exceptions 
            # should be handled without raising exceptions and stopping python process.
            traceback.print_exc()
```

By creating a history file and using the ```manage_history``` generator, history can be persisted on the disk. Only files not present in the history will be yielded upon starting the genertor. 

```python
import traceback
from pydirwatch import listen, manage_history

history_file  = (Path.cwd().resolve() / Path("~pydirwatch_history.temp"))
history_file.touch()

with mangage_history(history_file) as history:

    history_paths = set([Path(p).resolve() for p in history])

    for new_file_path in listen(Path("test_dir"), history_paths=history_paths, pattern = "*.txt"):

        try:
            #DO STUFF with new_file_path
            print(f"{new_file_path}")
            
            #ADD to history if sucessful
            history.add(new_file_path)
        
        except Exception:
            # For use cases such as writing to database often exceptions 
            # should be handled without raising exceptions and stopping python process.
            traceback.print_exc()
```

## Installation

pip install git+https://github.com/noahridge/python-directory-watch.git

