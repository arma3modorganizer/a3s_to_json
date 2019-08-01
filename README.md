
# a3s_to_json (WIP)
## Description
Converts [Arma3Sync](https://forums.bohemia.net/forums/topic/152942-arma3sync-launcher-and-addons-synchronization-software-for-arma-3/)'s binary file format (Java serialized objects) into an JSON representation.

## Requirements
 - Python (Tested with 3.7)
 - Java (Tested with 1.8.0_211)
 - All requirements listed in the [requirements.txt](https://github.com/Scarjit/a3s_to_json/blob/master/requirements.txt)

## Usage

 1. Install all requirements
 2. Clone the repository
 3. Run:
```bash
python Parser.py \<url> \<filename>
```
4. Example:
```bash
python Parser.py ftp://arma.github.com/.a3s/ git_repo.json
```

# Please note, that this project is WIP, the json output can change at any new commit !

## Licenses
a3s_to_json is developed under [Unlicense](https://github.com/arma3modorganizer/pyJParse/LICENSE).

## Credits

 - [Chris Frohoff for JDeserialize](https://github.com/frohoff/jdeserialize/tree/master/jdeserialize) [Public Domain]
 - [Jetbrains](https://www.jetbrains.com/) for PyCharm <3

