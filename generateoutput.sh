#!/bin/bash
# sample program to parse multiple *.torrent files
# Created by Kenneth G. Hartman http://www.kennethghartman.com

# Make sure the required directories exist
if [ ! -d "output" ]; then
  mkdir output
  echo "created the output/ directory"
else 
  rm output/*
fi
echo "<html><head><title>list.html</title></head><body>" > output/list.html
echo -e "infohash\tcreation_date\tpiece_length\tnumber_pieces\tnumber_files\ttorrent_size\terror" > statistics.csv
counter=0
wd=$(pwd)
for item in $(find torrents/ -name "*.torrent"); do
    counter=$((counter+1))
    #echo $item
    part=$(echo $item | cut -d"/" -f2)
    ./parse-torrent.py $item output/Output-$counter.html
    if [ "$?" = "0" ]; then
        echo "<a href=\"Output-$counter.html\">$part</a></br>" >> output/list.html	
    else
	echo "This file was not added to list.html" 1>&2
        echo $item > errors.txt
    fi   
done
echo "</body></html>" >> output/list.html
echo "DONE"

echo "Open file://"$(pwd)"/output/list.html in a browser to get an index listing of all of the output files"

