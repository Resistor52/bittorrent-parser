# bittorrent-parser.py README

This is a python program to parse one or more BitTorrent metainfo (*torrent) files.  The output is a HTML file.

## Requirements 

In addition to Python 2.7, you will need Jinja2, hurry.filesize, and bencode and possibly a few other libraries as  indicated in the import statements.  To use the included bash scripts you will need to to be using Linux.

## Syntax
To run the program type at the command line:
```
python parse-torrent.py myfile.torrent
```
or 
```
python parse-torrent.py myfile.torrent myoutput.html
```

where `myfile.torrent` is the name of the metainfo file to parse and 'myoutput.html' is the name of resulting output file.  If a name of the output file is not provided, it will default to `output.html`

Note that the extension of the metainfo file need not be "torrent."  For example if I want to prevent a BitTorrent client from accidently opening and starting to download the torrent, I can rename the metainfo file to something like *.torrentNOT

## Included Sample Scripts
- **getfiles.sh** --  This script allows one to download a bunch of metainfo files from [www.legittorrents.info](http://www.legittorrents.info).  Stop this file when you have enough or it will run until it has exhausted the list on the source.  In the case of legittorrents this will be several thousand.
- **cleanup.sh** --  This script keeps only the *.torrent files that are greater than 100 kb
- **generateoutput.sh** -- A script that calls bittorrent-parser.py for each *.torrent file found in the torrents directory.  Each file processed gets a sequential name and is listed in a master list called "list.html"

## References and acknowledgements: 
* [https://wikigurus.com/Article/Show/298784/Extract-the-SHA1-hash-from-a-torrent-file](https://wikigurus.com/Article/Show/298784/Extract-the-SHA1-hash-from-a-torrent-file)
* [http://error.news/question/139520/extract-the-sha1-hash-from-a-torrent-file/](http://error.news/question/139520/extract-the-sha1-hash-from-a-torrent-file/)
* [http://www.kristenwidman.com/blog/33/how-to-write-a-bittorrent-client-part-1/](http://www.kristenwidman.com/blog/33/how-to-write-a-bittorrent-client-part-1/)
* [https://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure](http://www.kristenwidman.com/blog/33/how-to-write-a-bittorrent-client-part-1/)


*Created by Kenneth G. Hartman -  [www.kennethghartman.com](www.kennethghartman.com)* 
