#!/usr/bin/python3
import sys
import argparse

from inc.linkUtil import LinkUtil
from inc.storage import Storage



host = sys.argv[1]

st = Storage()
linkUtil = LinkUtil(host, st)


add_index = ("INSERT INTO indexes (url) VALUES (?)")
#linksArray = []
#linksArray.append(host)
linkUtil.appendHost(host)

print(linkUtil.linksArray)
for host in linkUtil.linksArray:
	linkUtil.crawlLink(host)
	
