#!/usr/bin/env python
# -*- coding: utf-8 -*-
from darpdfurls import encode_url
import sys, os, re
import urllib2
from urllib2 import urlopen
import shutil
import urlparse

FILENAME_TEMPLATE = 'dar_%d_%02d_%03d.'

def make_filename(leg, sess, number, format="pdf"):
    leg = int(leg)
    sess = int(sess)
    number = int(number)
    return (FILENAME_TEMPLATE % (leg, sess, number)) + format.lower()

def download(leg, sess, number, format="pdf"):
    leg = int(leg)
    sess = int(sess)
    number = int(number)
    url = encode_url(leg, sess, num, format)
    filename = make_filename(leg, sess, number, format)
    cmd = 'wget "%s" --quiet --output-document %s' % (url, filename)
    if format.lower() == 'txt':
        cmd = 'lynx -dump -nolist -force_html -display_charset UTF-8 "%s" >%s' % (url, filename)
    import subprocess
    subprocess.call(cmd, shell=True)
    if format.lower() == 'txt':
        html = open(filename, 'r').read()
        raw = html.splitlines()
        file = open(filename, 'w')
        for line in raw:
            line = re.sub(r"^( +)(Aplausos.*)\.$", "\g<1>_\g<2>_.", line, re.UNICODE)
            line = re.sub(r"^( +)(Pausa)\.$", "\g<1>_\g<2>_.", line, re.UNICODE)
            line = re.sub(r"^( +)(Procedeu-se .{1,10} vota.{3,10})\.$", "\g<1>_\g<2>_.", line, re.UNICODE)
            line = re.sub(r"^( +)(Submetido .{1,10} vota.{3,50})\.$", "\g<1>_\g<2>_.", line, re.UNICODE)
            line = re.sub(r"^( +)(Eram [0-9]+ horas e [0-9]+ minutos)\.$", "\g<1>_\g<2>_.", line, re.UNICODE)
            line = re.sub(r"^( +)(Eram [0-9]+ horas)\.$", "\g<1>_\g<2>_.", line, re.UNICODE)            
            line = re.sub(r"^(.{0,10} Sr..? )([^:]*) (\([A-Z-]+\)): ", "\g<1>*\g<2>* \g<3>: ", line, re.UNICODE)
            line = re.sub(r"^(.{0,10} Sr..{0,2} )(Presidente)(( \([^\)]+\))?: )", "\g<1>*\g<2>*\g<3>", line, re.UNICODE)
            line = re.sub(r"^(.{0,10} Sr..{0,2} )(Secret.*ri[oa])([^:]{0,50}): ", "\g<1>*\g<2>*\g<3>: ", line, re.UNICODE)
            line = re.sub(r": - ",": — ", line, re.UNICODE)
            line = re.sub(r"^ *","", line, re.UNICODE)
            line = re.sub(r"(.*[^\.])$","\g<1> ", line, re.UNICODE)
            if not(re.match(r'.*[0-9]+ \| [XVI]+',line)): file.write(line + "\n")
        file.close()
        
def dar_exists(leg, sess, num, format="pdf"):
    url = encode_url(leg, sess, num, format)
    # Now we check if there's anything at the URL.
    # We always get return code 200 since there's a HTML error message, 
    # so we check if we're getting a PDF file or a HTML response.
    from urllib2 import urlopen
    response = urlopen(url)
    mimetype = response.info().values()[-1].split(';')[0]
    
    if format.lower() == 'pdf' and mimetype == 'application/pdf':
        return True
        print "Resource exists!"
    elif format.lower() == 'pdf' and mimetype == 'text/html':
        return False
    elif format.lower() == 'txt' and mimetype == 'text/html':
        content = response.read()
        if "<p>" in content:
            return True
            print "Resource exists!"    
    else:
        print mimetype
        raise ValueError

if __name__ == '__main__':
    if not len(sys.argv) == 5:
        print 'Give me 4 args (leg, session, number, file_format)'
        sys.exit()

    leg, sess, num, format = sys.argv[1:]
    if dar_exists(leg, sess, num, format):
        print "Resource exists! Downloading to %s..." % make_filename(leg, sess, num, format)
        download(leg, sess, num, format)
    else:
        print "Resource does not exist."