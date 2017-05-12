#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pycurl

try:
    if sys.argv[1] == "-":
        urls = [u.strip() for u in sys.stdin.readlines()]
    else:
        urls = [u.strip() for u in open(sys.argv[1]).readlines()]
except:
    print("Usage: %s <file with URLs to fetch> [<# of concurrent connections>]" % sys.argv[0])
    raise SystemExit


num_urls = len(urls)

m = pycurl.CurlMulti()
m.setopt(pycurl.M_PIPELINING, 1)
m.setopt(pycurl.M_MAX_HOST_CONNECTIONS, 1)
m.handles = []
for i in range(num_urls):
    c = pycurl.Curl()
    c.fp = None
    m.handles.append(c)

freelist = m.handles[:]
for url in urls:
    c = freelist.pop()
    header_lines = [
        'User-Agent: PythonSDK',
        'Version: 4',
        'Content-Type: application/xml',
        'Accept: application/xml',
        'Authorization: Bearer MilBNsldleVhr2QbPKB5oGN9ar5KQG5SRwszW8yNO9SVtD6E_SJkumCXOxmbuEqc0IW6enK_H89jRKmTlF0azg',
    ]
    c.setopt(pycurl.COPYPOSTFIELDS, ''.encode('utf-8'))
    c.setopt(pycurl.HTTPHEADER, header_lines)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEDATA, open('/dev/null', 'wb'))
    c.setopt(pycurl.COOKIEFILE, '/dev/null')
    c.setopt(pycurl.COOKIEJAR, '/dev/null')
    c.setopt(pycurl.TIMEOUT, 0)
    c.setopt(pycurl.VERBOSE, 1)
    c.setopt(pycurl.DEBUGFUNCTION, mylog)
    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    m.add_handle(c)
    c.url = url

m_ok = set()
def wait(index):
    global m_ok
    while 1:
        ret, num_handles = m.perform()
        num_q, ok_list, err_list = m.info_read()
        m_ok = m_ok.union(set(ok_list))
        if m.handles[index] in m_ok:
            break

wait(0)
wait(1)
wait(2)

for c in m.handles:
    c.close()
m.close()
