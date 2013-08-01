## Enigma Virtual Box Extractor

### Overview
It is a tool to extract the files from the file container made ​​using the program [Enigma Virtual Box](http://enigmaprotector.com/en/aboutvb.html)

### Features
 * displays information about the options with which the file was created
 * extract files

### RoadMap
 * extracting registry
 * extracting data from external packages

### Requires
[pefile](http://code.google.com/p/pefile) is a Python module to read and work with PE (Portable Executable) files

### Usage
**Tested only on Python 2.7.3 and on last version of EVB (6.70 build 20130604)**

`python evbe.py [-h] [-e] [-o output_directory] file`

Shows the information of options with which to make the file:

`python evbe.py file`

Extract data:

`python evbe.py -e file`

Extract data to custom directory:

`python evbe.py -e file -o directory`

### License
`evb-extractor`'s code uses the MIT license, see `LICENSE` file.
