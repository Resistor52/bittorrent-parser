#!/bin/bash
# sample program to download multiple *.torrent files
# Created by Kenneth G. Hartman http://www.kennethghartman.com

# Make sure the required directories exist
if [ ! -d "downloaded" ]; then
  echo "created the downloaded/ directory" 
fi

# download a bunch of files
wget -r -nd -P downloaded/ http://www.legittorrents.info

