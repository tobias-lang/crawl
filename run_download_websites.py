import traceback
from HTMLParser import HTMLParser
from urllib2 import urlopen
import urlparse
import sys


# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.contents = []


        # This is a function that HTMLParser normally has

    # but we are adding some functionality to it
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
                    # And add it to our colection of links:
                    if " " not in newUrl and newUrl.count("http://") < 2:
                        self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        handle = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        # print "CONTENT TYPE ", handle.info().getheader('Content-Type')
        if 'text/html' in handle.info().getheader('Content-Type'):
            htmlLinesByte = handle.readlines()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlLinesString = []
            for l in htmlLinesByte:
                try:
                    htmlLinesString.append(l.decode("utf-8"))
                except:
                    sdf
            one_big_string = "\n".join(htmlLinesString)
            self.feed(one_big_string)
            return one_big_string, self.links
        else:
            return "", []


def getContents(self):
    all_contents = " ".join(self.contents)
    return all_contents


def is_interesting_url(url):
    if url.rfind("?")>0:
        return False
    if "#comments" in url:
        return False
    if "#" in url:
        return False
    return True


def filter_links(links, pagesVisited, domain):
    links = filter(lambda x: x not in pagesVisited, links)
    links = filter(lambda x: domain in x, links)
    links = filter(lambda x: is_interesting_url(x), links)
    return links


def write_website(data, filename):
    import codecs
    try:
        f = codecs.open(filename, "w", "utf-8")
        f.write(data)
        f.close()
    except Exception as e:
        print(traceback.format_exc())


# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(domain, maxPages, dir):
    pagesVisited = set()
    pagesToVisit = [domain]
    numberVisited = 0
    all_contents = set()

    file_id = 1

    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and pagesToVisit != []:
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        if url in pagesVisited:
            continue

        try:
            numberVisited = numberVisited + 1
            print numberVisited, "Visiting:", url
            pagesVisited.add(url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            filename = dir + "/" + "website" + str(file_id) + "__" + url[url.rfind("/")+1:] + ".html"
            file_id += 1
            write_website(data, filename)
            links = filter_links(links, pagesVisited, domain)
            # Add the pages that we visited to the end of our collection
            # of pages to visit:
            pagesToVisit = pagesToVisit + links
        except Exception as e:
            print(traceback.format_exc())
    return all_contents



domain = sys.argv[1]
maxPages = int(sys.argv[2])
outDir = sys.argv[3]

print "domain,", domain
print "maxPages,", maxPages
print "outDir", outDir

contents = spider(domain, maxPages, outDir)

