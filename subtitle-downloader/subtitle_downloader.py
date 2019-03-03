#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name      : subtitle downloader
# Purpose   : One step subtitle download
#
# Authors   : manoj m j, arun shivaram p, Valentin Vetter, niroyb
# Edited by : Valentin Vetter
# Created   :
# Copyright : (c) www.manojmj.com
# Licence   : GPL v3
#
#
# Edited for my using: Mohamed Hamza.
# Modified for multi-language support: Alex Mueller
#-------------------------------------------------------------------------------

import zipfile
import time
import sys
import shutil
import re
import os
import logging
import json
import hashlib
import glob

import click
import requests
from bs4 import BeautifulSoup
PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    import urllib2
if PY_VERSION == 3:
    import urllib.request

# List of ISO 639-1 two-letter language codes
# (reference: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
# This list is *very* incomplete. If your language doesn't appear here,
# feel free to add to the list. The program should still function as expected.
LANGUAGE_CODES = {
    "Arabic": "ar",
    "Chinese": "zh",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",      # Yes, I included Esperanto... just in case.
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Mongolian": "mn",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Spanish": "es",
    "Swedish": "sv",
    "Thai": "th",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Yiddish": "yi",
    "Zulu": "zu"
}

# List of video file extensions this program supports
VIDEO_EXTENSIONS = [
    ".avi", ".mp4", ".mkv", ".mpg",
    ".mpeg", ".mov", ".rm", ".vob",
    ".wmv", ".flv", ".3gp",".3g2"
]


def get_hash(file_path):
    """Return the hash of the video file."""
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def get_from_subdb(file_path, language, verbose=False):
    """Download subtitles from subdb."""
    try:
        # Skip this file if it is not a video
        root, extension = os.path.splitext(file_path)
        if extension not in VIDEO_EXTENSIONS:
            if verbose:
                print(file_path + " is not a video file. Skipping.")
            return

        language_code = LANGUAGE_CODES[language]
        filename = root + language_code + ".srt"

        if not os.path.exists(filename):
            headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
            url = "http://api.thesubdb.com/?action=download&hash=" + get_hash(file_path) + "&language=" + language_code
            if PY_VERSION == 3:
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req).read()
            if PY_VERSION == 2:
                req = urllib2.Request(url, '', headers)
                response = urllib2.urlopen(req).read()

            with open(filename, "wb") as subtitle:
                subtitle.write(response)
                if verbose:
                    print(language + " subtitles successfully downloaded for " + file_path)
                # logging.info(language + " subtitles successfully downloaded for " + file_path)

    except:
        if verbose:
            print(language + " subtitles not found for " + file_path + " in subdb")


def get_from_subscene(file_path, language):
    """Download subtitles from subscene."""
    try:
        root, extension = os.path.splitext(file_path)
        if extension not in VIDEO_EXTENSIONS:
            return

        j=-1
        root2=root
        for idx, char in enumerate(reversed(root)):
            if(char == "\\" or char =="/"):
                j = len(root)-1 - idx
                break
        root=root2[j+1:]
        root2=root2[:j+1]
        print("language is " + language)
        r=requests.get("http://subscene.com/subtitles/release?q="+root);
        soup=BeautifulSoup(r.content,"lxml")
        atags=soup.find_all("a")
        href=""
        for i in range(0,len(atags)):
            spans=atags[i].find_all("span")
            if(len(spans)==2 and spans[0].get_text().strip()==language and spans[1].get_text().strip()==root):
                href=atags[i].get("href").strip()
        print(href)
        if(len(href)>0):
            r=requests.get("http://subscene.com"+href);
            soup=BeautifulSoup(r.content,"lxml")
            lin=soup.find_all('a',attrs={'id':'downloadButton'})[0].get("href")
            print('this lint', lin)
            r=requests.get("http://subscene.com"+lin);
            soup=BeautifulSoup(r.content,"lxml")
            subfile=open(root2+" {}.zip".format(language), 'wb')
            for chunk in r.iter_content(100000):
                subfile.write(chunk)
                subfile.close()
                time.sleep(1)
                zip_=zipfile.ZipFile(root2+" {}.zip".format(language)) #Naming zip is not recommended renamed it to zip_ (Following PEP 8 convention)
                zip_.extractall(root2)                                 #Naming it as zip would overwrite built-in function zip
                zip_.close()
                os_.unlink(root2+" {}.zip".format(language))
                shutil.move(root2+zip.namelist()[0], os.path.join(root2, root + " {}.srt".format(language)))
    except:
        #Ignore exception and continue
        print("Error in fetching subtitle for " + file_path)
        print("Error", sys.exc_info())
        logging.error("Error in fetching subtitle for " + file_path + str(sys.exc_info()))


