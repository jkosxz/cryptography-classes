# Hash functions
## How to run
### Export needed environmental variables
```bash
export PATH_TO_FILE=<PATH_TO_FILE_TO_HASH>
export SHAKE_HASH_LENGTH=<DIGEST_LENGTH_FOR_SHAKE_HASH_FUNCTION>
```
or 
```bash
set PATH_TO_FILE=<PATH_TO_FILE_TO_HASH>
set SHAKE_HASH_LENGTH=<DIGEST_LENGTH_FOR_SHAKE_HASH_FUNCTION>
```
Variable PATH_TO_FILE must lead to an existing file.
### Run the main script
```bash
python ./main.py
```
Running the script will pop up your browser with plotly graph