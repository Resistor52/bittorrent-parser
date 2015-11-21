# bittorrent-parser.py README

This is a python program to parse one or more BitTorrent metainfo (*torrent) files.  The output is a HTML file.

## Requirements 

In addition to Python 2.7, you will need Jinja2 and bencode and a few other libraries as  indicated in the import statements.  To use the included bash scripts you will need to to be using Linux.

## Syntax
To run the program type at the command line:
```
python bittorrent-parser.py myfile.torrent
```
or 
```
python bittorrent-parser.py myfile.torrent myoutput.html
```

where `myfile.torrent` is the name of the metainfo file to parse and 'myoutput.html' is the name of resulting output file.  If a name of the output file is not provided, it will default to `output.html`

Note that the extension of the metainfo file need not be torrent.  For example if I want to prevent a BitTorrent client from accidently opening and starting a download the torrent, I can rename the metainfo file to something like *.torrentNOT

## Included Sample Scripts
- **getfiles.sh** --  This script allows one to download a bunch or metainfo files from [www.legittorrents.info](http://www.legittorrents.info).  Stop this file when you have enough or it will run until it has exhausted the list on the source.  In the case of legittorrents this will be several thousand.
- **cleanup.sh** --  This script keeps only the *.torrent files that are greater than 100 kb
- **generateoutput.sh** -- A script that calls bittorrent-parser.py for each *.torrent file found in the torrents directory.  Each file processed gets a sequential name and is listed in a master list called "list.html"

