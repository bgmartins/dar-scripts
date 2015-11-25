#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import binascii
import re

def encode_url(leg, sess, number, format='pdf'):
    leg = int(leg)
    sess = int(sess)
    number = int(number)
    internal_url = "http://debates.parlamento.pt/pagina/export?exportType=" + format.lower() + "&exportControl=documentoCompleto&periodo=r3&publicacao=dar&serie=01&legis=%02d&sessao=%02d&numero=%03d"
    url = internal_url % (leg , sess, number)
    if format.lower() == 'txt':
        url2 = "http://debates.parlamento.pt/catalogo/r3/dar/01/%02d/%02d" % (leg , sess)
        url3 = "\/catalogo\/r3\/dar\/01\/%02d\/%02d\/%03d\/([^\"]*)" % (leg , sess, number)
        from urllib2 import urlopen
        response = urlopen(url2)
        content = response.read()
        url = url + "&data=" + re.search(url3, content).group(1)
    return url

def decode_url(url):
    hexstring = url.split('=')[1].split('&')[0]
    binstring = binascii.unhexlify(hexstring)
    internal_url = binascii.a2b_base64(binstring)
    return internal_url

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        print decode_url(url)
    elif len(sys.argv) == 4:
        print encode_url(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
            print encode_url(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print 'Only 1 argument (URL), 3 arguments (legislature, leg. session, number) or 4 arguments (legislature, leg. session, number, file_format) expected.'
        sys.exit()

