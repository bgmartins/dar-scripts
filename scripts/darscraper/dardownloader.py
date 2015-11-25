#!/usr/bin/env python
from darpdfurls import encode_url
import sys, os

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
    import subprocess
    subprocess.call(cmd, shell=True)

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