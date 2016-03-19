#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Kenneth G. Hartman http://www.kennethghartman.com

# References and acknowledgements: 
# https://wikigurus.com/Article/Show/298784/Extract-the-SHA1-hash-from-a-torrent-file
# http://error.news/question/139520/extract-the-sha1-hash-from-a-torrent-file/
# http://www.kristenwidman.com/blog/33/how-to-write-a-bittorrent-client-part-1/
# https://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure

import sys, codecs, hashlib, bencode, binascii, os, time
from jinja2 import Environment, FileSystemLoader
from hurry.filesize import size


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def make_html(
        torrent_filename, 
        infohash,
        announce,
        announce_list,
        creation_date,
        comment,
        created_by,
        encoding,
        piece_length,
        private,
        sflength,
        sfmd5sum, 
        files, 
        piecehashes,
        last_piece_size,
        torrent_size,
        torrent_type,
        last_piece_percent,
        errmsg
        ):

    if sflength !="":
        sflength_hr = size(sflength)
    else:
        sflength_hr = ""
    if type(creation_date) != type(1):
        creation_date_conv = ""
    else: 
        creation_date_conv = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_date))
        creation_date_conv = "(" + creation_date_conv + ")"
    context = {
        'torrent_filename':unicode(torrent_filename, "utf8"),
        'infohash':infohash,
        'announce':announce,
        'announce_list':announce_list,
        'creation_date':creation_date,
        'creation_date_conv': creation_date_conv,
        'comment':unicode(comment, "utf8"),
        'created_by':unicode(created_by, "utf8"),
        'encoding':encoding,
        'piece_length':piece_length,
        'piece_length_hr':size(piece_length),
        'private':private,
        'sflength':sflength,
        'sflength_hr':sflength_hr,
        'sfmd5sum':sfmd5sum,
        'files':files,
        'piecehashes':piecehashes,
        'num_pieces':len(piecehashes),
        'last_piece_size': last_piece_size,
        'last_piece_size_hr': size(last_piece_size),
        'torrent_size': torrent_size,
        'torrent_size_hr': size(torrent_size),
        'torrent_type': torrent_type,
        'last_piece_percent': last_piece_percent,
        'errmsg': errmsg
    }
    
    with codecs.open(outfile, 'wb', 'utf-8') as f:
        if torrent_type == 'single file torrent':
            html = render_template('single.html', context)
        if torrent_type == 'multiple file torrent':
            html = render_template('multiple.html', context)
        f.write(html)

    with open("statistics.csv", "a") as f:
	record = str(infohash) + "\t" + str(creation_date_conv) + "\t" + str(piece_length) + "\t"
        record += str(len(piecehashes)) + "\t" + str(len(files)) + "\t" + str(torrent_size) + errmsg + "\n"
        f.write(record)

def main():
    torrent_filename = sys.argv[1]
    torrent_file = open(torrent_filename, "rb")
    try:
        metainfo = bencode.bdecode(torrent_file.read())
    except:
        sys.exit(torrent_filename + " is not a valid *.torrent file\n")
    announce = metainfo['announce']
    if 'announce-list' in metainfo:
        announce_list = metainfo['announce-list']
    else:
        announce_list = ""
    if 'creation date' in metainfo:
        creation_date = metainfo['creation date']
    else:
        creation_date = ""
    if 'comment' in metainfo:
        comment = metainfo['comment']
    else:
        comment = ""
    if 'created by' in metainfo:
        created_by = metainfo['created by']
    else:
        created_by = ""
    if 'encoding' in metainfo:
        encoding = metainfo['encoding']
    else:
        encoding = ""
    info = metainfo['info']
    piece_length = info['piece length']
    pieces = info['pieces']
    if 'private' in info:
        private = info['private']
    else:
        private = ""
    if 'name' in info:
        name = info['name']
    else: 
        name = ""
    if 'length' in info:
        sflength = info['length']
    else:
        sflength = ""
    if 'md5sum' in info:
        sfmd5sum = info['md5sum']
    else:
        sfmd5sum = ""
    if 'files' in info:  
        files = info['files']
    else:
        files = []
    infohash = hashlib.sha1(bencode.bencode(info)).hexdigest()
    piecehashes = [binascii.hexlify(pieces[i:i+20]) for i in range(0, len(pieces), 20)]
    torrent_size = 0
    
    for i in files:
        torrent_size += i['length']
        for j in range(len(i['path'])):
            i['path'][j] = unicode(i['path'][j], "utf8")
    if torrent_size == 0:
        torrent_type = 'single file torrent'
        torrent_size = sflength
    else:
        torrent_type = 'multiple file torrent' 
    last_piece_size = (len(piecehashes) * piece_length) - torrent_size
    last_piece_percent = '{:.1%}'.format(float(last_piece_size) / piece_length)
    errmsg = ""
    if last_piece_size > piece_length:
        errmsg += "WARNING: The calculated length of the last piece is greater than the stated piece length\n"
    if ((piece_length > torrent_size) and (torrent_type == 'multiple file torrent')):
        errmsg += "WARNING: The stated length of an individual piece is greater than the calculated torrent size\n"
    make_html(
        torrent_filename, 
        infohash,
        announce,
        announce_list,
        creation_date, 
        comment,
        created_by,
        encoding,
        piece_length,
        private,
        sflength,
        sfmd5sum, 
        files, 
        piecehashes,
        last_piece_size,
        torrent_size,
        torrent_type,
        last_piece_percent,
        errmsg
        )

if __name__ == "__main__":
    errormessage = "Expected syntax is: \n" + sys.argv[0] + " torrentfile \n or \n" + sys.argv[0] + " torrentfile output.html\n" 
    if len(sys.argv) < 2:
        print errormessage
        exit()
    if len(sys.argv) > 3:
        print errormessage
        exit()
    if len(sys.argv) == 3:
        outfile = sys.argv[2]
    else:
        outfile = "output.html"
    main()
