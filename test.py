import requests
import json
import urllib

# d = json.loads(urllib.request.urlopen('http://130.82.239.210/list').read().decode("utf-8"))
# # print(d)
# for i in d['gateway']['signals']:
#     print(i)

from ftplib import FTP
ftp = FTP('82.165.25.152')
ftp.login()
