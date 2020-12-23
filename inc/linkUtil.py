import re
import urllib.request
from urllib.error import HTTPError, URLError
from socket import timeout

class LinkUtil:

    def __init__(self,baseHost, storage):
        self.currentLink = ''
        self.linksArray = []
        self.baseHost = baseHost
        self.storage= storage

       
    
    def appendHost(self,host):
        self.linksArray.append(host)

    def setCurrentLink(self,link):
        self.currentLink = link
    
    def setBaseHost(self, baseHost):
        self.baseHost = baseHost

    def chekLink(self) :
        
        linkTarget = self.currentLink
    
        res = False
        if linkTarget.find('#') != 0 :
            if linkTarget.find('javasript') != 0:
                if linkTarget.find('mailto') != 0:
                    if linkTarget.find('tel') != 0:
                        if linkTarget.find('ftp') != 0:
                            res = True
        return res

    def checkHost(self):
        if self.currentLink.find('/') == 0:
            self.currentLink = self.baseHost + self.currentLink
        return self.currentLink
    
    def parseBody(self,bodyText):
        regex = re.compile(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1', re.MULTILINE)
        for match in regex.finditer(bodyText):
            group = match.group()
            attributes = group.split(' ')

            for attribute in attributes:
                pos = attribute.find('href')
                if pos == 0:
                    parts = attribute.split('=')
                    linkTarget = parts[1]
                    linkTarget =  linkTarget.replace('"', '')
                    self.setCurrentLink(linkTarget)
                    canUseLink = self.chekLink()
                    
                    if canUseLink :
                        linkTarget = self.checkHost()
                        if  linkTarget not in self.linksArray:
                            self.linksArray.append(linkTarget)	
                            self.storage.save(linkTarget)
                            

    def crawlLink(self, host):
        try:

            request = urllib.request.Request(host)
            
            with urllib.request.urlopen(request, timeout=10) as content:
                
                contentType = content.getheader('Content-Type', 'undef')
                contentTypeInfo = contentType.split(';')
                if len(contentTypeInfo) == 2:
                    if contentTypeInfo[0] == 'text/html':
                        charsetInfo = contentTypeInfo[1].split('=')
                        if len(charsetInfo) == 2:

                            charset = charsetInfo[1]
                            
                            body = content.read()
                            
                            if charset == 'urtf-8':
                                charset = 'utf-8'
                            bodyText = body.decode(charset)
                            parseResult = urllib.parse.urlparse(host)
                            
                            self.setBaseHost(parseResult.scheme + '://' + parseResult.netloc )
                            
                            self.parseBody(bodyText)
                        else:
                            print(charsetInfo)


        except HTTPError as error:
            print('Data not retrieved because URL:' + host)
            print(error)
        except URLError as error:
            
                print('some other error happened URL:' + host)

        except ValueError:
            print("OOOppps ")
            print( host )					


