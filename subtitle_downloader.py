#!/usr/bin/env python
'''Subtitle downloader utility using thesubdb'''
# -------------------------------------------------------------------------------
# Name      : subtitle downloader
# Purpose   : One step subtitle download
#
# Authors   : manoj m j, arun shivaram p, Valentin Vetter, niroyb
# Edited by : Valentin Vetter
# Created   :
# Copyright : (c) www.manojmj.com
# Licence   : GPL v3
# -------------------------------------------------------------------------------

# TODO: use another DB if subs are not found on subDB
from __future__ import print_function
import hashlib
import os
import sys

PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    import urllib2
if PY_VERSION == 3:
    import urllib.request

def log(message):
    print(message)

def get_hash(file_path):
    '''Returns the hash of a file as expected by subDB: http://thesubdb.com/api/
    We return the md5 of the concatenated first and last 64kb of data'''
    read_size = 64 * 1024
    with open(file_path, 'rb') as file_obj:
        data = file_obj.read(read_size)
        file_obj.seek(-read_size, os.SEEK_END)
        data += file_obj.read(read_size)
    return hashlib.md5(data).hexdigest()


def get_subtitles(file_hash):
    '''Return the subtitles text for the given movie file hash.'''
    headers = {'User-Agent':'SubDB/1.0 (subtitle_downloader/1.0; http://github.com/manojmj92/subtitle_downloader)'}
    url = "http://api.thesubdb.com/?action=download&hash={0}&language=en".format(file_hash)
    if PY_VERSION == 3:
        req = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(req).read()
    if PY_VERSION == 2:
        req = urllib2.Request(url, '', headers)
        response = urllib2.urlopen(req).read()
    return str(response)


def is_movie_file_extension(extension):
    '''Returns true if the passed in extension is a known movie extension.'''
    return extension in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov",
                         ".rm", ".vob", ".wmv", ".flv", ".3gp"]


def sub_download(file_path):
    '''Will try to download the subtitles for the given movie file path.
    The subtitle file will be placed in the same folder as the movie file.
    Returns the subtitle path.'''
    root, extension = os.path.splitext(file_path)

    # Skip this file if it is not a video
    if not is_movie_file_extension(extension):
        return

    # Don't redownload subs
    if os.path.exists(root + ".srt"):
        return

    # Ignore exceptions to continue seamlessly for other video files
    try:
        file_hash = get_hash(file_path)
        subs = get_subtitles(file_hash)
    except:
        # Ignore exception and continue
        log("Error in fetching subtitle for {0}".format(file_path))
        log("Error", sys.exc_info())
        return

    log("Subtitle successfully Downloaded for {0}".format(file_path))
    subtitle_path = root + ".srt"
    with open(subtitle_path, "wb") as subtitle:
        subtitle.write(subs)
    return subtitle_path


def sub_download_dir(path):
    '''Recursively downloads subtitles of movie files in the given directory'''
    for dir_path, _, file_names in os.walk(path):
        for filename in file_names:
            file_path = os.path.join(dir_path, filename)
            sub_download(file_path)


def main(argv):
    '''Main entry point'''
    if len(argv) <= 1:
        log("This program requires at least one parameterz")
        sys.exit(1)

    for path in argv:
        if os.path.isdir(path):
            sub_download_dir(path)
        else:
            sub_download(path)

if __name__ == '__main__':
    main(sys.argv)
