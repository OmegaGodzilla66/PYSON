# PYSON #
##### Maintained by: [OmegaGodzilla66](https://github.com/OmegaGodzilla66), [ComputingSquid](https://github.com/ProbablyComputingSquid), and [coolSchnoodle](https://github.com/coolSchnoodle) #####


## Overview ##
The purpose of this project is to provide a python-based alternative to JSON. This is a (almost) fully functional JSON-inspired data management system!

## How to Use ##
<strong>THIS PROJECT IS NOT YET FINISHED! DOCUMENTATION IS ONLY SHOWN FOR COMPLETED FEATURES. SOME FEATURES MAY BREAK DUE TO CONTINUED DEVELOPMENT. IF YOU SEE A PROBLEM, PLEASE LET ME KNOW!</strong>
<br>Belive it or not, this project is surprisingly easy to use. The only thing you have to do is copy/paste the contents of pyson.py into your own Python project! From then, you can just `import pyson`, and use functions as normal! Support for other languages may come soon. Support for this as a library (no copypaste needed) may be coming soon as well.
<br><strong>The PYSON format does NOT include a newline at the end of the file, files with a newline at the end will be considered invalid</strong>
### List of Functions ###

#### getData() ####
Required inputs: `filePath`, `datacall`<br>
Output: The item in the stored type at index `datacall` in file `filePath`<br>

#### getWhole() ####
Required inputs: `filePath`<br>
Output: A list of all datas in their respective types<br>

#### updateData() ####
Required inputs: `filePath`, `name`, `data`<br>
Updates entry `name` to contain value `data`<br>
Output: Whether or not function call worked<br>

#### isCompatible() ####
Required inputs: `filePath`<br>
Outputs: Bool<br>
Checks if a file is compatible with .cnf file format. Returns True if so, returns False if not. <br>

## Supported Types ##
There are 4 supported types: int, float, str, and list
<br><br>
An int is a whole number that can be any value<br>
A str is a list of text (quotes not required)<br>
A list is a list of values, which currently have to all be strings. List items are seperated by the (*) seperator. Currently there is no escaping support. I don't really know why you would use that value normally in a list. <br> 
A float is a decimal number, that can be any value<br>

More supported types may be added. 

## Changelog ##
v0.0.8: Added updateData function
v0.0.7: Fixed errors, refactored bad code
v0.0.6: Added floats
v0.0.5: Updated naming system, ported to github!
v0.0.4: Added a function that checks if a file is compatible with .pyson file format. Fixed a bug in the write. Other general bug fixes. 

v0.0.3: Added a write function! This is now (technicaally) a fully functioning data service!<br>
v0.0.2: Added a read function for the whole file. Returns a list of all contents. This is actually getting pretty cool!<br>
v0.0.1: Initial launch! Basic reading features for a .cnf file. Current compatible types are string, int, and list. <br>

### Dev comments ###
0.0.8: I (computingSquid) have had to resort to drastic measures to get my pull request approved. coolSchnoodle was forced to say "uwu"
0.0.5: <br>
Wahoo! Porting to github!...oh shoot now I have to rename everything. 
0.0.4: <br>
HAHA I HAVE DONE IT! ... Wait no never mind I'm stupid - OmegaGodzilla66
Compatability checks are my nightmare. AAAAAA. - OmegaGodzilla66