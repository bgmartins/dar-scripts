#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import binascii

def encode_url(leg, sess, number):
    leg = int(leg)
    sess = int(sess)
    number = int(number)
    internal_url = "http://debates.parlamento.pt/pagina/export?exportType=pdf&exportar=Exportar&exportControl=documentoCompleto&periodo=r3&publicacao=dar&serie=01&legis=%02d&sessao=%02d&numero=%03d"
    url = internal_url % (leg , sess, number)
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
    else:
        print 'Only 1 argument (URL) or 3 (legislature, leg. session, number) expected.'
        sys.exit()

