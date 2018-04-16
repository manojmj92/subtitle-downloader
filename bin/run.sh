#!/bin/bash

# to be run in the same directory as "setup.py"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Forward all arguments directly to the program itself.
# e.g. running "./bin/run.sh --list -v" is equivalent to
# "python subtitle-downloader/subtitle_downloader.py --list -v"
python $DIR/../subtitle-downloader/subtitle_downloader.py "$@"
