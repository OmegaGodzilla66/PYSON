# PYSON #
##### Maintained by: [OmegaGodzilla66](https://github.com/OmegaGodzilla66), [ComputingSquid](https://github.com/ProbablyComputingSquid), [CoolSchnoodle](https://github.com/CoolSchnoodle), and [nmd102](https://github.com/nmd102) #####


## Overview ##
The purpose of this project is to provide a python-based alternative to JSON. This is a (almost) fully functional JSON-inspired data management system!

## How to Use ##
This is a pip package, so to use this in python you can just `pip install pyson-data`.
From there, you can just `import pyson_data as pyson`.
Support for other languages may come soon.<br>

## Quickstart ##
Refer to the project wiki [here](https://github.com/OmegaGodzilla66/PYSON/wiki)

## Documentation ##
Documentation has also been moved to the project wiki [here](https://github.com/OmegaGodzilla66/PYSON/wiki) to decrease clutter in the README.

## Supported Types ##
There are 4 supported types: int, float, str, and list
<br><br>
- An int is a whole number that can be any valu
- A str is a list of text (quotes not required)
- A list is a list of values, which currently have to all be strings. List items are seperated by the (*) seperator.
Currently there is no escaping support. I don't really know why you would use that value normally in a list.
- A float is a decimal number, that can be any value representable by a 64-bit floating point number.
<br>More supported types may be added  at some point in the future. 

## Changelog ##
- v0.1.3: Added getDict function
- v0.1.2: Refactored pyson.py
- v0.1.1: Added writeMultiple function, various bug fixes
- v0.1.0-alpha: package & release deployed to pypi, merged code to main, and resolved all merge conflicts! truly a cause for celebration 🎉
- v0.0.9: coolSchnoodle and nmd102 made code fixes and README fixes
- v0.0.8: Added updateData function
- v0.0.7: Fixed errors, refactored bad code
- v0.0.6: Added floats
- v0.0.5: Updated naming system, ported to github!
- v0.0.4: Added a function that checks if a file is compatible with .pyson file format. Fixed a bug in the write. Other general bug fixes.
- v0.0.3: Added a write function! This is now (technically) fully functional!
- v0.0.2: Added a read function for the whole file. Returns a list of all contents.
- v0.0.1: Initial launch! Basic reading features for a .cnf (renamed almost immediately to pyson) file. Current compatible types are string, int, and list.
