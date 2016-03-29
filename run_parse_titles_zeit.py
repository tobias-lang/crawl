#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import article_parser
import collection_parser


class TitleParser(article_parser.ArticleParser):

    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'title':
            self.recording += 1


    def handle_endtag(self, tag):
        if tag == 'title' and self.recording:
            self.recording -= 1


    # Overridable
    def process_contents(self, data):
        i = data.find(u" | ZEIT ONLINE")
        return data[:i].strip()


input_dir = "out_zeit/"
output_filename = "out_contents/titles_zeit.txt"

collection_parser = collection_parser.CollectionParser(TitleParser())
collection_parser.run_full(input_dir, output_filename)

