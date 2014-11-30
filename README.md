Subtitle Downloader
===================

Python script to download english subtitles of any movie/TV series episode.


Get the latest version of Python at http://www.python.org/getit/.

### Usage:
#### Windows:
* Install Python and make sure it is in your path. Follow the steps at http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7 to set the python path.

* Place subtitle-downloader.py file in C:\

* Place the Subtitle.cmd in sendto folder in windows (can be accessed by typing shell:sendto in address bar)

* Right click the movie file/folder(s) and click sendto -> Subtitle.cmd

* If you want to access it directly in the right-click menu, open regedit.exe and go to HKEY_CLASSES_ROOT/SystemFileAssociations. For each video file (mkv, avi, mp4, etc.), you need to add a key, as follows: for instance for mkv files, go to .mkv, create the Shell sub-folder if it is not present, right-click on Shell > New > Key, call it 'Download subtitles'. Then, similarly create a new key under the 'Download subtitles' folder called 'command', double click on default value and in its data, write: path\to\Subtitle.cmd "%L"


#### Mac:
* Install python and make sure it is in your path

* Open Automator and create a new document of type "Service"

* Add an action called "Run Shell Script"

* On the right top of the Run Shell Script action, make sure you selected "as arguments" for "Pass Input"

* Copy the contents of subtitle.sh in the action

* Edit the path to "Subtitle_downloader.py" to whereever you have downloaded

* Press `Command + S` to save it and give some name like "Download Subtitle"

* Now, Right click the movie file/folder(s) and Click Services -> Download Subtitle


#####Linux (Tested on Debian Based):
* Install python

* Go to ~/.gnome2/nautilus-scripts folder and add Subtitles\_in\_english.sh in the folder

* The path for Subtitle_downloader.py is hardcoded to Desktop... You can change it accordingly

* Now Right Click on the movie file/folder(s) and Click Services -> Subtitles\_in\_english


![ScreenShot](https://cloud.githubusercontent.com/assets/1637697/3078931/1a693b9a-e487-11e3-8d51-64dce970ad9d.gif)

Voila! The .srt subtitle file will be created right next to your movie file.

Enjoy the show!

More details can be found here : qr.ae/GxOcx
A how to video can be found here: http://www.youtube.com/watch?v=Q5YWEqgw9X8
