#!/bin/bash
# sample program to download multiple *.torrent files
# Created by Kenneth G. Hartman http://www.kennethghartman.com

# Make sure the required directories exist
if [ ! -d "torrents" ]; then
  mkdir torrents
  echo "created the torrents/ directory" 
fi

# Move torrent files and remove the orininal path from the downloaded files. Ignore
# any files smaller tham 100 bytes as this indicates a download error
for item in $(find downloaded/. -name "*.torrent" -type f -size +100); do part=$(echo $item | cut -d "=" -f3) ; mv $item torrents/$part ; done

rm downloaded/*