@click.command(context_settings=dict(max_content_width=80))
@click.option("download_all", "--all", "-a", is_flag=True, 
              help="""Download subtitles in all available languages (nullifies '-i' or '-l')

              If subtitles cannot be found in a particular language, the download for that language will fail silently unless the verbose option is specified.
              \b

              """)
@click.option("--iso", "-i", default="en",
              help="""Specify the ISO 639-1 two-letter code that corresponds to your chosen subtitle language. For example, you would specify '--iso=fr' if you wanted French subtitles.

              If both the ISO value and the language name are specified, the ISO value takes priority.
              \b

              """)
@click.option("--language", "-l", default="English",
              help="""Select subtitle language by name (default: English).
              \b

              """)
@click.option("list_languages", "--list", is_flag=True,
              help="""List all available language name / ISO 639-1 code pairs and exit.
              \b

              """)
@click.option("--verbose", "-v", is_flag=True,
              help="""If this flag is on, console output will indicate which downloads were / were not successful.
              \b

              """)
@click.argument("input_path", type=click.Path(), default="./")
def main(download_all, iso, language, list_languages, verbose, input_path):
    """General purpose subtitle downloader."""
    if list_languages:
        # JSON for pretty-printing
        print(json.dumps(LANGUAGE_CODES, indent=4))
        sys.exit(0)

    # Put square brackets into character class so they work with glob
    glob_path = re.sub("([\[\]])", "[\g<1>]", input_path)

    # root, _ = os.path.splitext(input_path)
    # logging.basicConfig(filename=root + '.log', level=logging.INFO)
    # logging.info("Started with params " + str(sys.argv))

    languages = []
    if download_all:
        langauges = LANGUAGE_CODES.keys()
    else:
        if iso not in LANGUAGE_CODES.values():
            click.echo("Error: language code '" + iso + "' is unsupported.\n\nFor"
                       "a list of valid language codes, use the '--list' option.")
            click.echo("")
            click.echo("To add support for this language, open the python \n"
                       "source code and modify LANGUAGE_CODES accordingly.")
            sys.exit(1)

        if language not in LANGUAGE_CODES:
            click.echo("Error: language '" + language + "' is unsupported.\n\nFor"
                       "a list of supported languages, use the '--list' option.")
            click.echo("")
            click.echo("To add support for this language, open the python \n"
                       "source code and modify LANGUAGE_CODES accordingly.")
            sys.exit(1)

        # if both iso and language options are present, iso takes priority.
        if LANGUAGE_CODES[language] != iso:
            if verbose:
                click.echo("Language name '" + language + "' does not match"
                           " ISO 639-1 language code '" + iso + "'.")

            # the dictionary is mapped by language name, so we have to reverse it
            # to get the language name based on the code entered. This approach is
            # slightly inefficient, but I personally find it much more readable.
            language = dict(map(reversed, LANGUAGE_CODES.items()))[iso]
            if verbose:
                click.echo("Proceeding with language '" + language + "'"
                           " (the language specified by the code).")

        languages.append(language)

    for lang in languages:
        if os.path.isdir(input_path):
            files = []
            for extension in VIDEO_EXTENSIONS:
                for file in glob.glob(glob_path + "*" + extension):
                    files.append(file)
            for file in files:
                get_from_subdb(file, lang, verbose=verbose)
        else:
            get_from_subdb(input_path, lang, verbose=verbose)


if __name__ == '__main__':
    main()
