from HTMLParser import HTMLParser
from urllib2 import urlopen
import urlparse

# CREDIT
# Mostly taken from:
# https://github.com/swapnil-k/python_programs/blob/master/crawler_py3.py

class LinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.contents = []


    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = urlparse.urljoin(self.baseUrl, value)
                    if " " not in newUrl and newUrl.count("http://") < 2:
                        self.links = self.links + [newUrl]


    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        handle = urlopen(url)

        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if 'text/html' in handle.info().getheader('Content-Type'):
            htmlLinesByte = handle.readlines()
            htmlLinesString = []
            for l in htmlLinesByte:
                try:
                    htmlLinesString.append(l.decode("utf-8"))
                except:
                    pass
            url_content = "\n".join(htmlLinesString)
            self.feed(url_content)
            return url_content, self.links
        else:
            return "", []


