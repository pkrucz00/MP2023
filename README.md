# MP2023

The repository contains artifacts that came into existance during the *Pracownia problemowa* course at AGH Science and Technology. Main contributors: [@pkrucz00](https://github.com/pkrucz00) and [@czyjtu](https://github.com/czyjtu) 

The repository consists of mainly two things:

1. A CLI tool for acquiring gene data from *Crusader Kings III*.
2. Tests of face recognition tools.

## How to run data acquisition tool

The python scripts are located in the `face_generator` folder.

### Requirements

- `Python 3.10` or higher
- A `Crusader Kings III` installation and path to it
    -  **Important!!!** for the `generate_faces_portraint_editor.py` the in-game `debug mode` should be enabled so the portrait editor is available (instructions on how to enable `debug mode` are given [here](https://www.reddit.com/r/CrusaderKings/comments/ikua0e/a_crash_course_into_ck3_custom_portraits/))  

### Description

The repository contains two scripts:

1. `generate_faces.py` - generates faces to the `results` folder. It saves text files with *DNA* of a randomized character and a `jpeg` image of its appearance. The process is repeated `n` times per all possible in-game ethnicity and sex combinations that are stored in different folders.

2. `generate_faces_portrait_editor.py` -- **EXPERIMENTAL AND BUGGY** - variation on the aforementioned scripts that also takes a list of genes and a given DNA as an input and makes all possible variations of it. Unfortunately, at this moment it requires more manual work to make it work (see the *Other important stuff/issues* part for more info). 

### Usage

Most basic usage is to go into the script folder and run:

```bash
python3 generate_faces.py --exec PATH_TO_CK_III
```

For more optional features see `python3 generate_faces.py --help`.

### Other important stuff/issues
- Tested on Windows 10, but should be possible to make it work on other OSes since the python modules for controlling the mouse should work also on Linux (see its documentation for more details)
- The script finds a button by trying to locate the picture in the `locate_picks` folder. This means that:
    - it's a little bit slower than it could be if it only knew the location *a priori*
    - is vulnerable to bugs on different settings (this scripts is a *best-effort no money* mini-project not meant for production hence the limited QA and almost no assurance for other environments than the writer's laptop ;] )
- The script **does not** open the portrait mode automatically so it is mandatory to click it through once the debug mode opens