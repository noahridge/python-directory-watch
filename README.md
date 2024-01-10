# python-directory-watch

A minimal python package with the singular goal to watch a directory for new files. 

Designed to allow for processing of files upon creation. Such as reading data files in CSV format into a database upon creation. 

Inludes functionality to persist history on disk, allowing for the restart of python process running the service


# Usage

The ```listen``` generator prodvides a mechanism to yeild the path for each new file in the provided directory. New file discover is performed by polling the directory. This generator is an infinite blocking generator so should be run in a seperate thread or python process. 

The ```manage_history``` context manager provides a mechanism to write history file. This is simply a newline delimited list of paths which have already been processed. The history manager returns a python set string paths. Any items added to this set will automatically be written to the file at the end when the python process ends. 

```python
import traceback
from pydirwatch import listen, manage_history

history_file  = (Path.cwd().resolve() / Path("~pydirwatch_history.temp"))
history_file.touch()

with mangage_history(history_file) as history:

    history_paths = set([Path(p).resolve() for p in history])

    for new_file_path in listen(Path("test_dir"), history_paths=history_paths):

        try:
            #DO STUFF with new_file_path
            print(f"{new_file}")
            
            #ADD to history if sucessfull
            history.add(new_file)
        
        except Exception :
            # For use cases such as writing to database often exceptions should be handled with our raising and stopping python process.
            traceback.print_exc()
```

## Installation




