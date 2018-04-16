#!/usr/bin/env python
"""
Test module for subtitle-downloader command line interface.

Designed to be run in the same directory as "setup.py"
"""

import subprocess
import os
import io
import glob

import sh

# syntactic sugar for (somewhat) shorter filenames in the list definition
# modify accordingly for local testing
DLDS = "/home/alecastle/Downloads/"
VIDEO_FILES = [
    "12 Monkeys (1995)/12Monkeys.mp4",          # test movie title starting with numbers
    "Brazil (1985)/Brazil.avi",                 # test .avi format, as opposed to .mp4
    "Hackers/Hackers.mp4",                      # vanilla test, no tricks
    "Monsters Inc (2001)/MonstersInc.mkv"       # test .mkv format, as opposed to .mp4
    "The Room (2003)/TheRoom.mp4",              # test spaces/parentheses in directory name
    "War Games (1983) [1080p]/WarGames.mkv",    # test square brackets in directory name (should fail)
    "Wings of Desire (1987) 720p BRrip_sujaidr (pimprg)/Wings of Desire (1987) 720p BRrip_sujaidr (pimprg).mkv"
                                                # test really long directory/file name with multiple special characters
                                                # also, this movie has a spoken language of German
]
for index, file in enumerate(VIDEO_FILES):
    VIDEO_FILES[index] = os.path.join(DLDS, file)

# directory contains multiple movies
# again, modify accordingly for local testing
VIDEO_DIRECTORY = "/home/alecastle/Desktop/Movies/"

# reinstall development build for a fresh testing environment
sh.Command("./bin/install.sh")("reinstall")

def test_run_script():
    print("test_run_script")

    executable = os.path.realpath("../bin/run.sh")

    sh.Command(executable)                          # should do nothing; default behavior is to look in
                                                    # the current directory, which in this case should
                                                    # not have any video files.
    sh.Command(executable)("--help")                # should print help message.

    buf1 = io.StringIO()
    sh.Command(executable)("--list", _out=buf1)     # should list available languages.

    buf2 = io.StringIO()
    sh.Command(executable)("--list", "-a",
                           _out=buf2)               # output should be the same as previous command
                                                    # since --list is a flag, it should take priority.
    assert buf1.getvalue() == buf2.getvalue(), "--list is a flag; it should override any other functionality"

    for file in VIDEO_FILES:
        sh.Command(executable)("-i", "en", file)    # should work except for square brackets in directory

    sh.Command(executable)("-v", VIDEO_DIRECTORY)   # test video directory

    # gather a list of subtitle files created before removing them
    sub_files = glob.glob(VIDEO_DIRECTORY + "*.srt")
    sh.Command("rm")("-rf", sub_files)

    # change directories to the path containing the video files
    current_path = os.path.realpath(__file__)
    sh.cd(os.path.abspath(VIDEO_DIRECTORY))

    # run vanilla command and ensure that the result is the same as before
    subprocess.run([executable])
    sub_files2 = glob.glob(VIDEO_DIRECTORY + "*.srt")

    try:
        assert sub_files == sub_files2
    except AssertionError:
        print("Error: given no arguments, script should search the current directory")
        sh.cd(os.path.dirname(current_path))


def test_python_script():
    print("test_python_script")

    executable = os.path.realpath("subtitle-downloader/subtitle_downloader.py")

    # should try all languages and print whether each download was successful
    # -a option should override language specifications, even invalid ones
    for file in VIDEO_FILES:
        sh.python(executable, "--verbose", "-a", "--language", "Engrish", file)

    sh.python(executable, VIDEO_DIRECTORY)      # test video directory

    # gather a list of subtitle files created before removing them
    sub_files = glob.glob(VIDEO_DIRECTORY + "*.srt")
    sh.Command("rm")("-rf", sub_files)

    # change directories to the path containing the video files
    current_path = os.path.realpath(__file__)
    sh.cd(os.path.abspath(VIDEO_DIRECTORY))

    # run vanilla command and ensure that the result is the same as before
    sh.python(executable)
    sub_files2 = glob.glob(VIDEO_DIRECTORY + "*.srt")

    try:
        assert sub_files == sub_files2
    except AssertionError:
        print("Error: given no arguments, script should search the current directory")

    sh.cd(os.path.dirname(current_path))


def main():
    # comment out as needed
    test_python_script()
    test_run_script()

if __name__ == "__main__":
    main()