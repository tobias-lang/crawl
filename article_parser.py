import traceback
from HTMLParser import HTMLParser
from urllib2 import urlopen
import urlparse
import codecs
import numpy as np

# work in progress


class ArticleParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()


    def reset(self):
        HTMLParser.reset(self)
        self.in_article_section = False
        self.recording = 0
        self.contents = []


    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            # print "guenther ist da"
            for (key, value) in attrs:
                if key == 'class' and value == "article-page":
                    self.in_article_section = True
        elif tag == 'p' and self.in_article_section:
            self.recording += 1


    def handle_endtag(self, tag):
        if tag == "section" and self.in_article_section:
            self.in_article_section = False
        if tag == 'p' and self.recording:
            self.recording -= 1


    def handle_data(self, data):
        if self.recording:
            processed_data = self.process_contents(data)
            if len(processed_data):
                self.contents.append(processed_data)


    def getContents(self):
        all_contents = " ".join(self.contents)
        return all_contents


    # Overridable
    def process_contents(self, data):
        splits = data.split("\n")
        splits = [s.strip() for s in splits]
        splits = map(lambda x: self.process_contents__additional(x), splits)
        splits = filter(lambda x: self.is_good_data_chunck(x), splits)
        answer = ""
        if len(splits):
            answer = " ".join(splits)
        return answer


    # Overridable
    def process_contents__additional(self, data_chunk):
        return data_chunk


    # Overridable
    def is_good_data_chunck(self, data_chunk):
        if ArticleParser.contains_code(data_chunk):
            return False
        if len(data_chunk) < 10:
            return False
        return True


    @staticmethod
    def contains_code(data_chunk):
        return "if(" in data_chunk or "typeof(" in data_chunk or "img{position:"  in data_chunk
