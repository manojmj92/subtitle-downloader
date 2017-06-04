Subtitle Downloader
===================

Python script to download english subtitles of any movie/tv series episode.


Get the latest version of Python at http://www.python.org/getit/.

### Usage:
If you have python in your path, simply drag and drop files and folders you wish to get subtitles from on subtitle-downloader.py

#### Windows:
* Install Python
    Follow the steps at http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7 to set the python path.

* Place subtitle-downloader.py file in C:\

* Place the Subtitle.cmd in sendto folder in windows (can be accessed by typing shell:sendto in address bar)

* Right click the movie file (not the movie folder). You can also select multiple files.
and click sendto -> Subtitle.cmd

* If you want to download subtitles for all movies in a folder, you can use a folder as parameter to subtitle-downloader.py.

#### Mac:
* Install python and make sure it is in your path

* Open Automator and create a new document of type "Service"

* Add an action called "Run Shell Script"

* On the top, under 'Service receives selected' drop-down, select 'files or folder' and in the next drop-down, for 'in' select 'Finder'

* On the right top of the Run Shell Script action, make sure you selected "as arguments" for "Pass Input"

* Copy the contents of subtitle.sh in the action

* Edit the path to "Subtitle_downloader.py" to wherever you have downloaded

* Press `Command + S` to save it and give some name like "Download Subtitle"

* Now, Right click the movie file (not the movie folder). You can also select multiple files. Click Services -> Download Subtitle


##### Linux with Nautilus file manager(Tested on Debian Based with nautilus as file manager):
* Install python

* Go to ~/.local/share/nautilus/scripts/ (Ubuntu 13.04 or above) OR ~/.gnome2/nautilus-scripts/ (Ubuntu 12.10 and below) folder and add Subtitles_in_english.sh in the folder.

* The path for Subtitle_downloader.py is hardcoded to Desktop ...U can change it accordingly.

* Now Right Click on the movie file (not the movie folder). You can also select multiple files. Click Services -> Subtitles_in_english.


![ScreenShot](https://cloud.githubusercontent.com/assets/1637697/3078931/1a693b9a-e487-11e3-8d51-64dce970ad9d.gif)

Voila. the .srt subtitle file will be created right next to your movie file.

Enjoy the show!

More details can be found here : qr.ae/GxOcx
A how to video can be found here: http://www.youtube.com/watch?v=Q5YWEqgw9X8

##### Linux with NEMO file manager(Tested on Debian Based with NEMO as file manager):
* Install python

* Go to ~/.gnome2/nemo-scripts folder and add Subtitles_In_English_for_nemo.sh in the folder.

* The path for Subtitle_downloader.py is hardcoded to Desktop ...You can change it accordingly.

* Open terminal and execute following command :
```
chmod +x ~/.gnome2/nemo-scripts/Subtitles_In_English_for_nemo.sh
```

* Now Right Click on the movie file (not the movie folder). You can also select multiple files. Click Services -> Subtitles_In_English_for_nemo.

Voila. the .srt subtitle file will be created right next to your movie file.
