#!/usr/bin/env python
#coding=utf-8
#
# Generate a list of  rules for gfwlist
#
# Copyright (C) 2014 http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules

from requests import request
import base64

import re
import os
import datetime
import base64
import shutil

mydnsip = '127.0.0.1'
mydnsport = '5352'

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
tmpfile = '/tmp/gfwlisttmp'
# do not write to router internal flash directly
outfile = '/tmp/gfwlist.conf'


fs =  open(outfile, 'w')
fs.write('# gfw list  rules\n')
fs.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
fs.write('#\n')

print ('fetching list...')
#content = urllib2.urlopen(baseurl, timeout=15).read().decode('base64')
response=request('GET',baseurl)
content=base64.b64decode(response.text).decode('utf-8')

# write the decoded content to file then read line by line
tfs = open(tmpfile, 'w')
tfs.write(content)
tfs.close()
tfs = open(tmpfile, 'r')

print ('page content fetched, analysis...')

# remember all blocked domains, in case of duplicate records
domainlist = []

for line in tfs.readlines():
        if re.findall(comment_pattern, line):
                pass
                #print ('this is a comment line: ' + line)
                #fs.write('#' + line)
        else:
                domain = re.findall(domain_pattern, line)
                if domain:
                        try:
                                found = domainlist.index(domain[0])
                                #print (domain[0] + ' exists.')
                        except ValueError:
                                #print ('saving ' + domain[0])
                                domainlist.append(domain[0])
                                fs.write('DOMAIN-SUFFIX,%s,gfw_domian_list\n'%domain[0])
                else:
                        print ('no valid domain in this line: ' + line)

tfs.close()
fs.close();


print ('done!')

