#!/usr/bin/env python

import optparse
import django
django.setup()
from django.conf import settings
from django.core.urlresolvers import reverse

import sys
import re
import requests

import datetime
from dateutil.parser import parse as dateparser
import pytz
import json

from PNGinfo import PNGinfo

HTTP_PREFIX = 'https'
from django.contrib.sites.models import Site
URL_PREFIX = Site.objects.get_current().domain

#URL_PREFIX = 'localhost'


def fixTimezone(the_time):
    if not the_time.tzinfo or the_time.tzinfo.utcoffset(the_time) is None:
        the_time = pytz.timezone('utc').localize(the_time)
    the_time = the_time.astimezone(pytz.utc)
    return the_time

def get_doc_metadata(filename):
    p = PNGinfo(filename)
    # The header will be json containing standard PNG header info
    metadata = p.header
    # The text will be DOC-specific, and contains two timestamps and several parameters
    for txt in p.text:
        if 'Comment' in txt:
            # Example DOC comment string: "Comment:8,0,0,0,2047,0,2047,299,1,1204871,3"
            # From Ted: the numbers you extracted mean:
            # 8 bit image,
            # xscale=0,
            # yscale=0,
            # x start = 0,
            # x end = 2047,
            # y start = 0,
            # y end = 2047,
            # exposure = 299 ms,
            # gain = 1,
            # compression quality = 1204871,
            # compression mode = 3
            match = re.search('Comment(\D+)([\d\,]+)', txt)
            if match:
                param = [int(s) for s in match.group(2).split(',')]
                label=['Bits per pixel','X Scale','Y Scale','X Start','X End','Y Start',
                       'Y End','Exposure','Gain','Compression Quality','Compression Mode']
                for i in range(10):
                    metadata[label[i]] = param[i]
        else:
            match = re.search('date:(\D+)([\d\-T\:]+)', txt)
            if match:
                timestamp = dateparser(match.group(2)).astimezone(pytz.utc)
                timestr = timestamp.isoformat()
                if 'create' in txt:
                    metadata['Creation Time'] = timestr
                    metadata['DateTimeOriginal'] = timestr
                elif 'modify' in txt:
                    metadata['Modify Time'] = timestr
    return metadata


def import_doc_image(filename, username, password):
    metadata = get_doc_metadata(filename)
    data ={
        'timezone':'utc',
        'vehicle':'',
        'username': username,
        'camera': 'NRVD',
        'exifData': json.dumps(metadata)
    }
    fp = open(filename)
    files = {'file': fp}

    # TODO: reverse is only getting the last part, missing '<http(s)>://<hostname>/'
    url = reverse('xgds_save_image')
    # ... so roll it like this:
    url = "%s://%s%s" % (HTTP_PREFIX, URL_PREFIX, '/xgds_image/rest/saveImage/')

    r = requests.post(url, data=data, files=files, verify=False, auth=(username, password))
    if r.status_code == 200:
        print 'HTTP status code:', r.status_code
        print r.text
        return 0
    else:
        sys.stderr.write('HTTP status code: ' + str(r.status_code) + '\n')
        sys.stderr.write(r.text)
        sys.stderr.write('\n')
        sys.stderr.flush()
        return -1


if __name__=='__main__':
    parser = optparse.OptionParser('usage: %prog')
    parser.add_option('-u', '--username', default='irg', help='username for xgds auth')
    parser.add_option('-p', '--password', help='authtoken for xgds authentication.  Can get it from https://xgds_server_name/accounts/rest/genToken/<username>')

    opts, args = parser.parse_args()

    doc_image_filename = args[0]
    retval = import_doc_image(doc_image_filename, opts.username, opts.password)
    sys.exit(retval)
