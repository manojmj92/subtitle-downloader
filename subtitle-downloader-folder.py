#-------------------------------------------------------------------------------
# Name		: subtitle downloader folder
# Purpose	: Download subtitle for any number of movies at once.
# 
# Authors	: manoj m j, arun shivaram p, Avinash Srivastava
#Edited by     : Rahil Sharma
# Created	:
# Copyright	: (c) www.manojmj.com
# Licence	: GPL v3
#-------------------------------------------------------------------------------
import os
import hashlib
import sys

try:
    import urllib.request, urllib.parse
    pyVer = 3
except ImportError:
    import urllib2
    pyVer = 2
 
# The get_hash function return a unique hash for each video file. The subscene API uses an unique hash, calculated from the video file to match a subtitle    
def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

# Add any video extensions in case I missed any :)
videoExtensions = [".avi",".mp4",".mkv",".mpg",".mpeg",".mov",".rm",".vob",".wmv",".flv",".3gp"]

def sub_downloader(fileName):
    # Put the code in a try catch block in order to continue for other video files, if it fails during execution
    try:            
        originalFileName = fileName
        for videoExtension in videoExtensions:
            fileName = fileName.replace(videoExtension,"")
        
        # The originalFilename is same as the fileName, implies the file may not be video file at all and there is no point in wasting 
        # a http request and calculating a hash for a file which isn't of a video mimetype.      
        if originalFileName == fileName:
            return

        hash = get_hash(originalFileName)
        
        if not os.path.exists(fileName + ".srt"):    
            headers = { 'User-Agent' : 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)' }
            url = "http://api.thesubdb.com/?action=download&hash=" + hash + "&language=en"
            if pyVer == 3:
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req).read()
            else:
                req = urllib2.Request(url, '', headers)
                response = urllib2.urlopen(req).read()                
            
            #print "Subtitle successfully Downloaded for file " + fileName
            with open (fileName + ".srt", "wb" ) as subtitle:
                subtitle.write(response)
    except:
        #Ignore exception and continue
        print "Error in fetching subtitle for " + fileName          
            
    
rootdir = sys.argv[1]
# Iterate the root directory recursively using os.walk and for each video file present get the subtitle
for root, subFolders, files in os.walk(rootdir):
    for file in files:                
        fname = os.path.join(root, file)
        sub_downloader(fname)