IFS_BAK=$IFS
IFS="
"

for line in $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS; do
        full_path="/home/"$USER"/Desktop/"subtitle_downloader.py
        python $full_path $line 
        notify-send $line
done

IFS=$IFS_BAK




##to do::#give a check here to see if the files coming are .mp4........videoformat files only otherwise exit.....
#to do::also we can give languagae as second parameter
#path to save in ~/.gnome2/nautilus-scripts
