#-------------------------------------------------------------------------------
# Name      : subtitle downloader
# Purpose   : One step subtitle download
#
# Authors   : manoj m j, arun shivaram p, Valentin Vetter, niroyb
# Edited by : Valentin Vetter
# Created   :
# Copyright : (c) www.manojmj.com
# Licence   : GPL v3
#-------------------------------------------------------------------------------

# TODO: use another DB if subs are not found on subDB

import hashlib
import os
import sys

PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    import urllib2
if PY_VERSION == 3:
    import urllib.request


def get_hash(file_path):
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def sub_downloader(file_path):
    # Put the code in a try catch block in order to continue for other video files, if it fails during execution
    try:
        # Skip this file if it is not a video
        root, extension = os.path.splitext(file_path)
        if extension not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp"]:
            return

        if not os.path.exists(root + ".srt"):
            headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
            url = "http://api.thesubdb.com/?action=download&hash=" + get_hash(file_path) + "&language=en"
            if PY_VERSION == 3:
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req).read()
            if PY_VERSION == 2:
                req = urllib2.Request(url, '', headers)
                response = urllib2.urlopen(req).read()

            # print "Subtitle successfully Downloaded for file " + fileName
            with open(root + ".srt", "wb") as subtitle:
                subtitle.write(response)
    except:
        #Ignore exception and continue
        print("Error in fetching subtitle for " + file_path)
        print("Error", sys.exc_info())


def main():
    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)

    for path in sys.argv:
        if os.path.isdir(path):
            # Iterate the root directory recursively using os.walk and for each video file present get the subtitle
            for dir_path, _, file_names in os.walk(path):
                for filename in file_names:
                    file_path = os.path.join(dir_path, filename)
                    sub_downloader(file_path)
        else:
            sub_downloader(path)

if __name__ == '__main__':
    main()
