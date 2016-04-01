import sys
import traceback
import parse.link_parser
import parse.impl.zeit_title_parser


def is_interesting_url(url):
    if url.rfind("?")>0:
        return False
    if "#comments" in url:
        return False
    if "#" in url:
        return False
    if "/201" not in url:
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


def spider(domain, article_parser, maxPages, dir):
    pagesVisited = set()
    pagesToVisit = [domain]

    numVisited = 0
    numUsed = 0  # different from numVisited (as parsing can fail)

    titles = []

    while numVisited < maxPages and pagesToVisit != []:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        if url in pagesVisited:
            continue

        try:
            numVisited += 1
            print numVisited-1, "Visiting:", url
            pagesVisited.add(url)

            parser = parse.link_parser.LinkParser()
            page_data, page_links = parser.getLinks(url)

            page_links = filter_links(page_links, pagesVisited, domain)
            pagesToVisit = pagesToVisit + page_links

            if "/201" in url:
                article_parser.reset()
                article_parser.feed(page_data)
                title = article_parser.getContents()
                titles.append(title.encode("utf-8"))
                numUsed += 1
        except Exception as e:
            print(traceback.format_exc())

    f = open("titles.txt", "w")
    for t in titles:
        # s = unicode(t).encode('utf8')
        f.write(t + "\n")
    f.close()

    print titles
    print "done"



if __name__ == '__main__':
    domain = "http://www.zeit.de"
    maxPages = 100
    outDir = "../out/"
    article_parser = parse.impl.zeit_title_parser.TitleParser()

    # if len(sys.argv) < 4:
    #     print "usage: python run_download_websites <domain> <maxPages> <outDir>\n" \
    #           "<domain> = start-url (e.g. www.zeit.de)"
    #     exit(1)
    # domain = sys.argv[1]
    # maxPages = int(sys.argv[2])
    # outDir = sys.argv[3]

    print "domain,", domain
    print "maxPages,", maxPages
    print "outDir", outDir

    contents = spider(domain, article_parser, maxPages, outDir)

